import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
import ccxt
import ta
from app.models.prediction import PricePoint, PredictionResponse
from app.core.config import get_settings

class PredictionService:
    def __init__(self):
        self.settings = get_settings()
        self.exchange = ccxt.binance({
            'apiKey': self.settings.BINANCE_API_KEY,
            'secret': self.settings.BINANCE_API_SECRET
        })
         
    async def predict(self, symbol: str, timeframe: str = "1h", features: Optional[List[str]] = None) -> PredictionResponse:
        """
        Generate price predictions for the specified cryptocurrency
        """
        # Fetch historical data
        ohlcv = self.fetch_historical_data(symbol, timeframe)
        df = self.prepare_features(ohlcv, features)
        
        # Generate predictions
        predictions = self.generate_predictions(df)
        
        # Calculate confidence scores
        confidence_scores = self.calculate_confidence(df, predictions)
        
        # Prepare response
        price_points = []
        for i, pred in enumerate(predictions):
            timestamp = datetime.now() + timedelta(hours=i+1)
            price_points.append(PricePoint(
                timestamp=timestamp,
                price=float(pred),
                confidence=float(confidence_scores[i])
            ))
        
        return PredictionResponse(
            symbol=symbol,
            timeframe=timeframe,
            predictions=price_points,
            model_version="1.0.0",
            generated_at=datetime.now(),
            performance_metrics=self.get_performance_metrics()
        )
    
    def fetch_historical_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """
        Fetch historical OHLCV data from Binance
        """
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=1000)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    
    def prepare_features(self, df: pd.DataFrame, features: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Prepare technical indicators and features for prediction
        """
        if features is None:
            features = ['rsi', 'macd', 'bbands']
            
        # Add technical indicators
        if 'rsi' in features:
            df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
        if 'macd' in features:
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
        if 'bbands' in features:
            bb = ta.volatility.BollingerBands(df['close'])
            df['bb_high'] = bb.bollinger_hband()
            df['bb_low'] = bb.bollinger_lband()
            
        return df.dropna()
    
    def generate_predictions(self, df: pd.DataFrame) -> np.ndarray:
        """
        Generate price predictions using the trained model
        TODO: Implement actual model prediction
        """
        # Placeholder: Return simple moving average as prediction
        last_price = df['close'].iloc[-1]
        return np.array([last_price * (1 + np.random.normal(0, 0.01)) for _ in range(24)])
    
    def calculate_confidence(self, df: pd.DataFrame, predictions: np.ndarray) -> np.ndarray:
        """
        Calculate confidence scores for predictions
        TODO: Implement actual confidence calculation
        """
        # Placeholder: Return random confidence scores
        return np.random.uniform(0.6, 0.9, len(predictions))
    
    def get_performance_metrics(self) -> dict:
        """
        Get model performance metrics
        TODO: Implement actual performance metrics calculation
        """
        return {
            "mae": 0.02,
            "rmse": 0.03,
            "accuracy": 0.85
        }
    
    async def get_supported_symbols(self) -> List[str]:
        """
        Get list of supported cryptocurrency symbols
        """
        markets = self.exchange.load_markets()
        # 优先返回主要交易对
        priority_pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
        all_pairs = [symbol for symbol in markets.keys() if symbol.endswith('/USDT')]
        # 确保优先交易对在列表前面
        return sorted(all_pairs, key=lambda x: (x not in priority_pairs, x))
