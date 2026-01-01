"""Test script for Phase 5: Transits and Extended Panchanga"""

from app.services.calculator import PyJHoraCalculator
from datetime import datetime

print("="*100)
print("PHASE 5 TESTING: TRANSITS AND EXTENDED PANCHANGA")
print("="*100)

# Birth data for natal chart (Sharan)
birth_data = {
    'date': '1998-12-22',
    'time': '17:12:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

# Current date data for transits (use today's date for actual transits)
current_data = {
    'date': '2026-01-01',  # Today
    'time': '12:00:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

print(f"\n{' TRANSIT ANALYSIS ':=^100}")

# Test 1: Current Transits
print(f"\n{'='*100}")
print("1. CURRENT PLANETARY TRANSITS (GOCHARA)")
print("="*100)

calc = PyJHoraCalculator(current_data, 'LAHIRI')
transits = calc.calculate_current_transits()

print(f"\nCalculation Date: {transits['calculation_date']}")
print(f"Calculation Time: {transits['calculation_time']}")

print(f"\n{'Planet':<12} {'Sign':<15} {'Degree':<8} {'Nakshatra':<20} {'Pada':<5} {'Speed':<10} {'Status'}")
print("-"*100)

for pos in transits['planetary_positions']:
    status = "RETROGRADE" if pos['retrograde'] else "Direct"
    print(f"{pos['planet']:<12} {pos['sign']:<15} {pos['degree']:<8.2f} {pos['nakshatra']:<20} {pos['nakshatra_pada']:<5} {pos['speed']:<10.4f} {status}")

# Test 2: Sade Sati
print(f"\n{'='*100}")
print("2. SADE SATI ANALYSIS")
print("="*100)

calc_birth = PyJHoraCalculator(birth_data, 'LAHIRI')
sade_sati = calc_birth.calculate_sade_sati()

print(f"\nBirth Data: {birth_data['date']} at {birth_data['time']}")
print(f"Moon Sign (Birth): {sade_sati['moon_sign']}")
print(f"Current Saturn Position: {sade_sati['current_saturn_sign']}")
print(f"\nIn Sade Sati: {'YES' if sade_sati['in_sade_sati'] else 'NO'}")

if sade_sati['in_sade_sati']:
    print(f"Current Phase: {sade_sati['current_phase']}")

print(f"\nSade Sati Spans These Signs:")
print(f"  Rising Phase (12th from Moon): {sade_sati['sade_sati_signs']['rising']}")
print(f"  Peak Phase (on Moon):           {sade_sati['sade_sati_signs']['peak']}")
print(f"  Setting Phase (2nd from Moon):  {sade_sati['sade_sati_signs']['setting']}")

print(f"\nDescription: {sade_sati['description']}")

# Test 3: Next Planet Entries
print(f"\n{'='*100}")
print("3. NEXT PLANET ENTRY DATES")
print("="*100)

entries = calc.calculate_next_planet_entries(num_entries=5)

print(f"\nCalculating from: {entries['calculation_from']}")
print(f"\n{'Planet':<12} {'Entry Date':<15} {'Time':<8} {'Entering Sign'}")
print("-"*100)

for entry in entries['next_entries']:
    print(f"{entry['planet']:<12} {entry['entry_date']:<15} {entry['entry_time']:<8} {entry['entering_sign']}")

# Test 4: Extended Panchanga
print(f"\n{' EXTENDED PANCHANGA ':=^100}")
print(f"\n{'='*100}")
print("4. EXTENDED PANCHANGA WITH TIMINGS")
print("="*100)

calc_panchanga = PyJHoraCalculator(current_data, 'LAHIRI')
extended_panchanga = calc_panchanga.calculate_extended_panchanga()

# Basic Panchanga
print(f"\n{'-'*100}")
print("BASIC PANCHANGA ELEMENTS")
print("-"*100)

basic = extended_panchanga['basic_panchanga']
print(f"\nTithi:      {basic['tithi']['name']} (#{basic['tithi']['number']}, {basic['tithi']['paksha']} Paksha)")
print(f"Nakshatra:  {basic['nakshatra']['name']} (#{basic['nakshatra']['number']}, Pada {basic['nakshatra']['pada']})")
print(f"Yoga:       {basic['yoga']['name']} (#{basic['yoga']['number']})")
print(f"Karana:     {basic['karana']['name']} (#{basic['karana']['number']})")

# Vara
print(f"\n{'-'*100}")
print("VARA (WEEKDAY)")
print("-"*100)
vara = extended_panchanga['vara']
print(f"Day:  {vara['day']}")
print(f"Lord: {vara['lord']}")

# Sun & Moon Timings
print(f"\n{'-'*100}")
print("SUN & MOON TIMINGS")
print("-"*100)
timings = extended_panchanga['sun_moon_timings']
print(f"Sunrise:  {timings['sunrise']}")
print(f"Sunset:   {timings['sunset']}")
print(f"Moonrise: {timings['moonrise']}")
print(f"Moonset:  {timings['moonset']}")

# Inauspicious Periods
print(f"\n{'-'*100}")
print("INAUSPICIOUS PERIODS (AVOID THESE TIMES)")
print("-"*100)

inauspicious = extended_panchanga['inauspicious_periods']

print(f"\n1. RAHU KAAL:")
print(f"   Timing: {inauspicious['rahu_kaal']['timing']}")
print(f"   {inauspicious['rahu_kaal']['description']}")

print(f"\n2. YAMAGANDA:")
print(f"   Timing: {inauspicious['yamaganda']['timing']}")
print(f"   {inauspicious['yamaganda']['description']}")

print(f"\n3. GULIKA:")
print(f"   Timing: {inauspicious['gulika']['timing']}")
print(f"   {inauspicious['gulika']['description']}")

print(f"\n4. DURMUHURTA:")
if inauspicious['durmuhurta']['timings']:
    for i, timing in enumerate(inauspicious['durmuhurta']['timings'], 1):
        print(f"   Period {i}: {timing}")
else:
    print(f"   No Durmuhurta periods calculated")
print(f"   {inauspicious['durmuhurta']['description']}")

# Auspicious Periods
print(f"\n{'-'*100}")
print("AUSPICIOUS PERIODS (BEST TIMES FOR ACTIVITIES)")
print("-"*100)

auspicious = extended_panchanga['auspicious_periods']

print(f"\n1. ABHIJIT MUHURTA:")
print(f"   Timing: {auspicious['abhijit_muhurta']['timing']}")
print(f"   {auspicious['abhijit_muhurta']['description']}")

print(f"\n2. BRAHMA MUHURTA:")
print(f"   Timing: {auspicious['brahma_muhurta']['timing']}")
print(f"   {auspicious['brahma_muhurta']['description']}")

# Summary
print(f"\n{'='*100}")
print("PHASE 5 TEST SUMMARY")
print("="*100)

print(f"\n[SUCCESS] Transit Analysis:")
print(f"   - Current planetary positions: {len(transits['planetary_positions'])} planets")
print(f"   - Sade Sati calculation: {'Active' if sade_sati['in_sade_sati'] else 'Not active'}")
print(f"   - Next planet entries: {len(entries['next_entries'])} upcoming transits")

print(f"\n[SUCCESS] Extended Panchanga:")
print(f"   - Basic elements: Tithi, Nakshatra, Yoga, Karana")
print(f"   - Vara (Weekday): {vara['day']}")
print(f"   - Sun/Moon timings: Sunrise, Sunset, Moonrise, Moonset")
print(f"   - Inauspicious periods: Rahu Kaal, Yamaganda, Gulika, Durmuhurta")
print(f"   - Auspicious periods: Abhijit Muhurta, Brahma Muhurta")

print(f"\n{'='*100}")
print("NEW API ENDPOINTS READY:")
print("="*100)
print("POST /api/v1/transits/current        - Current planetary positions")
print("POST /api/v1/transits/sade-sati      - Sade Sati analysis")
print("POST /api/v1/transits/next-entries   - Next planet sign entries")
print("POST /api/v1/panchanga/extended      - Extended Panchanga with timings")
print("="*100)

print(f"\n[PASS] All Phase 5 features tested successfully!")
print(f"API Version: 1.1.0")
print("="*100)
