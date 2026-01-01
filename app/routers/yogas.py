"""Yoga calculation endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/yogas", tags=["Yogas"])

@router.post("/", responses={400: {"model": ErrorResponse}})
async def calculate_yogas(request: ChartRequest):
    """
    Calculate All Yogas in Birth Chart

    Detects 100+ planetary yogas including:
    - Pancha Mahapurusha Yogas (Hamsa, Malavya, Sasa, Ruchaka, Bhadra)
    - Raja Yogas (Kesari, Gaja Kesari, etc.)
    - Chandra Yogas (Sunaphaa, Anaphaa, Duradhara, etc.)
    - Dhana Yogas (wealth combinations)
    - And many more...

    Returns yoga name, description, effects, and which divisional chart it appears in.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_yogas()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
