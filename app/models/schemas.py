"""Pydantic models for API request/response validation"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from datetime import datetime

class BirthData(BaseModel):
    """Birth data input model"""
    date: str = Field(..., description="Birth date in YYYY-MM-DD format", example="1990-05-15")
    time: str = Field(..., description="Birth time in HH:MM:SS format (24-hour)", example="06:30:00")
    timezone_offset: float = Field(..., description="Timezone offset from UTC (e.g., 5.5 for IST)", example=5.5)
    latitude: float = Field(..., description="Latitude in decimal degrees", example=13.0827)
    longitude: float = Field(..., description="Longitude in decimal degrees", example=80.2707)
    place_name: Optional[str] = Field(None, description="Place name (optional)", example="Chennai, India")

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    @validator('time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM:SS format (24-hour)")

    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

class ChartRequest(BaseModel):
    """Request model for chart calculation"""
    birth_data: BirthData
    ayanamsa: Optional[str] = Field("LAHIRI", description="Ayanamsa system", example="LAHIRI")
    chart_type: Optional[str] = Field("D1", description="Chart type (D1, D9, D10, etc.)", example="D1")

class PlanetPosition(BaseModel):
    """Planet position in a chart"""
    planet: str
    sign: str
    sign_id: int
    longitude: float
    degree: int
    minute: int
    house: Optional[int] = None

class ChartResponse(BaseModel):
    """Response model for chart calculation"""
    status: str = "success"
    chart_type: str
    birth_data: Dict
    ascendant: Dict
    planets: List[PlanetPosition]
    calculation_info: Dict

class DashaRequest(BaseModel):
    """Request model for Dasha calculation"""
    birth_data: BirthData
    ayanamsa: Optional[str] = Field("LAHIRI", description="Ayanamsa system")
    dasha_system: Optional[str] = Field("VIMSOTTARI", description="Dasha system type")

class DashaPeriod(BaseModel):
    """Dasha period model"""
    lord: str
    start_date: str
    end_date: str
    duration_years: float

class DashaResponse(BaseModel):
    """Response model for Dasha calculation"""
    status: str = "success"
    dasha_system: str
    birth_data: Dict
    moon_nakshatra: Optional[Dict] = None
    current_dasha: Optional[Dict] = None
    maha_dasha_periods: List[DashaPeriod]
    antara_dasha_periods: Optional[List[Dict]] = None

class AshtakavargaRequest(BaseModel):
    """Request model for Ashtakavarga calculation"""
    birth_data: BirthData
    ayanamsa: Optional[str] = Field("LAHIRI", description="Ayanamsa system")

class AshtakavargaResponse(BaseModel):
    """Response model for Ashtakavarga calculation"""
    status: str = "success"
    birth_data: Dict
    binna_ashtakavarga: Optional[Dict] = None
    samudhaya_ashtakavarga: Optional[Dict] = None

class PanchangaRequest(BaseModel):
    """Request model for Panchanga calculation"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    latitude: float
    longitude: float
    timezone_offset: float

class PanchangaResponse(BaseModel):
    """Response model for Panchanga calculation"""
    status: str = "success"
    date: str
    location: Dict
    tithi: Dict
    nakshatra: Dict
    yoga: Dict
    karana: Dict
    sunrise: Optional[str] = None
    sunset: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    error: str
    detail: Optional[str] = None

class CompatibilityRequest(BaseModel):
    """Request model for marriage compatibility calculation"""
    boy_birth_data: BirthData
    girl_birth_data: BirthData
    ayanamsa: Optional[str] = Field("LAHIRI", description="Ayanamsa system")
