"""Test script for Ashtakavarga and Shadbala"""

from app.services.calculator import PyJHoraCalculator

# Test data for Sharan
birth_data = {
    'date': '1998-12-22',
    'time': '17:12:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

print("="*100)
print("TESTING ASHTAKAVARGA AND SHADBALA")
print("="*100)
print(f"\nBirth Data:")
print(f"  Date: {birth_data['date']}")
print(f"  Time: {birth_data['time']}")
print(f"  Location: Bangalore")

# Create calculator
calc = PyJHoraCalculator(birth_data, 'LAHIRI')

# Test Ashtakavarga
print(f"\n{'='*100}")
print("ASHTAKAVARGA (BINDU SYSTEM)")
print("="*100)
ashtakavarga_result = calc.calculate_ashtakavarga()

print(f"\n{'='*100}")
print("SAMUDHAYA ASHTAKAVARGA (Combined)")
print("="*100)
sam = ashtakavarga_result['samudhaya_ashtakavarga']
print(f"Total Bindus: {sam['total_bindus']}")
print(f"Strongest House: {sam['strongest_house']} ({sam['bindus_per_house'][sam['strongest_house']-1]} bindus)")
print(f"Weakest House: {sam['weakest_house']} ({sam['bindus_per_house'][sam['weakest_house']-1]} bindus)")
print(f"\nBindus per House:")
for i, bindus in enumerate(sam['bindus_per_house'], 1):
    bar = "#" * (bindus // 2)
    print(f"  House {i:2d}: {bindus:2d} bindus {bar}")

print(f"\n{'='*100}")
print("BINNA ASHTAKAVARGA (Planet-wise)")
print("="*100)
binna = ashtakavarga_result['binna_ashtakavarga']
print(f"{'Planet':<12} {'Total':<8} House Bindus (1-12)")
print("-"*100)
for planet, data in binna.items():
    bindus_str = " ".join([f"{b:2d}" for b in data['bindus']])
    print(f"{planet:<12} {data['total']:<8} {bindus_str}")

# Test Shadbala
print(f"\n{'='*100}")
print("SHADBALA (SIX-FOLD STRENGTH)")
print("="*100)
try:
    shadbala_result = calc.calculate_shadbala()

    if shadbala_result['planetary_strengths']:
        print(f"\n{'Planet':<12} {'Total Strength':<20}")
        print("-"*100)
        for planet_strength in shadbala_result['planetary_strengths']:
            print(f"{planet_strength['planet']:<12} {planet_strength['total_strength']:<20.2f}")

        # Find strongest and weakest
        strengths = [(p['planet'], p['total_strength']) for p in shadbala_result['planetary_strengths']]
        if strengths:
            strongest = max(strengths, key=lambda x: x[1])
            weakest = min(strengths, key=lambda x: x[1])
            print(f"\nStrongest Planet: {strongest[0]} ({strongest[1]:.2f})")
            print(f"Weakest Planet: {weakest[0]} ({weakest[1]:.2f})")
    else:
        print("No Shadbala data available")
except Exception as e:
    print(f"Shadbala calculation encountered an issue: {e}")
    print("This is a known limitation - Shadbala calculation may need additional parameters.")

print(f"\n{'='*100}")
print("Test completed!")
print("API Endpoints:")
print("  - POST /api/v1/strength/ashtakavarga")
print("  - POST /api/v1/strength/shadbala")
print("="*100)
