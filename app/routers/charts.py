"""Chart calculation endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ChartResponse, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/charts", tags=["Charts"])

@router.post("/rasi", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_rasi_chart(request: ChartRequest):
    """
    Calculate D1 Rasi (Birth) Chart

    Returns planet positions, ascendant, and house placements for the birth chart.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_chart("D1")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/navamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_navamsa_chart(request: ChartRequest):
    """
    Calculate D9 Navamsa Chart

    Returns planet positions in the Navamsa chart (marriage/spouse chart).
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_chart("D9")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dasamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_dasamsa_chart(request: ChartRequest):
    """
    Calculate D10 Dasamsa Chart

    Returns planet positions in the Dasamsa chart (career/profession chart).
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_chart("D10")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/divisional", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_divisional_chart(request: ChartRequest):
    """
    Calculate Any Divisional Chart

    Supports: D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D60
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        chart_type = request.chart_type or "D1"
        result = calculator.calculate_chart(chart_type.upper())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/house-wise/{chart_type}")
async def calculate_house_wise_chart(chart_type: str, request: ChartRequest):
    """
    Calculate House-Wise Planetary Placement

    Returns planets organized by houses for any divisional chart.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_house_wise(chart_type.upper())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
