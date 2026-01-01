# Comprehensive API Endpoint Guide

## Complete Vedic Astrology Analysis in One API Call

**Version:** 1.2.0
**Endpoint:** `POST /api/v1/comprehensive/full-analysis`

---

## Overview

This endpoint returns **ALL major Vedic astrology calculations** in a single API call, eliminating the need to make multiple requests.

### What You Get in One Call:

✅ **3 Divisional Charts** - D1 (Rasi), D9 (Navamsa), D10 (Dasamsa)
✅ **Maha Dasha** - 9 planetary periods (120-year cycle)
✅ **Antardasha** - 81 sub-periods (Bhukti)
✅ **7 Bhinna Ashtakavarga** - Individual planet bindu charts
✅ **Sarvashtakavarga** - Combined bindu strength chart
✅ **All Yogas** - Planetary combinations (39 analyzed)
✅ **All Doshas** - Afflictions (8 analyzed)

---

## API Request

### Endpoint
```
POST http://localhost:8002/api/v1/comprehensive/full-analysis
```

### Request Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "birth_data": {
    "date": "1998-12-22",
    "time": "17:12:00",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timezone_offset": 5.5,
    "place_name": "Bangalore, India"
  },
  "ayanamsa": "LAHIRI"
}
```

### Parameters

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `birth_data.date` | string | Yes | Date in YYYY-MM-DD format | "1998-12-22" |
| `birth_data.time` | string | Yes | Time in HH:MM:SS format (24-hour) | "17:12:00" |
| `birth_data.latitude` | float | Yes | Latitude (North positive, South negative) | 12.9716 |
| `birth_data.longitude` | float | Yes | Longitude (East positive, West negative) | 77.5946 |
| `birth_data.timezone_offset` | float | Yes | UTC offset in hours | 5.5 (IST) |
| `birth_data.place_name` | string | Yes | Place name for reference | "Bangalore, India" |
| `ayanamsa` | string | No | Ayanamsa system (default: LAHIRI) | "LAHIRI" |

### Available Ayanamsa Systems
- `LAHIRI` (default, most common)
- `KP` (Krishnamurti Paddhati)
- `TRUE_CITRA`
- `SURYA_SIDDHANTA`
- `RAMAN`
- `YUKTESHWAR`

---

## Response Structure

### Top-Level Fields

```json
{
  "status": "success",
  "birth_data": { ... },
  "ayanamsa": "LAHIRI",
  "charts": { ... },
  "dashas": { ... },
  "ashtakavarga": { ... },
  "yogas": { ... },
  "doshas": { ... },
  "summary": { ... }
}
```

---

## Response Details

### 1. Charts Object

Contains D1, D9, and D10 charts with complete planetary positions.

```json
"charts": {
  "d1_rasi": {
    "name": "D1 - Rasi (Birth Chart)",
    "ascendant": {
      "sign": "Taurus",
      "degree": 26.56,
      "house": 1
    },
    "planets": [
      {
        "planet": "Sun",
        "house": 8,
        "sign": "Sagittarius",
        "degree": 6.00,
        "longitude": 246.00,
        "nakshatra": "Mula",
        "nakshatra_pada": 2,
        "retrograde": false
      },
      // ... 8 more planets
    ]
  },
  "d9_navamsa": { ... },
  "d10_dasamsa": { ... }
}
```

**Each Chart Contains:**
- Ascendant sign and degree
- 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
- For each planet:
  - House position (1-12)
  - Sign position
  - Degree within sign
  - Absolute longitude (0-360°)
  - Nakshatra and pada
  - Retrograde status

---

### 2. Dashas Object

Contains Maha Dasha and Antardasha periods.

```json
"dashas": {
  "maha_dasha": {
    "system": "Vimsottari",
    "moon_nakshatra": {
      "number": 22,
      "name": "Shravana",
      "lord": "Moon"
    },
    "periods": [
      {
        "lord": "Moon",
        "start_date": "1993-04-05",
        "end_date": "2003-04-05",
        "duration_years": 10
      },
      // ... 8 more periods
    ],
    "current_period": {
      "lord": "Rahu",
      "start_date": "2010-04-04",
      "end_date": "2028-04-03",
      "duration_years": 18,
      "elapsed_years": 15.75,
      "remaining_years": 2.25
    }
  },
  "antardasha": {
    "system": "Vimsottari",
    "total_periods": 81,
    "periods": [
      {
        "maha_dasha_lord": "Moon",
        "bhukti_lord": "Moon",
        "start_date": "1993-04-05 09:13:56"
      },
      // ... 80 more periods
    ],
    "current_period": { ... }
  }
}
```

**Maha Dasha:**
- 9 planetary periods (120-year cycle)
- Current running period with elapsed and remaining time
- Moon's birth nakshatra

**Antardasha:**
- 81 sub-periods (9 per Maha Dasha)
- Start dates for each period
- Current running sub-period

---

### 3. Ashtakavarga Object

Contains Bhinna Ashtakavarga (7 planets) and Sarvashtakavarga.

```json
"ashtakavarga": {
  "bhinna_ashtakavarga": {
    "description": "7 Individual Planet Charts",
    "planets": {
      "Sun": {
        "bindus": [4, 3, 5, 6, 3, 3, 7, 3, 4, 3, 2, 5],
        "total": 48
      },
      "Moon": {
        "bindus": [1, 3, 6, 4, 4, 6, 5, 4, 1, 3, 7, 5],
        "total": 49
      },
      // ... Mars, Mercury, Jupiter, Venus, Saturn, Ascendant
    }
  },
  "sarvashtakavarga": {
    "description": "Combined Ashtakavarga",
    "data": {
      "bindus_per_house": [23, 22, 29, 35, 27, 31, 35, 27, 25, 24, 28, 31],
      "total_bindus": 337,
      "strongest_house": 4,
      "weakest_house": 2
    }
  }
}
```

**Bhinna Ashtakavarga:**
- 7 planets + Ascendant (8 total)
- Bindu distribution across 12 houses
- Total bindus per planet

**Sarvashtakavarga:**
- Combined bindu strength
- Strongest and weakest houses
- Total bindus across all houses

---

### 4. Yogas Object

Contains all planetary combination analysis.

```json
"yogas": {
  "total_analyzed": 39,
  "total_present": 0,
  "present_yogas": [],
  "all_yogas": [
    {
      "name": "Gaja Kesari Yoga",
      "present": false,
      "description": "Moon and Jupiter in mutual kendras...",
      "effects": "Wealth, wisdom, respect..."
    },
    // ... all 39 yogas
  ]
}
```

**Fields:**
- `total_analyzed`: Number of yogas checked (39)
- `total_present`: How many are present in chart
- `present_yogas`: Only yogas that are present
- `all_yogas`: Complete list with present/absent status

---

### 5. Doshas Object

Contains all affliction analysis.

```json
"doshas": {
  "total_analyzed": 8,
  "total_present": 2,
  "present_doshas": [
    {
      "name": "Pitru Dosha",
      "present": true,
      "description": "Ancestral karmic debt...",
      "severity": "Moderate",
      "remedies": "Shradh rituals, donations..."
    },
    {
      "name": "Guru Chandala Dosha",
      "present": true,
      "description": "Jupiter-Rahu conjunction...",
      "severity": "Low"
    }
  ],
  "all_doshas": [ ... ]
}
```

**Doshas Analyzed:**
1. Mangal Dosha (Mars affliction)
2. Kaal Sarp Dosha (Rahu-Ketu axis)
3. Pitru Dosha (Ancestral karma)
4. Guru Chandala Dosha (Jupiter-Rahu)
5. Shakata Dosha (Moon-Jupiter)
6. Kemadrum Dosha (Moon isolation)
7. Grahan Dosha (Eclipse)
8. Nadi Dosha (Compatibility)

---

### 6. Summary Object

Quick overview of all calculations.

```json
"summary": {
  "charts_calculated": ["D1 Rasi", "D9 Navamsa", "D10 Dasamsa"],
  "maha_dasha_periods": 9,
  "antardasha_periods": 81,
  "bhinna_ashtakavarga_planets": 7,
  "yogas_present": 0,
  "doshas_present": 2,
  "current_maha_dasha": "Rahu",
  "strongest_planet_ashtakavarga": "Jupiter"
}
```

---

## Usage Examples

### Python Example

```python
import requests
import json

# API endpoint
url = "http://localhost:8002/api/v1/comprehensive/full-analysis"

# Request payload
payload = {
    "birth_data": {
        "date": "1998-12-22",
        "time": "17:12:00",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone_offset": 5.5,
        "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
}

# Make request
response = requests.post(url, json=payload)

# Get response
if response.status_code == 200:
    data = response.json()

    # Access charts
    d1_chart = data['charts']['d1_rasi']
    print(f"Ascendant: {d1_chart['ascendant']['sign']}")

    # Access current dasha
    current_dasha = data['dashas']['maha_dasha']['current_period']
    print(f"Current Dasha: {current_dasha['lord']}")

    # Access ashtakavarga
    jupiter_bindus = data['ashtakavarga']['bhinna_ashtakavarga']['planets']['Jupiter']['total']
    print(f"Jupiter Total Bindus: {jupiter_bindus}")

    # Access doshas
    doshas_present = data['doshas']['total_present']
    print(f"Doshas Present: {doshas_present}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### JavaScript Example

```javascript
const axios = require('axios');

const url = 'http://localhost:8002/api/v1/comprehensive/full-analysis';

const payload = {
  birth_data: {
    date: '1998-12-22',
    time: '17:12:00',
    latitude: 12.9716,
    longitude: 77.5946,
    timezone_offset: 5.5,
    place_name: 'Bangalore, India'
  },
  ayanamsa: 'LAHIRI'
};

axios.post(url, payload)
  .then(response => {
    const data = response.data;

    // Access summary
    console.log('Summary:', data.summary);

    // Access D1 chart
    const d1 = data.charts.d1_rasi;
    console.log('Ascendant:', d1.ascendant);

    // Access Maha Dasha
    const currentDasha = data.dashas.maha_dasha.current_period;
    console.log('Current Dasha:', currentDasha.lord);

    // Access Ashtakavarga
    const ashtaka = data.ashtakavarga.sarvashtakavarga.data;
    console.log('Total Bindus:', ashtaka.total_bindus);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### cURL Example

```bash
curl -X POST http://localhost:8002/api/v1/comprehensive/full-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1998-12-22",
      "time": "17:12:00",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "timezone_offset": 5.5,
      "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
  }'
```

---

## Response Size

**Typical Response Size:** ~32-35 KB (compressed)

**Contains:**
- 3 complete divisional charts (27 planetary positions)
- 9 Maha Dasha periods
- 81 Antardasha periods
- 8 Bhinna Ashtakavarga charts (96 house values)
- 1 Sarvashtakavarga chart (12 house values)
- 39 Yoga analyses
- 8 Dosha analyses

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "invalid literal for int() with base 10: 'invalid-date'"
}
```

**Common Causes:**
- Invalid date format (must be YYYY-MM-DD)
- Invalid time format (must be HH:MM:SS)
- Missing required fields
- Invalid latitude/longitude values

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "birth_data", "date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Performance

**Average Response Time:** 500-800ms
**Includes:**
- Chart calculations: ~200ms
- Dasha calculations: ~100ms
- Ashtakavarga: ~100ms
- Yogas: ~50ms
- Doshas: ~50ms

---

## Comparison with Individual Endpoints

### Before (Multiple API Calls):

```python
# 9 separate API calls needed
d1 = requests.post('/api/v1/charts/rasi', json=payload)
d9 = requests.post('/api/v1/charts/navamsa', json=payload)
d10 = requests.post('/api/v1/charts/divisional', json=payload)
dashas = requests.post('/api/v1/dashas/vimsottari', json=payload)
bhukti = requests.post('/api/v1/dashas/bhukti', json=payload)
ashtaka = requests.post('/api/v1/strength/ashtakavarga', json=payload)
yogas = requests.post('/api/v1/yogas/', json=payload)
doshas = requests.post('/api/v1/doshas/', json=payload)

# Total time: ~2-3 seconds
# Total data transferred: ~40KB
# Network overhead: 8 round trips
```

### Now (Single API Call):

```python
# 1 comprehensive API call
data = requests.post('/api/v1/comprehensive/full-analysis', json=payload)

# Total time: ~500-800ms
# Total data transferred: ~32KB
# Network overhead: 1 round trip
```

**Benefits:**
- ⚡ **3-4x faster** (single round trip)
- 📦 **20% less data** (no duplicate fields)
- 💻 **Simpler code** (one call vs nine)
- 🔄 **Atomic data** (all calculations from same moment)

---

## API Versioning

**Current Version:** 1.2.0

**Version History:**
- **v1.2.0** - Added comprehensive endpoint
- **v1.1.0** - Added transit analysis and extended panchanga
- **v1.0.0** - Initial release

---

## Rate Limiting

Currently no rate limiting implemented. Recommended usage:
- Maximum 10 requests per minute
- Cache responses when possible
- Use for on-demand calculations only

---

## Support

**Documentation:** http://localhost:8002/docs
**API Reference:** http://localhost:8002/redoc
**Health Check:** http://localhost:8002/health

---

## License

PyJHora Vedic Astrology API v1.2.0
Based on PyJHora library v4.5.5
