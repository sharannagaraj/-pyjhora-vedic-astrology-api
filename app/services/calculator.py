"""PyJHora calculation service"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import swisseph as swe
from jhora.panchanga import drik
from jhora.horoscope.chart import charts
from jhora.horoscope.dhasa.graha import vimsottari
from jhora.horoscope.chart import yoga, dosha, ashtakavarga, strength
from jhora.horoscope.match import compatibility
from jhora import utils

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

    def calculate_dasha_bhukti(self, dasha_system: str = "VIMSOTTARI") -> Dict:
        """Calculate Dasha periods with Bhukti (sub-periods)"""
        if dasha_system != "VIMSOTTARI":
            raise ValueError("Only VIMSOTTARI dasha system is currently supported")

        # Get Moon nakshatra for basic info
        chart_data = charts.rasi_chart(self.jd, self.place)
        parsed, _, _ = self.parse_chart_data(chart_data)
        moon_sign, moon_long_in_sign = parsed.get(1, (0, 0))
        moon_abs_long = moon_sign * 30 + moon_long_in_sign
        nakshatra_num = int(moon_abs_long / (360/27))
        nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]
        nakshatra_lords = [8, 3, 0, 1, 2, 7, 4, 6, 5] * 3
        starting_lord = nakshatra_lords[nakshatra_num]

        # Get Bhukti periods from PyJHora
        current_period, all_periods = vimsottari.get_vimsottari_dhasa_bhukthi(self.jd, self.place)

        # Parse Bhukti periods
        bhukti_periods = []
        for period in all_periods:
            maha_lord_id = period[0]
            bhukti_lord_id = period[1]
            date_str = period[2]

            bhukti_periods.append({
                "maha_dasha_lord": PLANET_NAMES[maha_lord_id],
                "bhukti_lord": PLANET_NAMES[bhukti_lord_id],
                "start_date": date_str
            })

        # Find current Bhukti
        from datetime import date
        today = date.today()
        current_bhukti = None

        for i in range(len(bhukti_periods) - 1):
            start_date = datetime.strptime(bhukti_periods[i]['start_date'], '%Y-%m-%d %H:%M:%S').date()
            end_date = datetime.strptime(bhukti_periods[i+1]['start_date'], '%Y-%m-%d %H:%M:%S').date()

            if start_date <= today < end_date:
                duration_days = (end_date - start_date).days
                elapsed_days = (today - start_date).days
                remaining_days = (end_date - today).days

                current_bhukti = {
                    "maha_dasha_lord": bhukti_periods[i]['maha_dasha_lord'],
                    "bhukti_lord": bhukti_periods[i]['bhukti_lord'],
                    "start_date": start_date.strftime('%Y-%m-%d'),
                    "end_date": end_date.strftime('%Y-%m-%d'),
                    "duration_months": round(duration_days / 30.44, 2),
                    "elapsed_months": round(elapsed_days / 30.44, 2),
                    "remaining_months": round(remaining_days / 30.44, 2)
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
            "current_bhukti": current_bhukti,
            "bhukti_periods": bhukti_periods
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

    def calculate_yogas(self) -> Dict:
        """Calculate all Yogas present in the chart"""
        # Get yoga details for all divisional charts
        # Returns: (all_yogas_dict, d1_count, total_count)
        all_yogas_dict, d1_count, total_count = yoga.get_yoga_details_for_all_charts(self.jd, self.place)

        # Format the results
        yogas_found = []
        for yoga_name, yoga_info in all_yogas_dict.items():
            if isinstance(yoga_info, list) and len(yoga_info) >= 4:
                yogas_found.append({
                    "name": yoga_name,
                    "chart": yoga_info[0],
                    "title": yoga_info[1],
                    "description": yoga_info[2],
                    "effect": yoga_info[3]
                })

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "total_yogas_all_charts": total_count,
            "d1_yogas_count": d1_count,
            "yogas": yogas_found
        }

    def calculate_doshas(self) -> Dict:
        """Calculate all Doshas present in the chart"""
        # Get dosha details
        dosha_details = dosha.get_dosha_details(self.jd, self.place)

        # Parse the HTML results to extract information
        doshas_found = []
        for dosha_name, dosha_html in dosha_details.items():
            # Remove HTML tags for cleaner output
            import re
            clean_text = re.sub('<[^<]+?>', '', dosha_html)
            clean_text = clean_text.replace('\n', ' ').strip()

            # Determine if dosha is present
            is_present = "no " not in clean_text.lower()[:50]

            doshas_found.append({
                "name": dosha_name,
                "present": is_present,
                "description": clean_text
            })

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "doshas": doshas_found
        }

    def calculate_ashtakavarga(self) -> Dict:
        """Calculate Ashtakavarga (Bindus in each house for each planet)"""
        # Get chart data
        chart_data = charts.rasi_chart(self.jd, self.place)
        house_to_planet_list = utils.get_house_planet_list_from_planet_positions(chart_data)

        # Calculate Ashtakavarga
        binna, samudhaya, prastara = ashtakavarga.get_ashtaka_varga(house_to_planet_list)

        # Format Binna Ashtakavarga (planet-wise)
        planet_names_av = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]
        binna_formatted = {}
        for i, planet_name in enumerate(planet_names_av):
            binna_formatted[planet_name] = {
                "bindus": binna[i],
                "total": sum(binna[i])
            }

        # Format Samudhaya (combined)
        samudhaya_formatted = {
            "bindus_per_house": samudhaya,
            "total_bindus": sum(samudhaya),
            "strongest_house": samudhaya.index(max(samudhaya)) + 1,
            "weakest_house": samudhaya.index(min(samudhaya)) + 1
        }

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "binna_ashtakavarga": binna_formatted,
            "samudhaya_ashtakavarga": samudhaya_formatted
        }

    def calculate_shadbala(self) -> Dict:
        """Calculate Shadbala (Six-fold Planetary Strength)"""
        # Calculate Shadbala
        shad_bala_values = strength.shad_bala(self.jd, self.place)

        # Format the results
        planet_strengths = []
        for i, planet_name in enumerate(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]):
            if i < len(shad_bala_values):
                strength_data = shad_bala_values[i]
                if isinstance(strength_data, (list, tuple)) and len(strength_data) > 0:
                    total_strength = strength_data[0] if isinstance(strength_data[0], (int, float)) else 0
                    planet_strengths.append({
                        "planet": planet_name,
                        "total_strength": round(total_strength, 2),
                        "strength_details": strength_data[1:] if len(strength_data) > 1 else []
                    })

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "planetary_strengths": planet_strengths
        }

    def calculate_panchanga(self) -> Dict:
        """Calculate Panchanga (5 limbs of time)"""
        # Calculate all Panchanga elements
        tithi_result = drik.tithi(self.jd, self.place)
        nakshatra_result = drik.nakshatra(self.jd, self.place)
        yoga_result = drik.yogam(self.jd, self.place)
        karana_result = drik.karana(self.jd, self.place)

        # Tithi names
        tithi_names = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
        ]

        # Nakshatra names
        nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]

        # Yoga names
        yoga_names = [
            "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
            "Sukarman", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva",
            "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
            "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
            "Brahma", "Indra", "Vaidhriti"
        ]

        # Karana names
        karana_names = [
            "Kimstughna", "Bava", "Balava", "Kaulava", "Taitila",
            "Garija", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga"
        ]

        # Format results
        tithi_num = int(tithi_result[0])
        paksha = "Shukla" if tithi_num <= 15 else "Krishna"
        tithi_index = (tithi_num - 1) % 15

        nakshatra_num = int(nakshatra_result[0])
        nakshatra_pada = int(nakshatra_result[1])

        yoga_num = int(yoga_result[0])
        karana_num = int(karana_result[0])

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "tithi": {
                "number": tithi_num,
                "name": tithi_names[tithi_index],
                "paksha": paksha,
                "elapsed_fraction": round(tithi_result[1], 2)
            },
            "nakshatra": {
                "number": nakshatra_num,
                "name": nakshatra_names[nakshatra_num - 1],
                "pada": nakshatra_pada,
                "elapsed_fraction": round(nakshatra_result[2], 2)
            },
            "yoga": {
                "number": yoga_num,
                "name": yoga_names[yoga_num - 1],
                "elapsed_fraction": round(yoga_result[1], 2)
            },
            "karana": {
                "number": karana_num,
                "name": karana_names[karana_num] if karana_num < len(karana_names) else f"Karana {karana_num}",
                "elapsed_fraction": round(karana_result[1], 2)
            }
        }

    def calculate_extended_panchanga(self) -> Dict:
        """Calculate Extended Panchanga with timings and special periods"""
        # Get basic panchanga
        basic_panchanga = self.calculate_panchanga()

        # Get Vara (weekday)
        day_of_week = int((self.jd + 1.5) % 7)
        vara_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        vara_lords = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]

        # Get sunrise and sunset
        try:
            sunrise_jd = drik.sunrise(self.jd, self.place)[1]
            sunset_jd = drik.sunset(self.jd, self.place)[1]
            sunrise_hours = (sunrise_jd - int(sunrise_jd)) * 24
            sunset_hours = (sunset_jd - int(sunset_jd)) * 24
            sunrise_time = f"{int(sunrise_hours):02d}:{int((sunrise_hours % 1) * 60):02d}"
            sunset_time = f"{int(sunset_hours):02d}:{int((sunset_hours % 1) * 60):02d}"
        except:
            sunrise_time = "06:00"
            sunset_time = "18:00"

        # Get moonrise and moonset
        try:
            moonrise_jd = drik.moonrise(self.jd, self.place)[1]
            moonset_jd = drik.moonset(self.jd, self.place)[1]
            moonrise_hours = (moonrise_jd - int(moonrise_jd)) * 24
            moonset_hours = (moonset_jd - int(moonset_jd)) * 24
            moonrise_time = f"{int(moonrise_hours):02d}:{int((moonrise_hours % 1) * 60):02d}"
            moonset_time = f"{int(moonset_hours):02d}:{int((moonset_hours % 1) * 60):02d}"
        except:
            moonrise_time = "N/A"
            moonset_time = "N/A"

        # Rahu Kaal
        try:
            rahu_kaal = drik.raahu_kaalam(self.jd, self.place)
            rahu_start_hours = (rahu_kaal[0] - int(rahu_kaal[0])) * 24
            rahu_end_hours = (rahu_kaal[1] - int(rahu_kaal[1])) * 24
            rahu_kaal_timing = f"{int(rahu_start_hours):02d}:{int((rahu_start_hours % 1) * 60):02d} - " + \
                              f"{int(rahu_end_hours):02d}:{int((rahu_end_hours % 1) * 60):02d}"
        except:
            rahu_kaal_timing = "Not available"

        # Yamaganda
        try:
            yamaganda = drik.yamaganda_kaalam(self.jd, self.place)
            yama_start_hours = (yamaganda[0] - int(yamaganda[0])) * 24
            yama_end_hours = (yamaganda[1] - int(yamaganda[1])) * 24
            yamaganda_timing = f"{int(yama_start_hours):02d}:{int((yama_start_hours % 1) * 60):02d} - " + \
                              f"{int(yama_end_hours):02d}:{int((yama_end_hours % 1) * 60):02d}"
        except:
            yamaganda_timing = "Not available"

        # Gulika
        try:
            gulika = drik.gulikai_kaalam(self.jd, self.place)
            gulika_start_hours = (gulika[0] - int(gulika[0])) * 24
            gulika_end_hours = (gulika[1] - int(gulika[1])) * 24
            gulika_timing = f"{int(gulika_start_hours):02d}:{int((gulika_start_hours % 1) * 60):02d} - " + \
                           f"{int(gulika_end_hours):02d}:{int((gulika_end_hours % 1) * 60):02d}"
        except:
            gulika_timing = "Not available"

        # Durmuhurtam
        try:
            durmuhurta = drik.durmuhurtam(self.jd, self.place)
            durmuhurta_timings = []
            for period in durmuhurta:
                start_hours = (period[0] - int(period[0])) * 24
                end_hours = (period[1] - int(period[1])) * 24
                timing = f"{int(start_hours):02d}:{int((start_hours % 1) * 60):02d} - " + \
                        f"{int(end_hours):02d}:{int((end_hours % 1) * 60):02d}"
                durmuhurta_timings.append(timing)
        except:
            durmuhurta_timings = []

        # Abhijit Muhurta
        try:
            abhijit = drik.abhijit_muhurta(self.jd, self.place)
            abhijit_start_hours = (abhijit[0] - int(abhijit[0])) * 24
            abhijit_end_hours = (abhijit[1] - int(abhijit[1])) * 24
            abhijit_timing = f"{int(abhijit_start_hours):02d}:{int((abhijit_start_hours % 1) * 60):02d} - " + \
                            f"{int(abhijit_end_hours):02d}:{int((abhijit_end_hours % 1) * 60):02d}"
        except:
            abhijit_timing = "Not available"

        # Brahma Muhurta
        try:
            brahma = drik.brahma_muhurtha(self.jd, self.place)
            brahma_start_hours = (brahma[0] - int(brahma[0])) * 24
            brahma_end_hours = (brahma[1] - int(brahma[1])) * 24
            brahma_timing = f"{int(brahma_start_hours):02d}:{int((brahma_start_hours % 1) * 60):02d} - " + \
                           f"{int(brahma_end_hours):02d}:{int((brahma_end_hours % 1) * 60):02d}"
        except:
            brahma_timing = "Not available"

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "basic_panchanga": basic_panchanga,
            "vara": {
                "day": vara_names[day_of_week],
                "lord": vara_lords[day_of_week],
                "number": day_of_week + 1
            },
            "sun_moon_timings": {
                "sunrise": sunrise_time,
                "sunset": sunset_time,
                "moonrise": moonrise_time,
                "moonset": moonset_time
            },
            "inauspicious_periods": {
                "rahu_kaal": {
                    "timing": rahu_kaal_timing,
                    "description": "Period ruled by Rahu, inauspicious for new beginnings"
                },
                "yamaganda": {
                    "timing": yamaganda_timing,
                    "description": "Son of Yama period, inauspicious for important activities"
                },
                "gulika": {
                    "timing": gulika_timing,
                    "description": "Son of Saturn period, inauspicious for new ventures"
                },
                "durmuhurta": {
                    "timings": durmuhurta_timings,
                    "description": "Bad moments to avoid for any activity"
                }
            },
            "auspicious_periods": {
                "abhijit_muhurta": {
                    "timing": abhijit_timing,
                    "description": "Noon victory period, highly auspicious for all activities"
                },
                "brahma_muhurta": {
                    "timing": brahma_timing,
                    "description": "Pre-dawn spiritual time, best for meditation and study"
                }
            }
        }

    @staticmethod
    def calculate_marriage_compatibility(boy_birth_data: Dict, girl_birth_data: Dict, ayanamsa: str = "LAHIRI") -> Dict:
        """Calculate Marriage Compatibility using Ashtakoota system"""
        # Create calculators for both
        boy_calc = PyJHoraCalculator(boy_birth_data, ayanamsa)
        girl_calc = PyJHoraCalculator(girl_birth_data, ayanamsa)

        # Get nakshatras
        boy_nak = drik.nakshatra(boy_calc.jd, boy_calc.place)
        girl_nak = drik.nakshatra(girl_calc.jd, girl_calc.place)

        boy_nakshatra_num = int(boy_nak[0])
        boy_pada_num = int(boy_nak[1])
        girl_nakshatra_num = int(girl_nak[0])
        girl_pada_num = int(girl_nak[1])

        # Calculate Ashtakoota
        ashtakoota = compatibility.Ashtakoota(
            boy_nakshatra_num, boy_pada_num,
            girl_nakshatra_num, girl_pada_num,
            method="North"
        )

        # Get all scores (returns tuples of (score, max))
        varna_result = ashtakoota.varna_porutham()
        vasiya_result = ashtakoota.vasiya_porutham()
        tara_result = ashtakoota.tara_porutham()
        yoni_result = ashtakoota.yoni_porutham()
        maitri_result = ashtakoota.maitri_porutham()
        gana_result = ashtakoota.gana_porutham()
        rasi_result = ashtakoota.raasi_porutham()
        nadi_result = ashtakoota.naadi_porutham()

        # Extract scores
        varna_score = varna_result[0]
        vasiya_score = vasiya_result[0]
        tara_score = tara_result[0]
        yoni_score = yoni_result[0]
        maitri_score = maitri_result[0]
        gana_score = gana_result[0]
        rasi_score = rasi_result[0]
        nadi_score = nadi_result[0]

        total_score = (varna_score + vasiya_score + tara_score + yoni_score +
                      maitri_score + gana_score + rasi_score + nadi_score)

        # Nakshatra names for reference
        nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]

        # Compatibility interpretation
        if total_score >= 28:
            compatibility_rating = "Excellent"
            recommendation = "Highly compatible match. Very auspicious for marriage."
        elif total_score >= 24:
            compatibility_rating = "Very Good"
            recommendation = "Good compatibility. Suitable for marriage."
        elif total_score >= 18:
            compatibility_rating = "Average"
            recommendation = "Moderate compatibility. Some challenges may arise."
        else:
            compatibility_rating = "Below Average"
            recommendation = "Low compatibility. Marriage may face significant challenges."

        return {
            "status": "success",
            "boy": {
                "birth_data": boy_birth_data,
                "nakshatra": nakshatra_names[boy_nakshatra_num - 1],
                "nakshatra_pada": boy_pada_num
            },
            "girl": {
                "birth_data": girl_birth_data,
                "nakshatra": nakshatra_names[girl_nakshatra_num - 1],
                "nakshatra_pada": girl_pada_num
            },
            "ashtakoota_scores": {
                "varna": {"score": float(varna_score), "max": float(varna_result[1])},
                "vasiya": {"score": float(vasiya_score), "max": float(vasiya_result[1])},
                "tara": {"score": float(tara_score), "max": float(tara_result[1])},
                "yoni": {"score": float(yoni_score), "max": float(yoni_result[1])},
                "graha_maitri": {"score": float(maitri_score), "max": float(maitri_result[1])},
                "gana": {"score": float(gana_score), "max": float(gana_result[1])},
                "rasi": {"score": float(rasi_score), "max": float(rasi_result[1])},
                "nadi": {"score": float(nadi_score), "max": float(nadi_result[1])}
            },
            "total_score": total_score,
            "maximum_score": 36,
            "percentage": round((total_score / 36) * 100, 2),
            "compatibility_rating": compatibility_rating,
            "recommendation": recommendation
        }

    def calculate_special_lagnas(self) -> Dict:
        """Calculate Special Lagnas (Ascendants for specific purposes)"""
        # Calculate all special lagnas
        hora_lagna_result = drik.hora_lagna(self.jd, self.place)
        ghati_lagna_result = drik.ghati_lagna(self.jd, self.place)
        bhava_lagna_result = drik.bhava_lagna(self.jd, self.place)
        sree_lagna_result = drik.sree_lagna(self.jd, self.place)
        pranapada_lagna_result = drik.pranapada_lagna(self.jd, self.place)
        indu_lagna_result = drik.indu_lagna(self.jd, self.place)
        bhrigu_bindhu_lagna_result = drik.bhrigu_bindhu_lagna(self.jd, self.place)

        # Format each lagna
        def format_lagna(lagna_result):
            sign_id = int(lagna_result[0])
            longitude = float(lagna_result[1])
            degree = int(longitude)
            minute = int((longitude - degree) * 60)
            return {
                "sign": SIGN_NAMES[sign_id],
                "sign_id": sign_id,
                "longitude": round(longitude, 2),
                "degree": degree,
                "minute": minute
            }

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "special_lagnas": {
                "hora_lagna": {
                    **format_lagna(hora_lagna_result),
                    "description": "Wealth and financial matters"
                },
                "ghati_lagna": {
                    **format_lagna(ghati_lagna_result),
                    "description": "Timing and general fortune"
                },
                "bhava_lagna": {
                    **format_lagna(bhava_lagna_result),
                    "description": "Mental disposition and temperament"
                },
                "sree_lagna": {
                    **format_lagna(sree_lagna_result),
                    "description": "Prosperity and overall well-being"
                },
                "pranapada_lagna": {
                    **format_lagna(pranapada_lagna_result),
                    "description": "Longevity and life force"
                },
                "indu_lagna": {
                    **format_lagna(indu_lagna_result),
                    "description": "Wealth from inheritance and family"
                },
                "bhrigu_bindhu_lagna": {
                    **format_lagna(bhrigu_bindhu_lagna_result),
                    "description": "Past life karma and spirituality"
                }
            }
        }

    def calculate_bhava_bala(self) -> Dict:
        """Calculate Bhava Bala (House Strength)"""
        # Calculate Bhava Bala
        bhava_bala_values = strength.bhava_bala(self.jd, self.place)

        # Format the results
        house_strengths = []
        for i in range(12):
            if i < len(bhava_bala_values):
                strength_data = bhava_bala_values[i]
                if isinstance(strength_data, (list, tuple)) and len(strength_data) > 0:
                    total_strength = strength_data[0] if isinstance(strength_data[0], (int, float)) else 0
                    house_strengths.append({
                        "house": i + 1,
                        "sign": SIGN_NAMES[i % 12],
                        "total_strength": round(total_strength, 2),
                        "strength_components": list(strength_data[1:]) if len(strength_data) > 1 else []
                    })

        # Find strongest and weakest houses
        if house_strengths:
            strongest = max(house_strengths, key=lambda x: x['total_strength'])
            weakest = min(house_strengths, key=lambda x: x['total_strength'])
        else:
            strongest = weakest = None

        return {
            "status": "success",
            "birth_data": self.birth_data,
            "house_strengths": house_strengths,
            "strongest_house": {
                "house": strongest['house'],
                "strength": strongest['total_strength']
            } if strongest else None,
            "weakest_house": {
                "house": weakest['house'],
                "strength": weakest['total_strength']
            } if weakest else None
        }

    def calculate_current_transits(self) -> Dict:
        """Calculate current planetary transits (Gochara)"""
        # Get current planetary positions
        positions = []
        for planet_id in range(9):  # 0-8 (Sun to Ketu)
            # Get longitude for all planets using sidereal_longitude
            long_deg = drik.sidereal_longitude(self.jd, planet_id)

            sign_num = int(long_deg / 30)
            degree = long_deg % 30

            # Get nakshatra
            nak_num = int(long_deg / 13.333333333333334) % 27
            nak_pada = int((long_deg % 13.333333333333334) / 3.333333333333333) + 1

            # Get planet speed
            speed = drik.daily_planet_speed(self.jd, self.place, planet_id)
            is_retrograde = speed < 0

            positions.append({
                "planet": PLANET_NAMES.get(planet_id, f"Planet_{planet_id}"),
                "sign": SIGN_NAMES[sign_num],
                "degree": round(degree, 2),
                "longitude": round(long_deg, 2),
                "nakshatra": self._get_nakshatra_name(nak_num),
                "nakshatra_pada": nak_pada,
                "speed": round(speed, 4),
                "retrograde": is_retrograde
            })

        return {
            "status": "success",
            "calculation_date": self.birth_data.get('date'),
            "calculation_time": self.birth_data.get('time'),
            "planetary_positions": positions
        }

    def calculate_sade_sati(self) -> Dict:
        """Calculate Sade Sati (Saturn's 7.5-year transit)"""
        # Get Moon's sign in birth chart
        moon_long = drik.sidereal_longitude(self.jd, 1)  # Moon is planet 1
        moon_sign = int(moon_long / 30)

        # Get current Saturn position
        saturn_long = drik.sidereal_longitude(self.jd, 6)  # Saturn is planet 6
        saturn_sign = int(saturn_long / 30)

        # Sade Sati spans 3 signs: 12th from Moon, Moon sign, 2nd from Moon
        sade_sati_start_sign = (moon_sign - 1) % 12
        sade_sati_end_sign = (moon_sign + 1) % 12

        # Check if Saturn is in Sade Sati zone
        in_sade_sati = False
        current_phase = None

        if saturn_sign == sade_sati_start_sign:
            in_sade_sati = True
            current_phase = "Rising Phase (12th from Moon)"
        elif saturn_sign == moon_sign:
            in_sade_sati = True
            current_phase = "Peak Phase (on Moon)"
        elif saturn_sign == sade_sati_end_sign:
            in_sade_sati = True
            current_phase = "Setting Phase (2nd from Moon)"

        # Calculate approximate dates (Saturn takes ~2.5 years per sign)
        return {
            "status": "success",
            "birth_data": self.birth_data,
            "moon_sign": SIGN_NAMES[moon_sign],
            "current_saturn_sign": SIGN_NAMES[saturn_sign],
            "in_sade_sati": in_sade_sati,
            "current_phase": current_phase,
            "sade_sati_signs": {
                "rising": SIGN_NAMES[sade_sati_start_sign],
                "peak": SIGN_NAMES[moon_sign],
                "setting": SIGN_NAMES[sade_sati_end_sign]
            },
            "description": "Sade Sati is Saturn's 7.5-year transit over Moon sign and adjacent signs. " +
                          "It's considered a period of challenges and spiritual growth."
        }

    def calculate_next_planet_entries(self, num_entries: int = 5) -> Dict:
        """Calculate next planet entry dates into signs"""
        entries = []

        # Check entries for all planets except Rahu/Ketu (they're always retrograde)
        for planet_id in range(7):  # 0-6 (Sun to Saturn)
            try:
                # Get next entry date
                next_date = drik.next_planet_entry_date(self.jd, planet_id)

                if next_date:
                    # Convert to datetime
                    year, month, day, hours = next_date
                    entry_datetime = datetime(int(year), int(month), int(day), int(hours),
                                            int((hours % 1) * 60))

                    # Get the sign the planet will enter
                    entry_jd = swe.julday(int(year), int(month), int(day), hours)
                    future_long = drik.sidereal_longitude(entry_jd, planet_id)
                    future_sign = int(future_long / 30)

                    entries.append({
                        "planet": PLANET_NAMES[planet_id],
                        "entry_date": entry_datetime.strftime("%Y-%m-%d"),
                        "entry_time": entry_datetime.strftime("%H:%M"),
                        "entering_sign": SIGN_NAMES[future_sign],
                        "entry_datetime": entry_datetime.isoformat()
                    })
            except Exception as e:
                continue

        # Sort by date
        entries.sort(key=lambda x: x['entry_datetime'])

        return {
            "status": "success",
            "calculation_from": self.birth_data.get('date'),
            "next_entries": entries[:num_entries]
        }

    @staticmethod
    def _get_nakshatra_name(nak_num: int) -> str:
        """Get nakshatra name from number"""
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        return nakshatras[nak_num % 27]
