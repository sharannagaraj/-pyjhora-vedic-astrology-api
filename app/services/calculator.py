"""PyJHora calculation service"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import swisseph as swe
from jhora.panchanga import drik
from jhora.horoscope.chart import charts

# Constants
PLANET_NAMES = {
    0: "Sun", 1: "Moon", 2: "Mars", 3: "Mercury",
    4: "Jupiter", 5: "Venus", 6: "Saturn", 7: "Rahu", 8: "Ketu", 'L': "Ascendant"
}

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

CHART_FACTORS = {
    "D1": 1, "D2": 2, "D3": 3, "D4": 4, "D7": 7, "D9": 9,
    "D10": 10, "D12": 12, "D16": 16, "D20": 20, "D24": 24,
    "D27": 27, "D30": 30, "D60": 60
}

class PyJHoraCalculator:
    """PyJHora calculation wrapper"""

    def __init__(self, birth_data: Dict, ayanamsa: str = "LAHIRI"):
        """Initialize calculator with birth data"""
        self.birth_data = birth_data
        self.ayanamsa = ayanamsa

        # Parse birth date
        year, month, day = map(int, birth_data['date'].split('-'))
        self.birth_date = drik.Date(year, month, day)

        # Setup place
        place_name = birth_data.get('place_name', 'Custom Location')
        self.place = drik.Place(
            place_name,
            birth_data['latitude'],
            birth_data['longitude'],
            birth_data['timezone_offset']
        )

        # Set ayanamsa
        drik.set_ayanamsa_mode(ayanamsa)
        swe.set_sid_mode(getattr(swe, f'SIDM_{ayanamsa}', swe.SIDM_LAHIRI))

        # Calculate Julian Day
        # IMPORTANT: PyJHora expects LOCAL TIME in JD, not UT
        # PyJHora internally converts to UTC using the timezone from place
        birth_time_str = birth_data['time']
        birth_time_local = datetime.strptime(birth_time_str, "%H:%M:%S")

        # Use LOCAL time for JD calculation (PyJHora handles timezone internally)
        local_time = (birth_time_local.hour + birth_time_local.minute/60.0 +
                      birth_time_local.second/3600.0)
        self.jd = swe.julday(year, month, day, local_time)

        # For ayanamsa, we need the actual UT time
        tz_offset = timedelta(hours=birth_data['timezone_offset'])
        birth_time_utc = birth_time_local - tz_offset
        ut_time = (birth_time_utc.hour + birth_time_utc.minute/60.0 +
                   birth_time_utc.second/3600.0)
        jd_ut = swe.julday(year, month, day, ut_time)
        self.ayanamsa_value = swe.get_ayanamsa_ut(jd_ut)

    def parse_chart_data(self, chart_data: List) -> Tuple[Dict, int, float]:
        """Parse PyJHora chart data"""
        parsed = {}
        asc_sign = None
        asc_deg = None

        for item in chart_data:
            if len(item) >= 2:
                planet_id = item[0]
                position_data = item[1]

                if isinstance(position_data, (list, tuple)) and len(position_data) >= 2:
                    sign_id = position_data[0]
                    longitude = position_data[1]

                    if planet_id == 'L':
                        asc_sign = sign_id
                        asc_deg = longitude
                    else:
                        parsed[planet_id] = (sign_id, longitude)

        return parsed, asc_sign, asc_deg

    def calculate_chart(self, chart_type: str = "D1") -> Dict:
        """Calculate specified divisional chart"""
        chart_factor = CHART_FACTORS.get(chart_type.upper(), 1)

        # Get chart from PyJHora
        if chart_factor == 1:
            chart_data = charts.rasi_chart(self.jd, self.place)
        else:
            chart_data = charts.divisional_chart(
                self.jd, self.place, divisional_chart_factor=chart_factor
            )

        # Parse chart
        parsed, asc_sign, asc_deg = self.parse_chart_data(chart_data)

        # Format results
        planets_list = []
        for planet_id in range(9):
            if planet_id in parsed:
                sign_id, longitude = parsed[planet_id]
                deg = int(longitude)
                minutes = int((longitude - deg) * 60)

                # Calculate house
                house_num = ((sign_id - asc_sign) % 12) + 1 if asc_sign is not None else None

                planets_list.append({
                    "planet": PLANET_NAMES[planet_id],
                    "sign": SIGN_NAMES[sign_id],
                    "sign_id": sign_id,
                    "longitude": round(longitude, 4),
                    "degree": deg,
                    "minute": minutes,
                    "house": house_num
                })

        return {
            "status": "success",
            "chart_type": chart_type.upper(),
            "birth_data": self.birth_data,
            "ascendant": {
                "sign": SIGN_NAMES[asc_sign] if asc_sign is not None else "Unknown",
                "sign_id": asc_sign,
                "degree": round(asc_deg, 4) if asc_deg is not None else 0
            },
            "planets": planets_list,
            "calculation_info": {
                "ayanamsa": self.ayanamsa,
                "ayanamsa_value": round(self.ayanamsa_value, 4),
                "julian_day": round(self.jd, 6),
                "divisional_factor": chart_factor
            }
        }

    def calculate_dasha(self, dasha_system: str = "VIMSOTTARI") -> Dict:
        """Calculate Vimsottari Dasha periods"""
        from jhora.horoscope.dhasa.graha import vimsottari
        from datetime import date

        # Get Moon position for nakshatra
        chart_data = charts.rasi_chart(self.jd, self.place)
        parsed, _, _ = self.parse_chart_data(chart_data)

        moon_sign, moon_long_in_sign = parsed.get(1, (0, 0))  # Moon is planet 1

        # Calculate absolute longitude for nakshatra
        moon_abs_long = moon_sign * 30 + moon_long_in_sign

        # Calculate nakshatra (27 nakshatras in 360 degrees)
        nakshatra_num = int(moon_abs_long / (360/27))
        nakshatra_deg = moon_abs_long % (360/27)
        nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]

        # Get dasha data
        dasha_years = {8: 7, 3: 20, 0: 6, 1: 10, 2: 7, 7: 18, 4: 16, 6: 19, 5: 17}
        nakshatra_lords = [8, 3, 0, 1, 2, 7, 4, 6, 5] * 3
        starting_lord = nakshatra_lords[nakshatra_num]

        # Calculate elapsed years in current dasha
        elapsed_fraction = nakshatra_deg / (360/27)
        elapsed_years = dasha_years[starting_lord] * elapsed_fraction

        # Build dasha sequence
        year, month, day = map(int, self.birth_data['date'].split('-'))
        birth_date_obj = date(year, month, day)

        # Create sequence starting from birth lord
        lord_sequence = []
        found_start = False
        for i in range(2):
            for lord in [8, 3, 0, 1, 2, 7, 4, 6, 5]:
                if lord == starting_lord or found_start:
                    found_start = True
                    lord_sequence.append(lord)
        lord_sequence = lord_sequence[:9]

        # Calculate dates
        from datetime import timedelta as td
        current_date = birth_date_obj - td(days=elapsed_years * 365.25)

        maha_dasha_periods = []
        for lord in lord_sequence:
            years = dasha_years[lord]
            end_date = current_date + td(days=years * 365.25)

            maha_dasha_periods.append({
                "lord": PLANET_NAMES[lord],
                "start_date": current_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "duration_years": years
            })

            current_date = end_date

        # Find current dasha
        today = date.today()
        current_dasha = None
        for period in maha_dasha_periods:
            start = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
            if start <= today < end:
                elapsed_in_dasha = (today - start).days / 365.25
                remaining = (end - today).days / 365.25
                current_dasha = {
                    **period,
                    "elapsed_years": round(elapsed_in_dasha, 2),
                    "remaining_years": round(remaining, 2)
                }
                break

        return {
            "status": "success",
            "dasha_system": dasha_system,
            "birth_data": self.birth_data,
            "moon_nakshatra": {
                "number": nakshatra_num + 1,
                "name": nakshatra_names[nakshatra_num],
                "lord": PLANET_NAMES[starting_lord]
            },
            "current_dasha": current_dasha,
            "maha_dasha_periods": maha_dasha_periods
        }

    def calculate_house_wise(self, chart_type: str = "D1") -> Dict:
        """Calculate house-wise planetary placement"""
        chart_data = self.calculate_chart(chart_type)

        houses = {i: [] for i in range(1, 13)}
        asc_sign = chart_data["ascendant"]["sign_id"]

        for planet in chart_data["planets"]:
            house_num = planet["house"]
            if house_num:
                houses[house_num].append({
                    "planet": planet["planet"],
                    "degree": planet["degree"],
                    "minute": planet["minute"]
                })

        # Format house-wise data
        house_wise = []
        for house_num in range(1, 13):
            house_sign = SIGN_NAMES[(asc_sign + house_num - 1) % 12]
            house_wise.append({
                "house": house_num,
                "sign": house_sign,
                "planets": houses[house_num]
            })

        return {
            **chart_data,
            "house_wise_placement": house_wise
        }
