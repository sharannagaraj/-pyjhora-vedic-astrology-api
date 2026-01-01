"""Test script for Yogas and Doshas detection"""

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
print("TESTING YOGAS AND DOSHAS DETECTION")
print("="*100)
print(f"\nBirth Data:")
print(f"  Date: {birth_data['date']}")
print(f"  Time: {birth_data['time']}")
print(f"  Location: Bangalore ({birth_data['latitude']}°N, {birth_data['longitude']}°E)")

# Create calculator
calc = PyJHoraCalculator(birth_data, 'LAHIRI')

# Test Yogas
print(f"\n{'='*100}")
print("YOGAS DETECTION")
print("="*100)
yogas_result = calc.calculate_yogas()
print(f"\nTotal Yogas Found (All Charts): {yogas_result['total_yogas_all_charts']}")
print(f"D1 (Rasi Chart) Yogas: {yogas_result['d1_yogas_count']}")
print(f"Yogas in Result: {len(yogas_result['yogas'])}")
print(f"\nFirst 10 Yogas:")
print(f"{'#':<4} {'Name':<30} {'Chart':<8} {'Title':<40}")
print("-"*100)
for i, yoga in enumerate(yogas_result['yogas'][:10], 1):
    print(f"{i:<4} {yoga['name']:<30} {yoga['chart']:<8} {yoga['title']:<40}")

print(f"\n{'='*100}")
print("SAMPLE YOGA DETAILS")
print("="*100)
if yogas_result['yogas']:
    sample_yoga = yogas_result['yogas'][0]
    print(f"\nName: {sample_yoga['name']}")
    print(f"Title: {sample_yoga['title']}")
    print(f"Chart: {sample_yoga['chart']}")
    print(f"Description: {sample_yoga['description']}")
    print(f"Effect: {sample_yoga['effect']}")

# Test Doshas
print(f"\n{'='*100}")
print("DOSHAS DETECTION")
print("="*100)
doshas_result = calc.calculate_doshas()
print(f"\n{'Name':<30} {'Present':<10} Description")
print("-"*100)
for dosha in doshas_result['doshas']:
    present_str = "YES" if dosha['present'] else "NO"
    desc_short = dosha['description'][:80] + "..." if len(dosha['description']) > 80 else dosha['description']
    print(f"{dosha['name']:<30} {present_str:<10} {desc_short}")

print(f"\n{'='*100}")
print("DETAILED DOSHA INFORMATION")
print("="*100)
for dosha in doshas_result['doshas']:
    if dosha['present']:
        print(f"\n{dosha['name']}:")
        print(f"{dosha['description']}\n")

print("="*100)
print("Test completed successfully!")
print("API Endpoints:")
print("  - POST /api/v1/yogas/")
print("  - POST /api/v1/doshas/")
print("="*100)
