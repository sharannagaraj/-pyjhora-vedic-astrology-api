"""Special calculations endpoints (Lagnas and Bhava Bala)"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/special", tags=["Special Calculations"])

@router.post("/lagnas", responses={400: {"model": ErrorResponse}})
async def calculate_special_lagnas(request: ChartRequest):
    """
    Calculate Special Lagnas (Ascendants)

    Special Lagnas are sensitive points calculated for specific purposes:

    **7 Special Lagnas:**
    1. **Hora Lagna**: Wealth and financial matters
       - Used for wealth analysis and financial timing

    2. **Ghati Lagna**: Timing and general fortune
       - Indicates overall fortune and auspicious timing

    3. **Bhava Lagna**: Mental disposition and temperament
       - Shows mental state and psychological nature

    4. **Sree Lagna** (Sri Lagna): Prosperity and overall well-being
       - Most important for wealth and prosperity analysis

    5. **Pranapada Lagna**: Longevity and life force
       - Indicates vitality, health, and life span

    6. **Indu Lagna**: Wealth from inheritance and family
       - Shows inherited wealth and family fortune

    7. **Bhrigu Bindhu Lagna**: Past life karma and spirituality
       - Indicates spiritual progress and karmic patterns

    Each lagna is calculated based on specific planetary positions and time.
    Returns sign, degree, and significance for each lagna.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )
        result = calculator.calculate_special_lagnas()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bhava-bala", responses={400: {"model": ErrorResponse}})
async def calculate_bhava_bala(request: ChartRequest):
    """
    Calculate Bhava Bala (House Strength)

    Bhava Bala measures the strength of each of the 12 houses in the chart.
    Stronger houses give better results for matters related to that house.

    **House Significations:**
    - **1st:** Self, body, personality
    - **2nd:** Wealth, family, speech
    - **3rd:** Siblings, courage, communication
    - **4th:** Mother, home, property
    - **5th:** Children, education, intelligence
    - **6th:** Enemies, diseases, service
    - **7th:** Spouse, partnerships, business
    - **8th:** Longevity, transformation, occult
    - **9th:** Father, luck, religion, higher learning
    - **10th:** Career, status, authority
    - **11th:** Gains, friends, aspirations
    - **12th:** Losses, spirituality, foreign lands

    **Strength Components:**
    - Bhava Adhipati Bala (house lord strength)
    - Bhava Dig Bala (directional strength)
    - Bhava Drik Bala (aspectual strength)

    Returns total strength for each house with strongest/weakest identification.
    Higher strength = Better results from that house.
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
