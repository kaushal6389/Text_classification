# Multilingual Municipal Complaint Classification API

🚀 **Production-Ready REST API** for classifying municipal complaints in **11 languages** using Machine Learning.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

## 🌟 Features

- **Multi-language Support**: English + 10 Indian languages (Hindi, Bengali, Marathi, Telugu, Tamil, Gujarati, Urdu, Kannada, Odia, Malayalam)
- **High Accuracy**: 96.76% classification accuracy using Gradient Boosting
- **4 Categories**: Potholes, Streetlight, Garbage, Others
- **Fast API**: Built with FastAPI for high performance
- **Production Ready**: Optimized for Railway deployment

## 🚀 Quick Deploy

### Deploy to Railway

1. **Fork this repository**
2. **Connect to Railway**:
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
   - Railway will auto-detect and deploy!

3. **Environment Variables** (Optional):
   ```
   PORT=8000
   MODEL_PATH=models/multilingual_classifier_improved.pkl
   ```

### Manual Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/multilingual-complaint-classifier.git
cd multilingual-complaint-classifier

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn api:app --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Base URL
```
https://your-app.railway.app
```

### Main Endpoints

#### 1. Health Check
```bash
GET /health
```

#### 2. Predict Single Complaint
```bash
POST /predict
Content-Type: application/json

{
  "text": "The road has many potholes"
}
```

**Response:**
```json
{
  "category": "potholes",
  "confidence": 99.8,
  "text": "The road has many potholes",
  "timestamp": "2025-12-10T14:30:00"
}
```

#### 3. Batch Predictions
```bash
POST /predict/batch
Content-Type: application/json

{
  "texts": [
    "Street light not working",
    "सड़क पर गड्ढे हैं",
    "கழிவு சேகரிக்கப்படவில்லை"
  ]
}
```

#### 4. Model Information
```bash
GET /model/info
```

#### 5. Supported Categories
```bash
GET /categories
```

#### 6. Supported Languages
```bash
GET /languages
```

## 📖 Interactive Documentation

Once deployed, visit:
- **Swagger UI**: `https://your-app.railway.app/docs`
- **ReDoc**: `https://your-app.railway.app/redoc`

## 🌐 Supported Languages

| Language | Code | Native Name |
|----------|------|-------------|
| English | en | English |
| Hindi | hi | हिन्दी |
| Bengali | bn | বাংলা |
| Marathi | mr | मराठी |
| Telugu | te | తెలుగు |
| Tamil | ta | தமிழ் |
| Gujarati | gu | ગુજરાતી |
| Urdu | ur | اردو |
| Kannada | kn | ಕನ್ನಡ |
| Odia | or | ଓଡ଼ିଆ |
| Malayalam | ml | മലയാളം |

## 🎯 Categories

1. **Potholes** - Road damage and pothole complaints
2. **Streetlight** - Street lighting issues
3. **Garbage** - Waste collection problems
4. **Others** - General municipal complaints

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **ML Model**: Gradient Boosting (scikit-learn)
- **Deployment**: Railway
- **Python**: 3.12+

## 📊 Model Performance

- **Accuracy**: 96.76%
- **Potholes**: 98.90% recall
- **Others**: 97.53% recall
- **Streetlight**: 95.24% recall
- **Garbage**: 95.18% recall

## 📁 Project Structure

```
multilingual-complaint-classifier/
├── api.py                          # FastAPI application
├── models/
│   └── multilingual_classifier_improved.pkl  # Trained model
├── data/
│   └── clean_dataset_multilingual_all.csv   # Dataset
├── requirements.txt                # Python dependencies
├── Procfile                        # Railway/Heroku config
├── railway.json                    # Railway config
├── .gitignore                      # Git ignore rules
└── README.md                       # Documentation
```

## 🔧 Development

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python api.py
# or
uvicorn api:app --reload
```

### Testing

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Test prediction
curl -X POST "https://your-app.railway.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Street light not working"}'
```

## 📝 Example Usage

### Python
```python
import requests

url = "https://your-app.railway.app/predict"
response = requests.post(url, json={"text": "सड़क पर गड्ढे हैं"})
print(response.json())
```

### JavaScript
```javascript
fetch('https://your-app.railway.app/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'Garbage not collected'})
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST "https://your-app.railway.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "The road needs repair"}'
```

## 🚦 Rate Limits

- No rate limits for open deployment
- For production, consider adding authentication and rate limiting

## 🔒 Security

- CORS enabled for all origins (configure for production)
- Input validation with Pydantic
- No authentication required (add for production use)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ for Municipal Services**

**Model Version**: 1.0  
**API Version**: 1.0.0  
**Last Updated**: December 10, 2025
