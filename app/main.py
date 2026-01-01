"""FastAPI main application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import charts, dashas, yogas, doshas, strength, panchanga, compatibility, special, transits, comprehensive

# Create FastAPI app
app = FastAPI(
    title="PyJHora Vedic Astrology API",
    description="RESTful API for Vedic astrology calculations using PyJHora library",
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(comprehensive.router)  # Comprehensive endpoint (all-in-one)
app.include_router(charts.router)
app.include_router(dashas.router)
app.include_router(yogas.router)
app.include_router(doshas.router)
app.include_router(strength.router)
app.include_router(panchanga.router)
app.include_router(compatibility.router)
app.include_router(special.router)
app.include_router(transits.router)

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "PyJHora Vedic Astrology API",
        "version": "1.2.0",
        "description": "RESTful API for Vedic astrology calculations",
        "documentation": "/docs",
        "endpoints": {
            "comprehensive": "/api/v1/comprehensive/full-analysis",
            "charts": "/api/v1/charts",
            "dashas": "/api/v1/dashas",
            "yogas": "/api/v1/yogas",
            "doshas": "/api/v1/doshas",
            "strength": "/api/v1/strength",
            "panchanga": "/api/v1/panchanga",
            "compatibility": "/api/v1/compatibility",
            "special": "/api/v1/special",
            "transits": "/api/v1/transits"
        },
        "new_in_v1.2": [
            "Comprehensive endpoint - All data in one API call (D1/D9/D10, Dashas, Ashtakavarga, Yogas, Doshas)"
        ],
        "new_in_v1.1": [
            "Transit analysis (current positions, Sade Sati, planet entries)",
            "Extended Panchanga (Rahu Kaal, Yamaganda, Gulika, Abhijit Muhurta)"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pyjhora-api"
    }

@app.get("/api/v1/ayanamsa/list")
async def list_ayanamsa_systems():
    """List available Ayanamsa systems"""
    return {
        "status": "success",
        "ayanamsa_systems": [
            "LAHIRI",
            "KP",
            "TRUE_CITRA",
            "SURYA_SIDDHANTA",
            "RAMAN",
            "USHASHASHI",
            "KRISHNAMURTI",
            "YUKTESHWAR"
        ],
        "default": "LAHIRI",
        "note": "Lahiri is most commonly used in Indian Vedic astrology"
    }

@app.get("/api/v1/charts/types")
async def list_chart_types():
    """List available divisional chart types"""
    return {
        "status": "success",
        "chart_types": {
            "D1": "Rasi (Birth Chart)",
            "D2": "Hora (Wealth)",
            "D3": "Drekkana (Siblings)",
            "D4": "Chaturthamsa (Property)",
            "D7": "Saptamsa (Children)",
            "D9": "Navamsa (Marriage/Spouse)",
            "D10": "Dasamsa (Career)",
            "D12": "Dwadasamsa (Parents)",
            "D16": "Shodasamsa (Vehicles)",
            "D20": "Vimsamsa (Spirituality)",
            "D24": "Chaturvimsamsa (Education)",
            "D27": "Nakshatramsa (Strengths)",
            "D30": "Trimsamsa (Misfortunes)",
            "D60": "Shashtyamsa (Past Life)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
