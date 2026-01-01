"""Test script to demonstrate Bhukti (sub-period) calculations"""

from app.services.calculator import PyJHoraCalculator
import json

# Test data for Sharan
birth_data = {
    'date': '1998-12-22',
    'time': '17:12:00',
    'latitude': 12.9716,
    'longitude': 77.5946,
    'timezone_offset': 5.5
}

print("="*80)
print("Testing Vimsottari Dasha with Bhukti (Sub-periods)")
print("="*80)
print(f"\nBirth Data:")
print(f"  Date: {birth_data['date']}")
print(f"  Time: {birth_data['time']}")
print(f"  Location: {birth_data['latitude']}°N, {birth_data['longitude']}°E")
print(f"  Timezone: IST (UTC +{birth_data['timezone_offset']})")

# Create calculator
calc = PyJHoraCalculator(birth_data, 'LAHIRI')

# Calculate Bhukti periods
result = calc.calculate_dasha_bhukti('VIMSOTTARI')

print(f"\n{'='*80}")
print("MOON NAKSHATRA")
print("="*80)
nak = result['moon_nakshatra']
print(f"Nakshatra #{nak['number']}: {nak['name']}")
print(f"Nakshatra Lord: {nak['lord']}")

print(f"\n{'='*80}")
print("CURRENT BHUKTI (Sub-Period)")
print("="*80)
if result.get('current_bhukti'):
    cb = result['current_bhukti']
    print(f"Maha Dasha: {cb['maha_dasha_lord']}")
    print(f"Bhukti (Antara Dasha): {cb['bhukti_lord']}")
    print(f"Start Date: {cb['start_date']}")
    print(f"End Date: {cb['end_date']}")
    print(f"Total Duration: {cb['duration_months']} months")
    print(f"Elapsed: {cb['elapsed_months']} months")
    print(f"Remaining: {cb['remaining_months']} months")
else:
    print("No current Bhukti found")

print(f"\n{'='*80}")
print(f"ALL BHUKTI PERIODS (Total: {len(result['bhukti_periods'])})")
print("="*80)
print("\nShowing first 20 periods:")
print(f"{'#':<4} {'Maha Dasha':<10} {'Bhukti':<10} {'Start Date':<20}")
print("-"*80)

for i, period in enumerate(result['bhukti_periods'][:20], 1):
    print(f"{i:<4} {period['maha_dasha_lord']:<10} {period['bhukti_lord']:<10} {period['start_date']:<20}")

print("\n" + "="*80)
print("Bhukti calculation completed successfully!")
print("API endpoint: POST /api/v1/dashas/bhukti")
print("="*80)
