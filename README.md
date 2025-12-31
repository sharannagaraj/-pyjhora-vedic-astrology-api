# PyJHora Vedic Astrology API

A production-ready FastAPI server for Vedic astrology calculations using the PyJHora library.

## Features

- ✅ **Birth Charts (D1 Rasi)**
- ✅ **Divisional Charts** (D2-D60: Navamsa, Dasamsa, etc.)
- ✅ **Vimsottari Dasha** calculations with current period
- ✅ **House-wise** planetary placements
- ✅ **Automatic validation** with Pydantic
- ✅ **Interactive API docs** (Swagger/ReDoc)
- ✅ **CORS enabled** for web apps
- ✅ **Health check** endpoint

## API Endpoints

### Charts
- `POST /api/v1/charts/rasi` - D1 Birth Chart
- `POST /api/v1/charts/navamsa` - D9 Navamsa Chart
- `POST /api/v1/charts/dasamsa` - D10 Career Chart
- `POST /api/v1/charts/divisional` - Any divisional chart
- `POST /api/v1/charts/house-wise/{chart_type}` - House-wise placement

### Dashas
- `POST /api/v1/dashas/vimsottari` - Vimsottari Dasha periods
- `POST /api/v1/dashas/current` - Current running Dasha

### Utility
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/v1/ayanamsa/list` - List ayanamsa systems
- `GET /api/v1/charts/types` - List chart types
- `GET /docs` - Interactive API documentation
- `GET /redoc` - ReDoc documentation

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone/navigate to project
cd pyjhora-api

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for interactive API documentation.

## Testing the API

### Example Request (cURL)

```bash
curl -X POST "http://localhost:8000/api/v1/charts/rasi" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1998-12-22",
      "time": "17:12:00",
      "timezone_offset": 5.5,
      "latitude": 12.9716,
      "longitude": 77.5946,
      "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
  }'
```

### Example Request (Python)

```python
import requests

url = "http://localhost:8000/api/v1/charts/navamsa"

payload = {
    "birth_data": {
        "date": "1998-12-22",
        "time": "17:12:00",
        "timezone_offset": 5.5,
        "latitude": 12.9716,
        "longitude": 77.5946,
        "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Example Request (JavaScript)

```javascript
const response = await fetch('http://localhost:8000/api/v1/dashas/vimsottari', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    birth_data: {
      date: '1998-12-22',
      time: '17:12:00',
      timezone_offset: 5.5,
      latitude: 12.9716,
      longitude: 77.5946,
      place_name: 'Bangalore, India'
    },
    ayanamsa: 'LAHIRI'
  })
});

const data = await response.json();
console.log(data);
```

## Deployment

### Deploy to Railway

1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI: `npm install -g @railway/cli`
3. Login: `railway login`
4. Initialize: `railway init`
5. Deploy: `railway up`

Your API will be live at: `https://your-app.railway.app`

### Deploy to Render

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Click "Create Web Service"

Your API will be live at: `https://your-app.onrender.com`

### Deploy with Docker

```bash
# Build image
docker build -t pyjhora-api .

# Run container
docker run -p 8000:8000 pyjhora-api
```

## Environment Variables

No environment variables required for basic operation.

Optional:
- `PORT` - Port to run on (default: 8000)
- `WORKERS` - Number of worker processes (default: 4)

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PyJHora** - Vedic astrology calculations
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Gunicorn** - Production server
- **SwissEph** - Astronomical calculations

## API Response Example

### D1 Rasi Chart Response

```json
{
  "status": "success",
  "chart_type": "D1",
  "birth_data": {
    "date": "1998-12-22",
    "time": "17:12:00",
    "timezone_offset": 5.5,
    "latitude": 12.9716,
    "longitude": 77.5946,
    "place_name": "Bangalore, India"
  },
  "ascendant": {
    "sign": "Aquarius",
    "sign_id": 10,
    "degree": 25.5257
  },
  "planets": [
    {
      "planet": "Sun",
      "sign": "Sagittarius",
      "sign_id": 8,
      "longitude": 6.3466,
      "degree": 6,
      "minute": 20,
      "house": 11
    },
    {
      "planet": "Moon",
      "sign": "Capricorn",
      "sign_id": 9,
      "longitude": 14.6634,
      "degree": 14,
      "minute": 39,
      "house": 12
    }
  ],
  "calculation_info": {
    "ayanamsa": "LAHIRI",
    "ayanamsa_value": 23.8428,
    "julian_day": 2451169.9875,
    "divisional_factor": 1
  }
}
```

## License

This API uses PyJHora which is licensed under GNU AGPL v3.

## Support

For issues or questions:
- API Documentation: `/docs`
- PyJHora Documentation: [GitHub](https://github.com/naturalstupid/PyJHora)

## Version

- **API Version**: 1.0.0
- **PyJHora Version**: 4.5.5
- **FastAPI Version**: 0.109.0
