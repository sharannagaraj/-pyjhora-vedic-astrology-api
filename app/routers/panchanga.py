"""Panchanga calculation endpoint"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/panchanga", tags=["Panchanga"])

@router.post("/", responses={400: {"model": ErrorResponse}})
async def calculate_panchanga(request: ChartRequest):
    """
    Calculate Panchanga (Five Limbs of Time)

    Panchanga consists of 5 elements that define the quality of time:

    1. **Tithi**: Lunar day (1-30), divided into Shukla Paksha (waxing) and Krishna Paksha (waning)
    2. **Nakshatra**: Lunar mansion (1-27), showing Moon's position in the zodiac
    3. **Yoga**: Auspicious/inauspicious combinations (1-27) based on Sun-Moon positions
    4. **Karana**: Half of a Tithi (1-11), governing specific activities
    5. **Vara**: Day of the week

    Each element has an elapsed fraction showing how much has passed.

    Used for:
    - Muhurta (auspicious timing)
    - Daily predictions
    - Religious observances
    - Event planning
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_panchanga()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/extended", responses={400: {"model": ErrorResponse}})
async def calculate_extended_panchanga(request: ChartRequest):
    """
    Calculate Extended Panchanga with Timings and Special Periods

    Includes all basic Panchanga elements PLUS:

    **Vara (Weekday):**
    - Day name and ruling planet

    **Sun & Moon Timings:**
    - Sunrise and Sunset times
    - Moonrise and Moonset times

    **Inauspicious Periods (Avoid these times):**
    1. **Rahu Kaal**: Period ruled by Rahu (~1.5 hours, varies by weekday)
       - Monday: 07:30-09:00, Tuesday: 15:00-16:30, etc.
       - Inauspicious for new beginnings
    2. **Yamaganda**: Son of Yama period (~1.5 hours)
       - Inauspicious for important activities
    3. **Gulika**: Son of Saturn period (~1.5 hours)
       - Avoid for new ventures
    4. **Durmuhurta**: Multiple bad moments throughout the day
       - Avoid for any significant activity

    **Auspicious Periods (Best times):**
    1. **Abhijit Muhurta**: Noon victory period (~48 minutes around noon)
       - Highly auspicious for all activities
       - Nullifies doshas in chart
    2. **Brahma Muhurta**: Pre-dawn spiritual time (~48 minutes before sunrise)
       - Best for meditation, study, spiritual practices

    **Use Cases:**
    - Wedding timing (Muhurta)
    - Starting new ventures
    - Important meetings
    - Religious ceremonies
    - Daily activity planning

    **Note:** All times are in 24-hour format (HH:MM)
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_extended_panchanga()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
