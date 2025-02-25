from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from app.services.prediction import PredictionService
from app.models.prediction import PredictionRequest, PredictionResponse

router = APIRouter()
prediction_service = PredictionService()

@router.post("/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """
    Get price predictions for specified cryptocurrency
    """
    try:
        prediction = await prediction_service.predict(
            symbol=request.symbol,
            timeframe=request.timeframe,
            features=request.features
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols")
async def get_supported_symbols():
    """
    Get list of supported cryptocurrency symbols
    """
    try:
        symbols = await prediction_service.get_supported_symbols()
        return {"symbols": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
