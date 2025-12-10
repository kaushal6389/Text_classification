"""
FastAPI REST API for Multilingual Complaint Classifier
Provides endpoints for complaint classification in 11 languages
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from contextlib import asynccontextmanager
import pickle
import uvicorn
from datetime import datetime
import os

# Load model on startup using lifespan
model_artifacts = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup and cleanup on shutdown"""
    global model_artifacts
    try:
        model_path = os.getenv('MODEL_PATH', 'models/multilingual_classifier_improved.pkl')
        with open(model_path, 'rb') as f:
            model_artifacts = pickle.load(f)
        print(f"✓ Model loaded: {model_artifacts['model_name']}")
        print(f"  Accuracy: {model_artifacts['accuracy']*100:.2f}%")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise
    
    yield
    
    # Cleanup (if needed)
    print("Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="Multilingual Complaint Classifier API",
    description="Classify municipal complaints in 11 languages (English + 10 Indian languages)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ComplaintRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "The road has many potholes and needs repair"
            }
        }
    )
    
    text: str = Field(..., description="Complaint text in any supported language", min_length=1)

class BatchComplaintRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "texts": [
                    "Street light not working",
                    "सड़क पर गड्ढे हैं",
                    "கழிவு சேகரிக்கப்படவில்லை"
                ]
            }
        }
    )
    
    texts: List[str] = Field(..., description="List of complaint texts", min_length=1)

class PredictionResponse(BaseModel):
    category: str = Field(..., description="Predicted category")
    confidence: Optional[float] = Field(None, description="Prediction confidence (0-100)")
    all_probabilities: Optional[Dict[str, float]] = Field(None, description="All category probabilities")
    text: str = Field(..., description="Input text")
    timestamp: str = Field(..., description="Prediction timestamp")

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total: int
    timestamp: str

class ModelInfoResponse(BaseModel):
    model_name: str
    accuracy: float
    feature_count: int
    training_samples: int
    supported_languages: List[str]
    categories: List[str]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    timestamp: str

# Helper function
def predict_text(text: str) -> dict:
    """Predict category for a single text"""
    if not model_artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Vectorize
        vectorized = model_artifacts['vectorizer'].transform([text])
        
        # Predict
        prediction = model_artifacts['model'].predict(vectorized)[0]
        label = model_artifacts['label_encoder'].inverse_transform([prediction])[0]
        
        # Get probabilities
        result = {
            'category': label,
            'confidence': None,
            'all_probabilities': None
        }
        
        if hasattr(model_artifacts['model'], 'predict_proba'):
            proba = model_artifacts['model'].predict_proba(vectorized)[0]
            result['confidence'] = float(proba[prediction] * 100)
            
            # All probabilities
            result['all_probabilities'] = {
                model_artifacts['label_encoder'].classes_[i]: float(proba[i] * 100)
                for i in range(len(proba))
            }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Multilingual Complaint Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "model_info": "/model/info"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model_artifacts else "unhealthy",
        "model_loaded": model_artifacts is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def model_info():
    """Get model information"""
    if not model_artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_name": model_artifacts['model_name'],
        "accuracy": round(model_artifacts['accuracy'] * 100, 2),
        "feature_count": model_artifacts['feature_count'],
        "training_samples": model_artifacts['training_samples'],
        "supported_languages": [
            "English", "Hindi", "Bengali", "Marathi", "Telugu",
            "Tamil", "Gujarati", "Urdu", "Kannada", "Odia", "Malayalam"
        ],
        "categories": list(model_artifacts['label_encoder'].classes_)
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_complaint(request: ComplaintRequest):
    """
    Predict complaint category from text
    
    Supports 11 languages:
    - English
    - Hindi (हिन्दी)
    - Bengali (বাংলা)
    - Marathi (मराठी)
    - Telugu (తెలుగు)
    - Tamil (தமிழ்)
    - Gujarati (ગુજરાતી)
    - Urdu (اردو)
    - Kannada (ಕನ್ನಡ)
    - Odia (ଓଡ଼ିଆ)
    - Malayalam (മലയാളം)
    """
    result = predict_text(request.text)
    
    return {
        "category": result['category'],
        "confidence": result['confidence'],
        "all_probabilities": result['all_probabilities'],
        "text": request.text,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch_complaints(request: BatchComplaintRequest):
    """
    Predict categories for multiple complaints
    
    Process multiple complaint texts in a single request
    """
    predictions = []
    
    for text in request.texts:
        try:
            result = predict_text(text)
            predictions.append({
                "category": result['category'],
                "confidence": result['confidence'],
                "all_probabilities": result['all_probabilities'],
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            predictions.append({
                "category": "error",
                "confidence": None,
                "all_probabilities": None,
                "text": text,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            })
    
    return {
        "predictions": predictions,
        "total": len(predictions),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/categories", tags=["Reference"])
async def get_categories():
    """Get list of supported complaint categories"""
    if not model_artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    categories = list(model_artifacts['label_encoder'].classes_)
    
    return {
        "categories": categories,
        "descriptions": {
            "potholes": "Road damage and pothole complaints",
            "streetlight": "Street lighting and visibility issues",
            "garbage": "Waste collection and cleanliness problems",
            "others": "General municipal complaints"
        }
    }

@app.get("/languages", tags=["Reference"])
async def get_languages():
    """Get list of supported languages"""
    return {
        "total": 11,
        "languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "bn", "name": "Bengali", "native": "বাংলা"},
            {"code": "mr", "name": "Marathi", "native": "मराठी"},
            {"code": "te", "name": "Telugu", "native": "తెలుగు"},
            {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
            {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
            {"code": "ur", "name": "Urdu", "native": "اردو"},
            {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
            {"code": "ml", "name": "Malayalam", "native": "മലയാളം"}
        ]
    }

# Run the application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
