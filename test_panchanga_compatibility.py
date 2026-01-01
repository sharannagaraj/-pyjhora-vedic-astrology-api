"""Test script for Panchanga and Marriage Compatibility"""

from app.services.calculator import PyJHoraCalculator

print("="*100)
print("TESTING PANCHANGA AND MARRIAGE COMPATIBILITY")
print("="*100)

# Test Panchanga
print("\n" + "="*100)
print("PANCHANGA TEST")
print("="*100)

birth_data = {
    'date': '1998-12-22',
    'time': '17:12:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

print(f"\nBirth Data:")
print(f"  Date: {birth_data['date']}")
print(f"  Time: {birth_data['time']}")
print(f"  Location: Bangalore")

calc = PyJHoraCalculator(birth_data, 'LAHIRI')
panchanga_result = calc.calculate_panchanga()

print(f"\n{'='*100}")
print("PANCHANGA DETAILS")
print("="*100)

print(f"\n1. TITHI (Lunar Day)")
tithi = panchanga_result['tithi']
print(f"   Number: {tithi['number']}")
print(f"   Name: {tithi['name']}")
print(f"   Paksha: {tithi['paksha']} (Lunar Fortnight)")
print(f"   Elapsed: {tithi['elapsed_fraction']}%")

print(f"\n2. NAKSHATRA (Lunar Mansion)")
nak = panchanga_result['nakshatra']
print(f"   Number: {nak['number']}/27")
print(f"   Name: {nak['name']}")
print(f"   Pada: {nak['pada']}/4")
print(f"   Elapsed: {nak['elapsed_fraction']}%")

print(f"\n3. YOGA")
yoga = panchanga_result['yoga']
print(f"   Number: {yoga['number']}/27")
print(f"   Name: {yoga['name']}")
print(f"   Elapsed: {yoga['elapsed_fraction']}%")

print(f"\n4. KARANA (Half Tithi)")
karana = panchanga_result['karana']
print(f"   Number: {karana['number']}")
print(f"   Name: {karana['name']}")
print(f"   Elapsed: {karana['elapsed_fraction']}%")

# Test Marriage Compatibility
print(f"\n{'='*100}")
print("MARRIAGE COMPATIBILITY TEST (ASHTAKOOTA)")
print("="*100)

# Boy's data (Sharan)
boy_data = {
    'date': '1998-12-22',
    'time': '17:12:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

# Girl's data (sample)
girl_data = {
    'date': '2000-06-15',
    'time': '14:30:00',
    'latitude': 13.0827,
    'longitude': 80.2707,
    'timezone_offset': 5.5
}

print(f"\nBoy's Birth Data:")
print(f"  Date: {boy_data['date']}")
print(f"  Time: {boy_data['time']}")
print(f"  Location: Bangalore")

print(f"\nGirl's Birth Data:")
print(f"  Date: {girl_data['date']}")
print(f"  Time: {girl_data['time']}")
print(f"  Location: Chennai")

compatibility_result = PyJHoraCalculator.calculate_marriage_compatibility(
    boy_data, girl_data, 'LAHIRI'
)

print(f"\n{'='*100}")
print("NAKSHATRA DETAILS")
print("="*100)
print(f"Boy's Nakshatra: {compatibility_result['boy']['nakshatra']} (Pada {compatibility_result['boy']['nakshatra_pada']})")
print(f"Girl's Nakshatra: {compatibility_result['girl']['nakshatra']} (Pada {compatibility_result['girl']['nakshatra_pada']})")

print(f"\n{'='*100}")
print("ASHTAKOOTA SCORES (8 KOOTAS)")
print("="*100)
scores = compatibility_result['ashtakoota_scores']

koota_names = {
    'varna': 'Varna (Spiritual Compatibility)',
    'vasiya': 'Vasiya (Mutual Attraction)',
    'tara': 'Tara (Destiny)',
    'yoni': 'Yoni (Sexual Compatibility)',
    'graha_maitri': 'Graha Maitri (Mental Compatibility)',
    'gana': 'Gana (Temperament)',
    'rasi': 'Rasi/Bhakoot (Love & Prosperity)',
    'nadi': 'Nadi (Health & Progeny - Most Important)'
}

for key, name in koota_names.items():
    score_data = scores[key]
    score = score_data['score']
    max_score = score_data['max']
    percentage = (score / max_score * 100) if max_score > 0 else 0
    bar = "#" * int(percentage // 10)
    print(f"{name:50} {score}/{max_score} {bar}")

print(f"\n{'='*100}")
print("OVERALL COMPATIBILITY")
print("="*100)
print(f"Total Score: {compatibility_result['total_score']}/36")
print(f"Percentage: {compatibility_result['percentage']}%")
print(f"Rating: {compatibility_result['compatibility_rating']}")
print(f"\nRecommendation: {compatibility_result['recommendation']}")

# Special notes
if scores['nadi']['score'] == 0:
    print(f"\nWARNING: Nadi Dosha is present (0/8 score)!")
    print("This is considered highly inauspicious and may indicate health/progeny issues.")
    print("Consult an astrologer for remedies.")

print(f"\n{'='*100}")
print("Test completed!")
print("API Endpoints:")
print("  - POST /api/v1/panchanga/")
print("  - POST /api/v1/compatibility/marriage")
print("="*100)
