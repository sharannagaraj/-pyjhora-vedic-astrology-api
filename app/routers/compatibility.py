"""Marriage compatibility calculation endpoint"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import CompatibilityRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/compatibility", tags=["Compatibility"])

@router.post("/marriage", responses={400: {"model": ErrorResponse}})
async def calculate_marriage_compatibility(request: CompatibilityRequest):
    """
    Calculate Marriage Compatibility using Ashtakoota System

    The Ashtakoota (8-Kootas) system is the traditional Vedic method for assessing
    marriage compatibility. It evaluates 8 factors based on the birth nakshatras:

    **8 Kootas (Factors):**
    1. **Varna** (1 point): Spiritual compatibility, caste/class
    2. **Vasiya** (2 points): Mutual attraction, control
    3. **Tara** (3 points): Birth star compatibility, destiny
    4. **Yoni** (4 points): Sexual compatibility, nature
    5. **Graha Maitri** (5 points): Mental compatibility, friendship
    6. **Gana** (6 points): Temperament, behavior
    7. **Rasi/Bhakoot** (7 points): Love, prosperity
    8. **Nadi** (8 points): Health, progeny (most important)

    **Total Score: 36 points**
    - 28+: Excellent match
    - 24-27: Very good match
    - 18-23: Average match
    - Below 18: Not recommended

    **Important:** Nadi dosha (0 score in Nadi) is considered highly inauspicious
    and typically requires remedies or may indicate an unsuitable match.

    Returns detailed scores for each koota with overall compatibility rating.
    """
    try:
        result = PyJHoraCalculator.calculate_marriage_compatibility(
            request.boy_birth_data.dict(),
            request.girl_birth_data.dict(),
            request.ayanamsa
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
