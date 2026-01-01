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

@router.post("/hora", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_hora_chart(request: ChartRequest):
    """
    Calculate D2 Hora Chart

    Returns planet positions in the Hora chart (wealth/money chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D2")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/drekkana", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_drekkana_chart(request: ChartRequest):
    """
    Calculate D3 Drekkana Chart

    Returns planet positions in the Drekkana chart (siblings/courage chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D3")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chaturthamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_chaturthamsa_chart(request: ChartRequest):
    """
    Calculate D4 Chaturthamsa Chart

    Returns planet positions in the Chaturthamsa chart (property/assets chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D4")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/saptamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_saptamsa_chart(request: ChartRequest):
    """
    Calculate D7 Saptamsa Chart

    Returns planet positions in the Saptamsa chart (children/progeny chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D7")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dwadasamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_dwadasamsa_chart(request: ChartRequest):
    """
    Calculate D12 Dwadasamsa Chart

    Returns planet positions in the Dwadasamsa chart (parents chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D12")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/shodasamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_shodasamsa_chart(request: ChartRequest):
    """
    Calculate D16 Shodasamsa Chart

    Returns planet positions in the Shodasamsa chart (vehicles/comforts chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D16")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/vimsamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_vimsamsa_chart(request: ChartRequest):
    """
    Calculate D20 Vimsamsa Chart

    Returns planet positions in the Vimsamsa chart (spiritual practices chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D20")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chaturvimsamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_chaturvimsamsa_chart(request: ChartRequest):
    """
    Calculate D24 Chaturvimsamsa Chart

    Returns planet positions in the Chaturvimsamsa chart (education/learning chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D24")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/nakshatramsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_nakshatramsa_chart(request: ChartRequest):
    """
    Calculate D27 Nakshatramsa Chart

    Returns planet positions in the Nakshatramsa chart (strengths/weaknesses chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D27")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/trimsamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_trimsamsa_chart(request: ChartRequest):
    """
    Calculate D30 Trimsamsa Chart

    Returns planet positions in the Trimsamsa chart (evils/misfortunes chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D30")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/khavedamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_khavedamsa_chart(request: ChartRequest):
    """
    Calculate D40 Khavedamsa Chart

    Returns planet positions in the Khavedamsa chart (auspicious/inauspicious chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D40")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/akshavedamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_akshavedamsa_chart(request: ChartRequest):
    """
    Calculate D45 Akshavedamsa Chart

    Returns planet positions in the Akshavedamsa chart (general indications chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D45")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/shashtyamsa", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_shashtyamsa_chart(request: ChartRequest):
    """
    Calculate D60 Shashtyamsa Chart

    Returns planet positions in the Shashtyamsa chart (past life/karma chart).
    """
    try:
        calculator = PyJHoraCalculator(request.birth_data.dict(), request.ayanamsa)
        return calculator.calculate_chart("D60")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/divisional", response_model=ChartResponse, responses={400: {"model": ErrorResponse}})
async def calculate_divisional_chart(request: ChartRequest):
    """
    Calculate Any Divisional Chart

    Supports: D1-D60 (all divisional charts)
    Specify chart_type in request body (e.g., "D1", "D9", "D60")
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
