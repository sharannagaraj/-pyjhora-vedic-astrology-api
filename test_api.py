#!/usr/bin/env python3
"""Test PyJHora API endpoints"""

import requests
import json

# API Base URL - change this to your deployed URL
BASE_URL = "http://localhost:8000"

print("="*80)
print("PyJHora API Test Suite")
print("="*80 + "\n")

# Test data - Sharan's birth details
test_birth_data = {
    "date": "1998-12-22",
    "time": "17:12:00",
    "timezone_offset": 5.5,
    "latitude": 12.9716,
    "longitude": 77.5946,
    "place_name": "Bangalore, India"
}

# Test 1: Health Check
print("Test 1: Health Check")
print("-"*80)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test 2: D1 Rasi Chart
print("Test 2: D1 Rasi Chart")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/charts/rasi",
        json={"birth_data": test_birth_data, "ayanamsa": "LAHIRI"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Ascendant: {result['ascendant']['sign']} {result['ascendant']['degree']:.2f}°")
    print(f"Number of planets: {len(result['planets'])}")
    print(f"Sample planet: {result['planets'][0]}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test 3: D9 Navamsa Chart
print("Test 3: D9 Navamsa Chart")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/charts/navamsa",
        json={"birth_data": test_birth_data, "ayanamsa": "LAHIRI"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Chart Type: {result['chart_type']}")
    print(f"Ascendant: {result['ascendant']['sign']} {result['ascendant']['degree']:.2f}°\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test 4: D10 Dasamsa Chart
print("Test 4: D10 Dasamsa Chart")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/charts/dasamsa",
        json={"birth_data": test_birth_data, "ayanamsa": "LAHIRI"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Chart Type: {result['chart_type']}")
    print(f"Ascendant: {result['ascendant']['sign']} {result['ascendant']['degree']:.2f}°\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test 5: Vimsottari Dasha
print("Test 5: Vimsottari Dasha")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/dashas/vimsottari",
        json={"birth_data": test_birth_data, "ayanamsa": "LAHIRI"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Moon Nakshatra: {result['moon_nakshatra']['name']}")
    print(f"Current Dasha: {result['current_dasha']['lord']}")
    print(f"Total Maha Dashas: {len(result['maha_dasha_periods'])}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test 6: List Ayanamsa Systems
print("Test 6: List Ayanamsa Systems")
print("-"*80)
try:
    response = requests.get(f"{BASE_URL}/api/v1/ayanamsa/list")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Available Ayanamsa systems: {', '.join(result['ayanamsa_systems'])}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test 7: List Chart Types
print("Test 7: List Chart Types")
print("-"*80)
try:
    response = requests.get(f"{BASE_URL}/api/v1/charts/types")
    print(f"Status: {response.status_code}")
    result = response.json()
    print("Available Charts:")
    for chart_type, description in list(result['chart_types'].items())[:5]:
        print(f"  {chart_type}: {description}")
    print(f"  ... and {len(result['chart_types']) - 5} more\n")
except Exception as e:
    print(f"Error: {e}\n")

print("="*80)
print("All tests completed!")
print("="*80)
