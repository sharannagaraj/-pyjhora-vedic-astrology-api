"""Planetary strength calculation endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/strength", tags=["Strength"])

@router.post("/ashtakavarga", responses={400: {"model": ErrorResponse}})
async def calculate_ashtakavarga(request: ChartRequest):
    """
    Calculate Ashtakavarga (Bindus System)

    Ashtakavarga is a point system that shows benefic dots (bindus) in each house
    for each planet. It helps determine:
    - Which houses are strong for each planet
    - Which houses give favorable results
    - Overall strength distribution across the chart

    Returns:
    - Binna Ashtakavarga: Bindus for each planet in each house (12 houses)
    - Samudhaya Ashtakavarga: Combined bindus from all planets
    - Strongest and weakest houses
    - Total bindus count (should be ~337)
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_ashtakavarga()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/shadbala", responses={400: {"model": ErrorResponse}})
async def calculate_shadbala(request: ChartRequest):
    """
    Calculate Shadbala (Six-fold Planetary Strength)

    Shadbala measures planetary strength through six components:
    1. Sthana Bala (Positional strength)
    2. Dig Bala (Directional strength)
    3. Kala Bala (Temporal strength)
    4. Chesta Bala (Motional strength)
    5. Naisargika Bala (Natural strength)
    6. Drik Bala (Aspectual strength)

    Returns total strength for each planet in Shashtiamsas (1/60th of a sign).
    Higher values indicate stronger planets that give better results.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_shadbala()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bhava-bala", responses={400: {"model": ErrorResponse}})
async def calculate_bhava_bala(request: ChartRequest):
    """
    Calculate Bhava Bala (House Strength)

    Bhava Bala measures the strength of each of the 12 houses based on:
    - House lord strength
    - Planets aspecting the house
    - Planets occupying the house
    - Bhava Dig Bala (directional strength of houses)

    Returns strength values for all 12 houses.
    Stronger houses give better results in their significations.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_bhava_bala()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
