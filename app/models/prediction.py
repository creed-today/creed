from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    symbol: str  # e.g., "BTC/USDT"
    timeframe: str = "1h"  # e.g., "1h", "4h", "1d"
    features: Optional[List[str]] = None  # Optional technical indicators to include

class PricePoint(BaseModel):
    timestamp: datetime
    price: float
    confidence: float

class PredictionResponse(BaseModel):
    symbol: str
    timeframe: str
    predictions: List[PricePoint]
    model_version: str
    generated_at: datetime
    performance_metrics: dict
