"""Dosha calculation endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/doshas", tags=["Doshas"])

@router.post("/", responses={400: {"model": ErrorResponse}})
async def calculate_doshas(request: ChartRequest):
    """
    Calculate All Doshas in Birth Chart

    Detects major doshas including:
    - Kala Sarpa Dosha (all planets between Rahu-Ketu axis)
    - Manglik Dosha (Mars dosha affecting marriage)
    - Pitru Dosha (ancestral karmic debt)
    - Guru Chandala Dosha (Jupiter-Rahu conjunction)
    - Ganda Moola Dosha (born in critical nakshatras)
    - Kalathra Dosha (spouse-related affliction)
    - Ghata Dosha (obstacles)
    - Shrapit Dosha (Saturn-Rahu conjunction)

    Returns whether each dosha is present and detailed description with remedies.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_doshas()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
