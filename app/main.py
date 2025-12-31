"""FastAPI main application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import charts, dashas

# Create FastAPI app
app = FastAPI(
    title="PyJHora Vedic Astrology API",
    description="RESTful API for Vedic astrology calculations using PyJHora library",
    version="1.0.0",
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
app.include_router(charts.router)
app.include_router(dashas.router)

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "PyJHora Vedic Astrology API",
        "version": "1.0.0",
        "description": "RESTful API for Vedic astrology calculations",
        "documentation": "/docs",
        "endpoints": {
            "charts": "/api/v1/charts",
            "dashas": "/api/v1/dashas"
        }
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
