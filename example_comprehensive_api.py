"""
Example script demonstrating the Comprehensive API Endpoint
Returns all astrology data in a single API call
"""

import requests
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8002"
ENDPOINT = "/api/v1/comprehensive/full-analysis"

def get_comprehensive_analysis(date, time, latitude, longitude, timezone_offset, place_name, ayanamsa="LAHIRI"):
    """
    Get complete Vedic astrology analysis in one API call

    Args:
        date: Birth date in YYYY-MM-DD format
        time: Birth time in HH:MM:SS format
        latitude: Latitude (North +ve, South -ve)
        longitude: Longitude (East +ve, West -ve)
        timezone_offset: UTC offset in hours
        place_name: Place name for reference
        ayanamsa: Ayanamsa system (default: LAHIRI)

    Returns:
        dict: Complete astrology analysis
    """

    payload = {
        "birth_data": {
            "date": date,
            "time": time,
            "latitude": latitude,
            "longitude": longitude,
            "timezone_offset": timezone_offset,
            "place_name": place_name
        },
        "ayanamsa": ayanamsa
    }

    url = f"{API_BASE_URL}{ENDPOINT}"

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None


def display_analysis(data):
    """Display comprehensive analysis in readable format"""

    if not data:
        print("No data received")
        return

    print("=" * 80)
    print("COMPREHENSIVE VEDIC ASTROLOGY ANALYSIS")
    print("=" * 80)
    print()

    # Birth Data
    birth_data = data.get('birth_data', {})
    print(f"Birth Date: {birth_data.get('date')}")
    print(f"Birth Time: {birth_data.get('time')}")
    print(f"Place: {birth_data.get('place_name')}")
    print(f"Ayanamsa: {data.get('ayanamsa')}")
    print()

    # Summary
    summary = data.get('summary', {})
    print("QUICK SUMMARY:")
    print(f"  Charts: {', '.join(summary.get('charts_calculated', []))}")
    print(f"  Current Maha Dasha: {summary.get('current_maha_dasha')}")
    print(f"  Strongest Planet (Ashtakavarga): {summary.get('strongest_planet_ashtakavarga')}")
    print(f"  Yogas Present: {summary.get('yogas_present')}")
    print(f"  Doshas Present: {summary.get('doshas_present')}")
    print()

    # D1 Chart
    charts = data.get('charts', {})
    if 'd1_rasi' in charts:
        d1 = charts['d1_rasi']
        print(f"{d1['name']}:")
        print(f"  Ascendant: {d1['ascendant']['sign']} {d1['ascendant']['degree']:.2f}°")
        print("  Planetary Positions:")
        for planet in d1['planets']:
            retro = " (R)" if planet.get('retrograde') else ""
            print(f"    {planet['planet']:10s}: {planet['sign']:12s} {planet['degree']:6.2f}° (House {planet['house']}){retro}")
        print()

    # Current Dasha
    dashas = data.get('dashas', {})
    if 'maha_dasha' in dashas:
        maha = dashas['maha_dasha']
        if 'current_period' in maha and maha['current_period']:
            cp = maha['current_period']
            print("CURRENT MAHA DASHA:")
            print(f"  Planet: {cp['lord']}")
            print(f"  Period: {cp['start_date']} to {cp['end_date']}")
            print(f"  Elapsed: {cp['elapsed_years']:.2f} years")
            print(f"  Remaining: {cp['remaining_years']:.2f} years")
            print()

    # Ashtakavarga Summary
    ashtaka = data.get('ashtakavarga', {})
    if 'bhinna_ashtakavarga' in ashtaka:
        bhinna = ashtaka['bhinna_ashtakavarga'].get('planets', {})
        print("ASHTAKAVARGA (Planet Strengths):")
        for planet, pdata in sorted(bhinna.items(), key=lambda x: x[1].get('total', 0), reverse=True):
            print(f"  {planet:10s}: {pdata.get('total', 0):3d} bindus")
        print()

    if 'sarvashtakavarga' in ashtaka:
        sarva = ashtaka['sarvashtakavarga'].get('data', {})
        print("SARVASHTAKAVARGA (House Strengths):")
        print(f"  Total Bindus: {sarva.get('total_bindus', 0)}")
        print(f"  Strongest House: {sarva.get('strongest_house', 'N/A')}")
        print(f"  Weakest House: {sarva.get('weakest_house', 'N/A')}")
        print()

    # Yogas
    yogas_data = data.get('yogas', {})
    if yogas_data.get('present_yogas'):
        print("PRESENT YOGAS:")
        for yoga in yogas_data['present_yogas']:
            print(f"  - {yoga['name']}")
            if yoga.get('description'):
                desc = yoga['description'][:100] + "..." if len(yoga['description']) > 100 else yoga['description']
                print(f"    {desc}")
        print()
    else:
        print("YOGAS: No major yogas detected")
        print()

    # Doshas
    doshas_data = data.get('doshas', {})
    if doshas_data.get('present_doshas'):
        print("PRESENT DOSHAS:")
        for dosha in doshas_data['present_doshas']:
            print(f"  - {dosha['name']}")
            if dosha.get('severity'):
                print(f"    Severity: {dosha['severity']}")
            if dosha.get('description'):
                desc = dosha['description'][:100] + "..." if len(dosha['description']) > 100 else dosha['description']
                print(f"    {desc}")
        print()
    else:
        print("DOSHAS: No major doshas detected")
        print()

    print("=" * 80)


# Example usage
if __name__ == "__main__":
    # Example: Birth data for testing
    birth_date = "1998-12-22"
    birth_time = "17:12:00"
    latitude = 12.9716
    longitude = 77.5946
    timezone = 5.5
    place = "Bangalore, India"

    print("Fetching comprehensive astrology analysis...")
    print()

    # Get analysis
    data = get_comprehensive_analysis(
        date=birth_date,
        time=birth_time,
        latitude=latitude,
        longitude=longitude,
        timezone_offset=timezone,
        place_name=place,
        ayanamsa="LAHIRI"
    )

    # Display results
    if data:
        display_analysis(data)

        # Save to file
        filename = f"astrology_analysis_{birth_date.replace('-', '')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Full data saved to: {filename}")
        print(f"Response size: {len(json.dumps(data)):,} bytes")
    else:
        print("Failed to fetch analysis")
