"""Transit (Gochara) calculation endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/transits", tags=["Transits"])

@router.post("/current", responses={400: {"model": ErrorResponse}})
async def calculate_current_transits(request: ChartRequest):
    """
    Calculate Current Planetary Transits (Gochara)

    Returns current positions of all 9 planets with:
    - Sign and degree position
    - Nakshatra and pada
    - Daily speed (degrees/day)
    - Retrograde status

    **Use Cases:**
    - Daily horoscope analysis
    - Transit predictions
    - Identifying planetary movements
    - Retrograde tracking

    **Note:** Pass current date/time in birth_data to get current transits.
    For any date/time, use that date in birth_data field.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_current_transits()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sade-sati", responses={400: {"model": ErrorResponse}})
async def calculate_sade_sati(request: ChartRequest):
    """
    Calculate Sade Sati (Saturn's 7.5-Year Transit)

    Sade Sati is the 7.5-year period when Saturn transits:
    1. **Rising Phase**: 12th house from Moon (2.5 years)
    2. **Peak Phase**: Over Moon sign (2.5 years) - Most challenging
    3. **Setting Phase**: 2nd house from Moon (2.5 years)

    This period is considered:
    - Challenging and transformative
    - Tests patience and perseverance
    - Brings spiritual growth
    - Requires hard work and discipline

    Returns:
    - Current phase (if in Sade Sati)
    - Moon sign from birth chart
    - Current Saturn position
    - Whether native is in Sade Sati

    **Note:** Use birth data for natal Moon, current date for Saturn position.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_sade_sati()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/next-entries", responses={400: {"model": ErrorResponse}})
async def calculate_next_planet_entries(request: ChartRequest):
    """
    Calculate Next Planet Entry Dates into Signs

    Returns the next 5 planet ingress (entry) dates when planets
    move from one zodiac sign to another.

    **Useful for:**
    - Planning important events
    - Timing predictions
    - Understanding upcoming influences
    - Transit forecasting

    **Planets tracked:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
    (Rahu/Ketu move retrograde and are excluded)

    Returns for each entry:
    - Planet name
    - Entry date and time
    - Sign being entered
    - ISO datetime for sorting

    **Note:** Calculates from the date/time provided in birth_data.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_next_planet_entries(num_entries=5)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
