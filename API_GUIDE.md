# FastAPI Deployment Guide

## Starting the API Server

### Method 1: Direct Run
```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Start the API server
python api.py
```

### Method 2: Using Uvicorn
```powershell
.\venv\Scripts\activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Main URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Endpoints

### 🏥 Health & Info

#### `GET /health`
Check API health status
```bash
curl http://localhost:8000/health
```

#### `GET /model/info`
Get model information and performance metrics
```bash
curl http://localhost:8000/model/info
```

---

### 🔮 Prediction Endpoints

#### `POST /predict`
Classify a single complaint

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The road has many potholes\"}"
```

**Response:**
```json
{
  "category": "potholes",
  "confidence": 99.8,
  "all_probabilities": {
    "potholes": 99.8,
    "streetlight": 0.1,
    "garbage": 0.05,
    "others": 0.05
  },
  "text": "The road has many potholes",
  "timestamp": "2025-12-10T14:30:00"
}
```

#### `POST /predict/batch`
Classify multiple complaints at once

**Request:**
```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d "{\"texts\": [\"Street light broken\", \"सड़क पर गड्ढे हैं\"]}"
```

---

### 📚 Reference Endpoints

#### `GET /categories`
Get supported complaint categories
```bash
curl http://localhost:8000/categories
```

#### `GET /languages`
Get list of supported languages
```bash
curl http://localhost:8000/languages
```

---

## Testing the API

### Using Python Test Script
```powershell
.\venv\Scripts\activate
python test_api.py
```

### Using PowerShell
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# Single prediction
$body = @{text = "Garbage not collected"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json"
```

### Using Python
```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "Street light not working"}
)
print(response.json())
```

---

## Example Use Cases

### Example 1: English Complaint
```json
POST /predict
{
  "text": "The streetlight in our area has been broken for weeks"
}

Response:
{
  "category": "streetlight",
  "confidence": 98.5,
  "timestamp": "2025-12-10T14:30:00"
}
```

### Example 2: Hindi Complaint
```json
POST /predict
{
  "text": "सड़क पर बहुत गड्ढे हैं और मरम्मत की जरूरत है"
}

Response:
{
  "category": "potholes",
  "confidence": 97.2
}
```

### Example 3: Batch Prediction
```json
POST /predict/batch
{
  "texts": [
    "Road is full of potholes",
    "कचरा नहीं उठाया गया",
    "தெரு விளக்கு வேலை செய்யவில்லை"
  ]
}

Response:
{
  "predictions": [...],
  "total": 3
}
```

---

## Production Deployment

### Using Uvicorn with Workers
```powershell
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (Linux/Mac)
```bash
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t complaint-classifier .
docker run -p 8000:8000 complaint-classifier
```

---

## Performance Tips

1. **Enable caching** for repeated requests
2. **Use batch endpoint** for multiple predictions
3. **Deploy with multiple workers** for production
4. **Add rate limiting** to prevent abuse
5. **Monitor response times** and model performance

---

## Security Considerations

- Add API key authentication for production
- Implement rate limiting
- Enable HTTPS in production
- Validate input text length and content
- Add logging and monitoring

---

## Troubleshooting

### Model not loading
- Check if `models/multilingual_classifier_improved.pkl` exists
- Ensure the file path is correct relative to `api.py`

### Port already in use
```powershell
# Kill process on port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### CORS errors
- Check CORS middleware configuration in `api.py`
- Ensure allowed origins are correctly set

---

## API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can:
- Test all endpoints directly
- See request/response schemas
- View example requests
- Download OpenAPI specification

---

**API Version**: 1.0.0  
**Model Accuracy**: 96.76%  
**Supported Languages**: 11
