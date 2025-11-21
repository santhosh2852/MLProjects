from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and vectorizer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

model = None
vectorizer = None

@app.on_event("startup")
def load_model():
    global model, vectorizer
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("Model and vectorizer loaded successfully.")
        else:
            print("Model artifacts not found. Please run train_model.py first.")
    except Exception as e:
        print(f"Error loading model: {e}")

class EmailRequest(BaseModel):
    message: str

@app.post("/predict")
def predict_spam(request: EmailRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Transform input
    input_data = vectorizer.transform([request.message])
    
    # Predict
    prediction = model.predict(input_data)
    
    # 1 = Ham, 0 = Spam (based on training script)
    result = "Ham" if prediction[0] == 1 else "Spam"
    
    return {"prediction": result, "is_spam": int(prediction[0]) == 0}

@app.get("/")
def read_root():
    return {"message": "Spam Prediction API is running"}
