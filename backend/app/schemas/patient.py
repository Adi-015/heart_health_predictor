from pydantic import BaseModel, Field
from typing import List


class PatientInput(BaseModel):
    age:      int   = Field(..., ge=1,   le=120,  description="Age in years")
    sex:      int   = Field(..., ge=0,   le=1,    description="0=female, 1=male")
    cp:       int   = Field(..., ge=0,   le=3,    description="Chest pain type (0-3)")
    trestbps: int   = Field(..., ge=50,  le=250,  description="Resting blood pressure (mm Hg)")
    chol:     int   = Field(..., ge=100, le=600,  description="Serum cholesterol (mg/dl)")
    fbs:      int   = Field(..., ge=0,   le=1,    description="Fasting blood sugar >120 mg/dl: 1=true")
    restecg:  int   = Field(..., ge=0,   le=2,    description="Resting ECG (0=normal, 1=ST-T abnormality, 2=LVH)")
    thalach:  int   = Field(..., ge=60,  le=250,  description="Max heart rate achieved")
    exang:    int   = Field(..., ge=0,   le=1,    description="Exercise-induced angina: 1=yes")
    oldpeak:  float = Field(..., ge=0.0, le=10.0, description="ST depression (exercise vs rest)")
    slope:    int   = Field(..., ge=0,   le=2,    description="Slope of peak exercise ST (0=up, 1=flat, 2=down)")
    ca:       int   = Field(..., ge=0,   le=3,    description="Major vessels coloured by fluoroscopy (0-3)")
    thal:     int   = Field(..., ge=1,   le=3,    description="Thalassemia: 1=normal, 2=fixed defect, 3=reversible")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 54, "sex": 1, "cp": 0, "trestbps": 140,
                "chol": 239, "fbs": 0, "restecg": 1, "thalach": 160,
                "exang": 0, "oldpeak": 1.2, "slope": 1, "ca": 0, "thal": 2
            }
        }
    }


class SHAPFactor(BaseModel):
    feature: str
    impact:  float


class PredictionResponse(BaseModel):
    risk_label:  str
    probability: float
    top_factors: List[SHAPFactor]
