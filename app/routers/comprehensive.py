"""Comprehensive analysis endpoint - All data in one call"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/comprehensive", tags=["Comprehensive Analysis"])

@router.post("/full-analysis", responses={400: {"model": ErrorResponse}})
async def get_full_analysis(request: ChartRequest):
    """
    Get Complete Vedic Astrology Analysis in One Call

    Returns:
    - D1 Chart (Rasi) with houses, planets, degrees
    - D9 Chart (Navamsa) with houses, planets, degrees
    - D10 Chart (Dasamsa) with houses, planets, degrees
    - Maha Dasha (9 planetary periods)
    - Antardasha/Bhukti (81 sub-periods)
    - 7 Bhinna Ashtakavarga charts (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
    - Sarvashtakavarga (Combined chart)
    - All Yogas (planetary combinations)
    - All Doshas (afflictions)

    This endpoint combines all major calculations into a single response.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )

        # Calculate D1, D9, D10 charts
        d1_chart = calculator.calculate_chart('D1')
        d9_chart = calculator.calculate_chart('D9')
        d10_chart = calculator.calculate_chart('D10')

        # Calculate Maha Dasha
        maha_dasha = calculator.calculate_dasha('VIMSOTTARI')

        # Calculate Antardasha (Bhukti)
        antardasha = calculator.calculate_dasha_bhukti('VIMSOTTARI')

        # Calculate Ashtakavarga (7 Bhinna + 1 Sarva)
        ashtakavarga = calculator.calculate_ashtakavarga()

        # Calculate Yogas
        yogas = calculator.calculate_yogas()

        # Calculate Doshas
        doshas = calculator.calculate_doshas()

        # Compile comprehensive response
        response = {
            "status": "success",
            "birth_data": request.birth_data.dict(),
            "ayanamsa": request.ayanamsa,

            "charts": {
                "d1_rasi": {
                    "name": "D1 - Rasi (Birth Chart)",
                    "ascendant": d1_chart['ascendant'],
                    "planets": d1_chart['planets']
                },
                "d9_navamsa": {
                    "name": "D9 - Navamsa (Marriage/Spouse)",
                    "ascendant": d9_chart['ascendant'],
                    "planets": d9_chart['planets']
                },
                "d10_dasamsa": {
                    "name": "D10 - Dasamsa (Career)",
                    "ascendant": d10_chart['ascendant'],
                    "planets": d10_chart['planets']
                }
            },

            "dashas": {
                "maha_dasha": {
                    "system": "Vimsottari",
                    "moon_nakshatra": maha_dasha.get('moon_nakshatra'),
                    "periods": maha_dasha.get('maha_dasha_periods', []),
                    "current_period": maha_dasha.get('current_dasha')
                },
                "antardasha": {
                    "system": "Vimsottari",
                    "total_periods": len(antardasha.get('bhukti_periods', [])),
                    "periods": antardasha.get('bhukti_periods', []),
                    "current_period": antardasha.get('current_bhukti')
                }
            },

            "ashtakavarga": {
                "bhinna_ashtakavarga": {
                    "description": "7 Individual Planet Charts (Bindu strength by house)",
                    "planets": ashtakavarga.get('binna_ashtakavarga', {})
                },
                "sarvashtakavarga": {
                    "description": "Combined Ashtakavarga (Total strength across all planets)",
                    "data": ashtakavarga.get('samudhaya_ashtakavarga', {})
                }
            },

            "yogas": {
                "total_analyzed": len(yogas.get('yogas', [])),
                "total_present": sum(1 for y in yogas.get('yogas', []) if y.get('present', False)),
                "present_yogas": [y for y in yogas.get('yogas', []) if y.get('present', False)],
                "all_yogas": yogas.get('yogas', [])
            },

            "doshas": {
                "total_analyzed": len(doshas.get('doshas', [])),
                "total_present": sum(1 for d in doshas.get('doshas', []) if d.get('present', False)),
                "present_doshas": [d for d in doshas.get('doshas', []) if d.get('present', False)],
                "all_doshas": doshas.get('doshas', [])
            },

            "summary": {
                "charts_calculated": ["D1 Rasi", "D9 Navamsa", "D10 Dasamsa"],
                "maha_dasha_periods": len(maha_dasha.get('maha_dasha_periods', [])),
                "antardasha_periods": len(antardasha.get('bhukti_periods', [])),
                "bhinna_ashtakavarga_planets": 7,
                "yogas_present": sum(1 for y in yogas.get('yogas', []) if y.get('present', False)),
                "doshas_present": sum(1 for d in doshas.get('doshas', []) if d.get('present', False)),
                "current_maha_dasha": maha_dasha.get('current_dasha', {}).get('lord') if maha_dasha.get('current_dasha') else None,
                "strongest_planet_ashtakavarga": max(
                    ashtakavarga.get('binna_ashtakavarga', {}).items(),
                    key=lambda x: x[1].get('total', 0)
                )[0] if ashtakavarga.get('binna_ashtakavarga') else None
            }
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
