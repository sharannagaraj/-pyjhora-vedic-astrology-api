"""Comprehensive endpoint tests for PyJHora API"""
import requests
import json
from datetime import datetime

BASE_URL = "https://pyjhora-api-9bu4.onrender.com"

# Test birth data
BIRTH_DATA = {
    "date": "1993-06-08",
    "time": "01:50:00",
    "timezone_offset": 5.5,
    "latitude": 13.0827,
    "longitude": 80.2707,
    "place_name": "Chennai, India"
}

def test_wake_up():
    """Test wake-up endpoint"""
    print("\n1. Testing Wake-Up Endpoint...")
    response = requests.get(f"{BASE_URL}/wake-up")
    assert response.status_code == 200, f"Wake-up failed: {response.status_code}"
    print("   [OK] Wake-up successful")
    return True

def test_chart_endpoint(endpoint_name, endpoint_path):
    """Test a chart calculation endpoint"""
    print(f"\n2. Testing {endpoint_name}...")
    payload = {
        "birth_data": BIRTH_DATA,
        "ayanamsa": "LAHIRI"
    }
    
    response = requests.post(f"{BASE_URL}{endpoint_path}", json=payload)
    
    if response.status_code != 200:
        print(f"   [FAIL] Failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    data = response.json()
    
    # Verify response structure
    assert data.get("status") == "success", "Status not success"
    assert "planets" in data, "No planets in response"
    assert "ascendant" in data, "No ascendant in response"
    assert len(data["planets"]) == 9, f"Expected 9 planets, got {len(data['planets'])}"
    
    print(f"   [OK] {endpoint_name} working correctly")
    print(f"   - Chart Type: {data.get('chart_type', 'N/A')}")
    print(f"   - Ascendant: {data['ascendant']['sign']} {data['ascendant']['degree']:.2f}°")
    print(f"   - Planets: {len(data['planets'])}")
    
    # Print planet summary
    for planet in data["planets"][:3]:  # Show first 3 planets
        house_info = f"House {planet.get('house', 'N/A')}" if planet.get('house') else ""
        print(f"     {planet['planet']}: {planet['sign']} {planet['degree']}°{planet['minute']}' {house_info}")
    
    return True

def test_bhava_chalit():
    """Test Bhava Chalit endpoint"""
    print(f"\n3. Testing Bhava Chalit Chart...")
    payload = {
        "birth_data": BIRTH_DATA,
        "ayanamsa": "LAHIRI"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/charts/bhava-chalit", json=payload)
    
    if response.status_code != 200:
        print(f"   [FAIL] Failed: {response.status_code}")
        return False
    
    data = response.json()
    
    assert data.get("status") == "success"
    assert "house_cusps" in data
    assert "planets" in data
    assert len(data["house_cusps"]) == 12
    
    print(f"   [OK] Bhava Chalit working correctly")
    print(f"   - House Cusps: {len(data['house_cusps'])}")
    print(f"   - Method: {data['calculation_info'].get('bhava_method', 'N/A')}")
    
    # Show houses with planets
    for house in data["house_cusps"][:3]:
        planets_str = ", ".join([p["planet"] for p in house["planets"]]) if house["planets"] else "Empty"
        print(f"     House {house['house']}: {house['cusp_sign']} {house['cusp_degree']:.2f}° - Planets: {planets_str}")
    
    return True

def test_dasha_endpoint(endpoint_name, endpoint_path):
    """Test a dasha calculation endpoint"""
    print(f"\n4. Testing {endpoint_name}...")
    payload = {
        "birth_data": BIRTH_DATA,
        "ayanamsa": "LAHIRI",
        "dasha_system": "VIMSOTTARI"
    }
    
    response = requests.post(f"{BASE_URL}{endpoint_path}", json=payload)
    
    if response.status_code != 200:
        print(f"   [FAIL] Failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    data = response.json()
    
    assert data.get("status") == "success"
    assert "moon_nakshatra" in data, "No moon nakshatra in response"
    
    print(f"   [OK] {endpoint_name} working correctly")
    print(f"   - Moon Nakshatra: {data['moon_nakshatra']['name']} (Lord: {data['moon_nakshatra']['lord']})")
    
    if "current_dasha" in data:
        cd = data["current_dasha"]
        print(f"   - Current Maha Dasha: {cd.get('lord', 'N/A')}")
        print(f"   - Period: {cd.get('start_date', 'N/A')} to {cd.get('end_date', 'N/A')}")
    
    if "current_bhukti" in data:
        cb = data["current_bhukti"]
        print(f"   - Current Bhukti: {cb['maha_dasha_lord']}/{cb['bhukti_lord']}")
        print(f"   - Remaining: {cb['remaining_months']:.2f} months")
    
    return True

def run_all_tests():
    """Run all endpoint tests"""
    print("=" * 60)
    print("PYJHORA API COMPREHENSIVE ENDPOINT TEST")
    print("=" * 60)
    
    results = {}
    
    # Test wake-up
    results["Wake-Up"] = test_wake_up()
    
    # Wait a bit for service to fully wake
    import time
    print("\nWaiting for service to fully initialize...")
    time.sleep(3)
    
    # Test chart endpoints
    chart_tests = [
        ("D1 Rasi Chart", "/api/v1/charts/rasi"),
        ("D2 Hora Chart", "/api/v1/charts/hora"),
        ("D3 Drekkana Chart", "/api/v1/charts/drekkana"),
        ("D9 Navamsa Chart", "/api/v1/charts/navamsa"),
        ("D10 Dasamsa Chart", "/api/v1/charts/dasamsa"),
    ]
    
    for name, path in chart_tests:
        try:
            results[name] = test_chart_endpoint(name, path)
        except Exception as e:
            print(f"   [FAIL] Error: {str(e)}")
            results[name] = False
    
    # Test Bhava Chalit
    try:
        results["Bhava Chalit"] = test_bhava_chalit()
    except Exception as e:
        print(f"   [FAIL] Error: {str(e)}")
        results["Bhava Chalit"] = False
    
    # Test dasha endpoints
    dasha_tests = [
        ("Vimsottari Dasha", "/api/v1/dashas/vimsottari"),
        ("Vimsottari Bhukti", "/api/v1/dashas/bhukti"),
    ]
    
    for name, path in dasha_tests:
        try:
            results[name] = test_dasha_endpoint(name, path)
        except Exception as e:
            print(f"   [FAIL] Error: {str(e)}")
            results[name] = False
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[OK] PASS" if result else "[FAIL] FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! API is working correctly.")
    else:
        print(f"\n[WARNING]  {total - passed} test(s) failed. Please review.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
