"""Test script for Phase 4 features - Special Lagnas and Bhava Bala"""

from app.services.calculator import PyJHoraCalculator

birth_data = {
    'date': '1998-12-22',
    'time': '17:12:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

print("="*100)
print("TESTING PHASE 4: SPECIAL LAGNAS AND BHAVA BALA")
print("="*100)
print(f"\nBirth Data:")
print(f"  Date: {birth_data['date']}")
print(f"  Time: {birth_data['time']}")
print(f"  Location: Bangalore")

calc = PyJHoraCalculator(birth_data, 'LAHIRI')

# Test Special Lagnas
print(f"\n{'='*100}")
print("SPECIAL LAGNAS (7 Important Ascendants)")
print("="*100)

lagnas_result = calc.calculate_special_lagnas()
special_lagnas = lagnas_result['special_lagnas']

lagna_names = {
    'hora_lagna': 'Hora Lagna',
    'ghati_lagna': 'Ghati Lagna',
    'bhava_lagna': 'Bhava Lagna',
    'sree_lagna': 'Sree Lagna',
    'pranapada_lagna': 'Pranapada Lagna',
    'indu_lagna': 'Indu Lagna',
    'bhrigu_bindhu_lagna': 'Bhrigu Bindhu Lagna'
}

for key, name in lagna_names.items():
    lagna = special_lagnas[key]
    print(f"\n{name}:")
    print(f"  Sign: {lagna['sign']}")
    print(f"  Position: {lagna['degree']}° {lagna['minute']}'")
    print(f"  Longitude: {lagna['longitude']}°")
    print(f"  Purpose: {lagna['description']}")

# Test Bhava Bala
print(f"\n{'='*100}")
print("BHAVA BALA (HOUSE STRENGTH)")
print("="*100)

bhava_result = calc.calculate_bhava_bala()

print(f"\n{'House':<8} {'Sign':<15} {'Strength':<15} Bar Chart")
print("-"*100)

for house_data in bhava_result['house_strengths']:
    house_num = house_data['house']
    sign = house_data['sign']
    strength = house_data['total_strength']
    bar = "#" * int(strength / 10)
    print(f"{house_num:<8} {sign:<15} {strength:<15.2f} {bar}")

print(f"\n{'='*100}")
print("HOUSE STRENGTH SUMMARY")
print("="*100)

strongest = bhava_result['strongest_house']
weakest = bhava_result['weakest_house']

print(f"\nStrongest House: {strongest['house']} (Strength: {strongest['strength']:.2f})")
print(f"Weakest House: {weakest['house']} (Strength: {weakest['strength']:.2f})")

# House significations
house_meanings = {
    1: "Self, body, personality",
    2: "Wealth, family, speech",
    3: "Siblings, courage, communication",
    4: "Mother, home, property",
    5: "Children, education, intelligence",
    6: "Enemies, diseases, service",
    7: "Spouse, partnerships, business",
    8: "Longevity, transformation, occult",
    9: "Father, luck, religion",
    10: "Career, status, authority",
    11: "Gains, friends, aspirations",
    12: "Losses, spirituality, foreign"
}

print(f"\nStrongest House Significance: {house_meanings[strongest['house']]}")
print(f"Weakest House Significance: {house_meanings[weakest['house']]}")

print(f"\n{'='*100}")
print("INTERPRETATION")
print("="*100)
print(f"The {strongest['house']}th house is the strongest, indicating good results for:")
print(f"  - {house_meanings[strongest['house']]}")
print(f"\nThe {weakest['house']}th house is the weakest, which may show challenges in:")
print(f"  - {house_meanings[weakest['house']]}")

print(f"\n{'='*100}")
print("Test completed successfully!")
print("API Endpoints:")
print("  - POST /api/v1/special/lagnas")
print("  - POST /api/v1/special/bhava-bala")
print("="*100)
