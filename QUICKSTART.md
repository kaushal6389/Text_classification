# Multilingual Municipal Complaint Classification

## Quick Start Guide

### 1. Setup Environment

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Analyze Dataset

```powershell
python scripts/analyze_complete_multilingual.py
```

### 3. Train Model

```powershell
python scripts/train_improved_classifier.py
```

### 4. Make Predictions

```powershell
# Interactive mode
python scripts/predict.py

# Or use in your code:
```

```python
import pickle

# Load model
with open('models/multilingual_classifier_improved.pkl', 'rb') as f:
    model = pickle.load(f)

# Predict
text = "सड़क पर गड्ढे हैं"
vectorized = model['vectorizer'].transform([text])
prediction = model['model'].predict(vectorized)[0]
label = model['label_encoder'].inverse_transform([prediction])[0]

print(f"Category: {label}")
```

## Supported Languages

🇮🇳 **10 Indian Languages + English:**
- Hindi, Bengali, Marathi, Telugu, Tamil
- Gujarati, Urdu, Kannada, Odia, Malayalam

## Categories

1. **Potholes** - Road damage complaints
2. **Streetlight** - Lighting issues
3. **Garbage** - Waste collection problems
4. **Others** - General complaints

## Performance

- **Accuracy**: 96.76%
- **Model**: Gradient Boosting
- **Features**: 10,000 (character n-grams)

## Files

- `data/clean_dataset_multilingual_all.csv` - Complete dataset
- `models/multilingual_classifier_improved.pkl` - Trained model
- `scripts/predict.py` - Prediction script
- `scripts/train_improved_classifier.py` - Training script

## Help

For detailed documentation, see [README.md](README.md)
