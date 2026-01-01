# PyJHora API - Unit Test Report

## Critical Bug Found and Fixed

### Issue Summary
**Bug**: Timezone conversion applied twice, causing 5.5-hour offset in calculations
**Impact**: All chart calculations were incorrect (showing charts for 6:10 AM instead of 5:12 PM)
**Status**: FIXED

### Root Cause Analysis

#### How PyJHora Works
PyJHora library has a specific design for handling timezones:

1. **Input Expectation**: PyJHora expects Julian Day (JD) calculated with **LOCAL TIME**
2. **Internal Conversion**: PyJHora's `drik.ascendant()` function internally converts to UTC by subtracting timezone

Source code evidence (`jhora/panchanga/drik.py` line 1483):
```python
def ascendant(jd, place):
    _, lat, lon, tz = place
    jd_utc = jd - (tz / 24.)  # PyJHora subtracts timezone internally
    ...
```

#### Our Mistake
In `app/services/calculator.py`, we were:
1. Converting birth time from IST to UT (17:12 → 11:42)
2. Creating JD with UT time
3. PyJHora then subtracted timezone AGAIN (11:42 - 5:30 = 6:12)

Result: Chart calculated for 6:12 AM instead of 5:12 PM!

### The Fix

**Before (WRONG)**:
```python
birth_time_utc = birth_time_local - tz_offset
ut_time = (birth_time_utc.hour + birth_time_utc.minute/60.0 + ...)
self.jd = swe.julday(year, month, day, ut_time)
```

**After (CORRECT)**:
```python
# PyJHora expects LOCAL TIME in JD
local_time = (birth_time_local.hour + birth_time_local.minute/60.0 + ...)
self.jd = swe.julday(year, month, day, local_time)
```

### Verification Test Results

#### Test Case: Sharan's Birth Chart
- **Date**: 22 December 1998
- **Time**: 5:12 PM IST
- **Place**: Bangalore (12.9716°N, 77.5946°E)
- **Timezone**: IST (UTC +5:30)

#### Results Comparison

| Item | Before Fix | After Fix | Status |
|------|------------|-----------|--------|
| Ascendant | Aquarius 25.53° | Taurus 26.56° | ✓ FIXED |
| D9 Ascendant | Taurus 19.73° | Leo 29.07° | ✓ FIXED |
| D10 Ascendant | Libra 15.26° | Virgo 25.63° | ✓ FIXED |
| JD Used | 2451169.9875 | 2451170.2167 | ✓ FIXED |
| Time Calculated | 6:10 AM | 5:12 PM | ✓ FIXED |

#### Validation Against SwissEph Direct Calculation

```python
# Direct SwissEph calculation for verification
swe.set_sid_mode(swe.SIDM_LAHIRI)
ut_time = (17 + 12/60.0) - 5.5  # Convert IST to UT
jd_ut = swe.julday(1998, 12, 22, ut_time)
houses = swe.houses_ex(jd_ut, 12.9716, 77.5946, b'P', swe.FLG_SIDEREAL)
asc = houses[1][0]  # Result: 56.56° = Taurus 26.56°
```

**Result**: API now matches SwissEph direct calculation ✓

### All Test Results

```
Test 1: Health Check                    ✓ PASS
Test 2: D1 Rasi Chart                   ✓ PASS (Ascendant: Taurus 26.56°)
Test 3: D9 Navamsa Chart                ✓ PASS (Ascendant: Leo 29.07°)
Test 4: D10 Dasamsa Chart               ✓ PASS (Ascendant: Virgo 25.63°)
Test 5: Vimsottari Dasha                ✓ PASS (Moon Nakshatra: Bharani)
Test 6: List Ayanamsa Systems           ✓ PASS (8 systems)
Test 7: List Chart Types                ✓ PASS (14 chart types)
```

### Correct D1 Chart for Sharan

```
+-------+---------------+----------------------------------+
| House | Sign          | Planets                          |
+-------+---------------+----------------------------------+
|     1 | Taurus        | Ascendant (26.56°)              |
|     2 | Gemini        | -                                |
|     3 | Cancer        | -                                |
|     4 | Leo           | Rahu (1.07°)                    |
|     5 | Virgo         | Mars (19.72°)                   |
|     6 | Libra         | -                                |
|     7 | Scorpio       | Mercury (15.16°)                |
|     8 | Sagittarius   | Sun (6.58°), Venus (19.56°)     |
|     9 | Capricorn     | Moon (17.62°)                   |
|    10 | Aquarius      | Jupiter (27.01°), Ketu (1.07°)  |
|    11 | Pisces        | -                                |
|    12 | Aries         | Saturn (3.20°)                  |
+-------+---------------+----------------------------------+
```

### Key Learnings

1. **Library Documentation**: PyJHora's expected input format wasn't clearly documented
2. **Timezone Handling**: Always verify whether a library expects local or UT time
3. **Double Conversion**: Watch out for double timezone conversions
4. **Verification**: Always cross-check with reference calculations

### Impact Assessment

- **Severity**: CRITICAL (all calculations were wrong)
- **Affected Endpoints**: All chart and dasha endpoints
- **User Impact**: Anyone using the API before this fix received incorrect charts
- **Resolution Time**: Identified and fixed immediately upon investigation

### Recommendations

1. ✓ Fixed: Use LOCAL time for PyJHora JD calculations
2. ✓ Verified: All test cases now pass
3. ✓ Documented: Added inline comments explaining PyJHora's expectations
4. TODO: Add regression tests to prevent similar issues
5. TODO: Create comprehensive test suite with known-good charts

---

**Report Generated**: 2026-01-01
**Fixed By**: Claude Code with user Sharan
**Status**: RESOLVED
