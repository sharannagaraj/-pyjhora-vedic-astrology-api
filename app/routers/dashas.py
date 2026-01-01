"""Dasha calculation endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import DashaRequest, DashaResponse, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/dashas", tags=["Dashas"])

@router.post("/vimsottari", response_model=DashaResponse, responses={400: {"model": ErrorResponse}})
async def calculate_vimsottari_dasha(request: DashaRequest):
    """
    Calculate Vimsottari Dasha Periods

    Returns Maha Dasha periods (120-year cycle) with current dasha information.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_dasha("VIMSOTTARI")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/current")
async def get_current_dasha(request: DashaRequest):
    """
    Get Current Running Dasha Period

    Returns only the current Maha Dasha with elapsed and remaining time.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_dasha("VIMSOTTARI")

        if result.get("current_dasha"):
            return {
                "status": "success",
                "current_dasha": result["current_dasha"],
                "moon_nakshatra": result["moon_nakshatra"]
            }
        else:
            return {
                "status": "success",
                "message": "Current dasha period not found"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bhukti")
async def calculate_dasha_bhukti(request: DashaRequest):
    """
    Calculate Vimsottari Dasha with Bhukti (Sub-periods)

    Returns all Maha Dasha and Bhukti (Antara Dasha) periods with current period info.
    Each Bhukti period shows which Maha Dasha it belongs to and its duration.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_dasha_bhukti("VIMSOTTARI")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
