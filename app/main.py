from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Fluxion",
    description="Advanced AI-powered cryptocurrency market prediction platform",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api.routes import prediction, sentiment, portfolio, risk

# Include routers
app.include_router(prediction.router, prefix="/api/v1", tags=["predictions"])
app.include_router(sentiment.router, prefix="/api/v1", tags=["sentiment"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["portfolio"])
app.include_router(risk.router, prefix="/api/v1", tags=["risk"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Fluxion API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
