# How to Run Full API Tests

## Problem: Cached API Process

There are multiple Python/uvicorn processes running that are serving cached/old code (v1.0.0 instead of v1.1.0).

## Solution: Manual Testing Steps

### Step 1: Stop ALL Python Processes

```bash
# Kill all Python processes
taskkill /F /IM python.exe
taskkill /F /IM uvicorn.exe

# Verify port 8000 is free
npx kill-port 8000
```

### Step 2: Clear Python Cache

```bash
cd pyjhora-api

# Delete all .pyc files and __pycache__ directories
del /S /Q *.pyc
for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d"
```

### Step 3: Start Fresh API

```bash
# Start API (this will block the terminal)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

You should see:
```
INFO:     Will watch for changes in these directories: ['H:\\claude code\\pyjhora-api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Step 4: Verify API Version (in NEW terminal)

```bash
curl http://localhost:8000/
```

Should show:
```json
{
  "name": "PyJHora Vedic Astrology API",
  "version": "1.1.0",  <-- IMPORTANT: Should be 1.1.0
  ...
}
```

### Step 5: Run Comprehensive Tests (in NEW terminal)

```bash
cd pyjhora-api
python test_full_api.py
```

Expected results:
- **35 total tests**
- **35/35 should PASS (100%)**
- All categories should show SUCCESS

## Individual Feature Tests

If you want to test specific features:

### Test Phase 5 (Transits & Panchanga)
```bash
python test_phase5_transits_panchanga.py
```

### Test Phases 1-4
```bash
python test_bhukti.py
python test_yogas_doshas.py
python test_strength.py
python test_panchanga_compatibility.py
python test_phase4.py
```

## Expected Test Results

When the API is running v1.1.0 correctly, you should see:

```
========================================================================================================================
OVERALL RESULTS: 35/35 tests passed (100.0%)
========================================================================================================================

[SUCCESS] ALL TESTS PASSED!
API is fully functional and production-ready.
```

### Breakdown by Category:
- ✅ **Utility (4/4)** - Root, Health, Ayanamsa list, Chart types
- ✅ **Charts (16/16)** - All divisional charts D1-D60
- ✅ **Dashas (3/3)** - Vimsottari, Bhukti, Current
- ✅ **Yogas (1/1)** - 100+ yogas detection
- ✅ **Doshas (1/1)** - 8 doshas detection
- ✅ **Strength (2/2)** - Ashtakavarga, Shadbala
- ✅ **Panchanga (2/2)** - Basic + Extended
- ✅ **Compatibility (1/1)** - Marriage matching
- ✅ **Special (2/2)** - Special lagnas, Bhava Bala
- ✅ **Transits (3/3)** - Current positions, Sade Sati, Planet entries

## Troubleshooting

### Issue: Still seeing v1.0.0

**Problem:** Old Python bytecode is cached

**Solution:**
```bash
# Clear Python environment variables
set PYTHONDONTWRITEBYTECODE=1

# Delete all cached files
python -Bc "import compileall, shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"

# Restart Python shell
exit
```

### Issue: Port 8000 already in use

**Problem:** Old uvicorn process still running

**Solution:**
```bash
# Find process holding port 8000
netstat -ano | findstr :8000

# Kill by PID (replace XXXX with actual PID)
taskkill /F /PID XXXX

# Or use npx
npx kill-port 8000
```

### Issue: Tests failing with Connection Refused

**Problem:** API not running

**Solution:**
1. Make sure API is running: `python -m uvicorn app.main:app --reload`
2. Check health: `curl http://localhost:8000/health`
3. If health fails, check for errors in API terminal

## API Documentation

Once API is running, access:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Quick Verification

```bash
# 1. Check API is running v1.1.0
curl http://localhost:8000/ | python -m json.tool | grep version

# 2. Test a Phase 5 endpoint (Transits)
curl -X POST http://localhost:8000/api/v1/transits/current \
  -H "Content-Type: application/json" \
  -d "{\"birth_data\":{\"date\":\"2026-01-01\",\"time\":\"12:00:00\",\"latitude\":12.9716,\"longitude\":77.5946,\"timezone_offset\":5.5},\"ayanamsa\":\"LAHIRI\"}"

# 3. Test Extended Panchanga
curl -X POST http://localhost:8000/api/v1/panchanga/extended \
  -H "Content-Type: application/json" \
  -d "{\"birth_data\":{\"date\":\"2026-01-01\",\"time\":\"12:00:00\",\"latitude\":12.9716,\"longitude\":77.5946,\"timezone_offset\":5.5},\"ayanamsa\":\"LAHIRI\"}"
```

If these return JSON data (not 404), the API is working correctly!

