# Dataset — UCI Heart Disease (Cleveland)

Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/45/heart+disease)  
303 patients, 13 features, binary target (0 = no disease, 1 = disease).

| Column | Type | Description |
|---|---|---|
| `age` | int | Age in years |
| `sex` | int | 1 = male, 0 = female |
| `cp` | int | Chest pain type: 0 = typical angina, 1 = atypical angina, 2 = non-anginal pain, 3 = asymptomatic |
| `trestbps` | int | Resting blood pressure (mm Hg on admission) |
| `chol` | int | Serum cholesterol (mg/dl) |
| `fbs` | int | Fasting blood sugar > 120 mg/dl: 1 = true, 0 = false |
| `restecg` | int | Resting ECG results: 0 = normal, 1 = ST-T wave abnormality, 2 = left ventricular hypertrophy |
| `thalach` | int | Maximum heart rate achieved |
| `exang` | int | Exercise-induced angina: 1 = yes, 0 = no |
| `oldpeak` | float | ST depression induced by exercise relative to rest |
| `slope` | int | Slope of peak exercise ST segment: 0 = upsloping, 1 = flat, 2 = downsloping |
| `ca` | int | Number of major vessels (0–3) coloured by fluoroscopy |
| `thal` | int | Thalassemia: 1 = normal, 2 = fixed defect, 3 = reversible defect |
| `target` | int | 0 = no heart disease, 1 = heart disease present |

## Notes

- The Cleveland subset is the most commonly used portion of the UCI dataset (303 rows).
- Some mirrors encode `ca` and `thal` with `?` for missing values — `load_data.py` handles normalisation.
- The original UCI target has values 0–4; `load_data.py` collapses anything > 0 to 1 for binary classification.
