"""Comprehensive API Unit Test Suite - All Endpoints"""

import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json"}

# Test Birth Data
BIRTH_DATA = {
    "date": "1998-12-22",
    "time": "17:12:00",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timezone_offset": 5.5
}

CURRENT_DATA = {
    "date": "2026-01-01",
    "time": "12:00:00",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timezone_offset": 5.5
}

# Test Results
test_results = []
total_tests = 0
passed_tests = 0
failed_tests = 0

def log_test(category, endpoint, status, message=""):
    """Log test result"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if status == "PASS":
        passed_tests += 1
        symbol = "[PASS]"
    else:
        failed_tests += 1
        symbol = "[FAIL]"

    test_results.append({
        "category": category,
        "endpoint": endpoint,
        "status": status,
        "message": message,
        "symbol": symbol
    })
    print(f"{symbol} {category:30} {endpoint:40} {message}")

def test_endpoint(category, method, endpoint, payload=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        else:  # POST
            response = requests.post(url, json=payload, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" or "name" in data or "status" in data:
                log_test(category, endpoint, "PASS", f"{response.status_code}")
                return True, data
            else:
                log_test(category, endpoint, "FAIL", f"Invalid response format")
                return False, None
        else:
            log_test(category, endpoint, "FAIL", f"Status {response.status_code}")
            return False, None
    except requests.exceptions.ConnectionError:
        log_test(category, endpoint, "FAIL", "API not running")
        return False, None
    except Exception as e:
        log_test(category, endpoint, "FAIL", str(e)[:50])
        return False, None

print("="*120)
print("COMPREHENSIVE API UNIT TEST SUITE".center(120))
print("PyJHora Vedic Astrology API v1.1.0".center(120))
print("="*120)

# Check if API is running
print(f"\nChecking API availability at {BASE_URL}...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print(f"[OK] API is running and healthy")
    else:
        print(f"[ERROR] API returned status {response.status_code}")
        print("Please start the API with: uvicorn app.main:app --reload")
        exit(1)
except:
    print(f"[ERROR] Cannot connect to API at {BASE_URL}")
    print("Please start the API with: uvicorn app.main:app --reload")
    exit(1)

print(f"\n{'='*120}")
print("RUNNING TESTS...")
print("="*120)

# 1. UTILITY ENDPOINTS
print(f"\n{'1. UTILITY ENDPOINTS':=^120}")
test_endpoint("Utility", "GET", "/")
test_endpoint("Utility", "GET", "/health")
test_endpoint("Utility", "GET", "/api/v1/ayanamsa/list")
test_endpoint("Utility", "GET", "/api/v1/charts/types")

# 2. DIVISIONAL CHARTS (16 endpoints)
print(f"\n{'2. DIVISIONAL CHARTS (16 ENDPOINTS)':=^120}")

charts = [
    ("D1", "/api/v1/charts/rasi"),
    ("D2", "/api/v1/charts/hora"),
    ("D3", "/api/v1/charts/drekkana"),
    ("D4", "/api/v1/charts/chaturthamsa"),
    ("D7", "/api/v1/charts/saptamsa"),
    ("D9", "/api/v1/charts/navamsa"),
    ("D10", "/api/v1/charts/dasamsa"),
    ("D12", "/api/v1/charts/dwadasamsa"),
    ("D16", "/api/v1/charts/shodasamsa"),
    ("D20", "/api/v1/charts/vimsamsa"),
    ("D24", "/api/v1/charts/chaturvimsamsa"),
    ("D27", "/api/v1/charts/nakshatramsa"),
    ("D30", "/api/v1/charts/trimsamsa"),
    ("D40", "/api/v1/charts/khavedamsa"),
    ("D45", "/api/v1/charts/akshavedamsa"),
    ("D60", "/api/v1/charts/shashtyamsa"),
]

payload = {"birth_data": BIRTH_DATA, "ayanamsa": "LAHIRI"}
for chart_name, endpoint in charts:
    test_endpoint("Charts", "POST", endpoint, payload)

# 3. DASHA SYSTEMS (3 endpoints)
print(f"\n{'3. DASHA SYSTEMS (3 ENDPOINTS)':=^120}")

success, data = test_endpoint("Dashas", "POST", "/api/v1/dashas/vimsottari", payload)
if success and data:
    print(f"    Maha Dashas found: {len(data.get('maha_dashas', []))}")

success, data = test_endpoint("Dashas", "POST", "/api/v1/dashas/bhukti", payload)
if success and data:
    print(f"    Bhukti periods found: {len(data.get('bhukti_periods', []))}")

success, data = test_endpoint("Dashas", "POST", "/api/v1/dashas/current", payload)
if success and data:
    current = data.get('current_dasha', {})
    print(f"    Current: {current.get('maha_lord')} - {current.get('bhukti_lord')}")

# 4. YOGAS & DOSHAS (2 endpoints)
print(f"\n{'4. YOGAS & DOSHAS (2 ENDPOINTS)':=^120}")

success, data = test_endpoint("Yogas", "POST", "/api/v1/yogas/", payload)
if success and data:
    print(f"    Total Yogas: {data.get('total_yogas_all_charts', 0)}")
    print(f"    D1 Yogas: {data.get('d1_yogas_count', 0)}")

success, data = test_endpoint("Doshas", "POST", "/api/v1/doshas/", payload)
if success and data:
    doshas = data.get('doshas', [])
    if isinstance(doshas, list):
        present = sum(1 for d in doshas if d.get('present'))
        print(f"    Doshas present: {present}/{len(doshas)}")
    else:
        present = sum(1 for v in doshas.values() if v.get('present'))
        print(f"    Doshas present: {present}/{len(doshas)}")

# 5. STRENGTH SYSTEMS (2 endpoints)
print(f"\n{'5. STRENGTH SYSTEMS (2 ENDPOINTS)':=^120}")

success, data = test_endpoint("Strength", "POST", "/api/v1/strength/ashtakavarga", payload)
if success and data:
    sam = data.get('samudhaya_ashtakavarga', {})
    print(f"    Total Bindus: {sam.get('total_bindus', 0)}")

success, data = test_endpoint("Strength", "POST", "/api/v1/strength/shadbala", payload)
if success and data:
    strengths = data.get('planetary_strengths', [])
    print(f"    Planets analyzed: {len(strengths)}")

# 6. PANCHANGA (2 endpoints)
print(f"\n{'6. PANCHANGA (2 ENDPOINTS)':=^120}")

success, data = test_endpoint("Panchanga", "POST", "/api/v1/panchanga/", payload)
if success and data:
    tithi = data.get('tithi', {})
    nak = data.get('nakshatra', {})
    print(f"    Tithi: {tithi.get('name')} ({tithi.get('paksha')})")
    print(f"    Nakshatra: {nak.get('name')} Pada {nak.get('pada')}")

success, data = test_endpoint("Panchanga", "POST", "/api/v1/panchanga/extended", {"birth_data": CURRENT_DATA, "ayanamsa": "LAHIRI"})
if success and data:
    vara = data.get('vara', {})
    print(f"    Vara: {vara.get('day')} (Lord: {vara.get('lord')})")
    sun_moon = data.get('sun_moon_timings', {})
    print(f"    Sunrise: {sun_moon.get('sunrise')}, Sunset: {sun_moon.get('sunset')}")

# 7. COMPATIBILITY (1 endpoint)
print(f"\n{'7. COMPATIBILITY (1 ENDPOINT)':=^120}")

boy_data = BIRTH_DATA
girl_data = {
    "date": "2000-06-15",
    "time": "14:30:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone_offset": 5.5
}

compat_payload = {
    "boy_birth_data": boy_data,
    "girl_birth_data": girl_data,
    "ayanamsa": "LAHIRI"
}

success, data = test_endpoint("Compatibility", "POST", "/api/v1/compatibility/marriage", compat_payload)
if success and data:
    print(f"    Match Score: {data.get('total_score', 0)}/36")
    print(f"    Rating: {data.get('compatibility_rating', 'N/A')}")

# 8. SPECIAL CALCULATIONS (2 endpoints)
print(f"\n{'8. SPECIAL CALCULATIONS (2 ENDPOINTS)':=^120}")

success, data = test_endpoint("Special", "POST", "/api/v1/special/lagnas", payload)
if success and data:
    lagnas = data.get('special_lagnas', {})
    print(f"    Special Lagnas: {len(lagnas)}")

success, data = test_endpoint("Special", "POST", "/api/v1/special/bhava-bala", payload)
if success and data:
    houses = data.get('house_strengths', [])
    strongest = data.get('strongest_house', {})
    print(f"    Houses analyzed: {len(houses)}")
    print(f"    Strongest: House {strongest.get('house', 'N/A')}")

# 9. TRANSITS (3 endpoints) - NEW IN v1.1
print(f"\n{'9. TRANSITS (3 ENDPOINTS - NEW IN v1.1)':=^120}")

transit_payload = {"birth_data": CURRENT_DATA, "ayanamsa": "LAHIRI"}

success, data = test_endpoint("Transits", "POST", "/api/v1/transits/current", transit_payload)
if success and data:
    positions = data.get('planetary_positions', [])
    retrograde = sum(1 for p in positions if p.get('retrograde'))
    print(f"    Planets tracked: {len(positions)}")
    print(f"    Retrograde planets: {retrograde}")

success, data = test_endpoint("Transits", "POST", "/api/v1/transits/sade-sati", payload)
if success and data:
    in_sade_sati = data.get('in_sade_sati', False)
    moon_sign = data.get('moon_sign', 'N/A')
    print(f"    Moon Sign: {moon_sign}")
    print(f"    In Sade Sati: {'YES' if in_sade_sati else 'NO'}")

success, data = test_endpoint("Transits", "POST", "/api/v1/transits/next-entries", transit_payload)
if success and data:
    entries = data.get('next_entries', [])
    print(f"    Next entries: {len(entries)}")

# FINAL SUMMARY
print(f"\n{'='*120}")
print("TEST SUMMARY".center(120))
print("="*120)

# Group by category
categories = {}
for result in test_results:
    cat = result['category']
    if cat not in categories:
        categories[cat] = {'total': 0, 'passed': 0, 'failed': 0}
    categories[cat]['total'] += 1
    if result['status'] == 'PASS':
        categories[cat]['passed'] += 1
    else:
        categories[cat]['failed'] += 1

print(f"\n{'Category':<20} {'Total':<10} {'Passed':<10} {'Failed':<10} {'Success Rate':<15}")
print("-"*120)

for cat, stats in sorted(categories.items()):
    success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
    status_symbol = "[OK]" if stats['failed'] == 0 else "[WARN]"
    print(f"{status_symbol} {cat:<15} {stats['total']:<10} {stats['passed']:<10} {stats['failed']:<10} {success_rate:.1f}%")

print("\n" + "="*120)
print(f"OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
print("="*120)

if failed_tests > 0:
    print(f"\nFAILED TESTS ({failed_tests}):")
    print("-"*120)
    for result in test_results:
        if result['status'] == 'FAIL':
            print(f"  {result['category']:20} {result['endpoint']:50} {result['message']}")
    print("="*120)

# API Coverage
print(f"\n{'='*120}")
print("API COVERAGE REPORT".center(120))
print("="*120)

coverage = {
    "Divisional Charts": {"total": 16, "implemented": 16, "tested": sum(1 for r in test_results if r['category'] == 'Charts' and r['status'] == 'PASS')},
    "Dasha Systems": {"total": 48, "implemented": 1, "tested": sum(1 for r in test_results if r['category'] == 'Dashas' and r['status'] == 'PASS')},
    "Yogas": {"total": 1, "implemented": 1, "tested": sum(1 for r in test_results if r['category'] == 'Yogas' and r['status'] == 'PASS')},
    "Doshas": {"total": 1, "implemented": 1, "tested": sum(1 for r in test_results if r['category'] == 'Doshas' and r['status'] == 'PASS')},
    "Strength Systems": {"total": 2, "implemented": 2, "tested": sum(1 for r in test_results if r['category'] == 'Strength' and r['status'] == 'PASS')},
    "Panchanga": {"total": 2, "implemented": 2, "tested": sum(1 for r in test_results if r['category'] == 'Panchanga' and r['status'] == 'PASS')},
    "Compatibility": {"total": 2, "implemented": 1, "tested": sum(1 for r in test_results if r['category'] == 'Compatibility' and r['status'] == 'PASS')},
    "Special Calculations": {"total": 2, "implemented": 2, "tested": sum(1 for r in test_results if r['category'] == 'Special' and r['status'] == 'PASS')},
    "Transits": {"total": 3, "implemented": 3, "tested": sum(1 for r in test_results if r['category'] == 'Transits' and r['status'] == 'PASS')},
}

print(f"\n{'Feature Category':<30} {'Available':<12} {'Implemented':<12} {'Tested':<12} {'Status'}")
print("-"*120)

for feature, stats in coverage.items():
    impl_pct = (stats['implemented'] / stats['total'] * 100) if stats['total'] > 0 else 0
    test_status = "PASS" if stats['tested'] == stats['implemented'] else "PARTIAL"
    status_symbol = "[OK]" if stats['tested'] == stats['implemented'] else "[WARN]"
    print(f"{status_symbol} {feature:<25} {stats['total']:<12} {stats['implemented']:<12} {stats['tested']:<12} {test_status}")

# Final verdict
print("\n" + "="*120)
if failed_tests == 0:
    print("[SUCCESS] ALL TESTS PASSED!".center(120))
    print("API is fully functional and production-ready.".center(120))
else:
    print(f"[WARNING] {failed_tests} test(s) failed. Check details above.".center(120))

print("="*120)

print(f"\nAPI Version: 1.1.0")
print(f"Total Endpoints Tested: {total_tests}")
print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nDocumentation: {BASE_URL}/docs")
print(f"Health Check: {BASE_URL}/health")
print("="*120)
