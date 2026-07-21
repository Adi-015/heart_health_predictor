// Maps one-hot encoded SHAP feature names to human-readable labels.
// Encoding based on the CSV mirror used for training — see data/README.md.
const LABELS = {
  // Chest pain type
  cp_0: 'Chest Pain: Typical Angina',
  cp_1: 'Chest Pain: Atypical Angina',
  cp_2: 'Chest Pain: Non-anginal',
  cp_3: 'Chest Pain: Asymptomatic',

  // Resting ECG
  restecg_0: 'Resting ECG: Normal',
  restecg_1: 'Resting ECG: ST-T Abnormality',
  restecg_2: 'Resting ECG: LV Hypertrophy',

  // Exercise-induced angina
  exang_0: 'Exercise Angina: No',
  exang_1: 'Exercise Angina: Yes',

  // ST slope
  slope_0: 'ST Slope: Upsloping',
  slope_1: 'ST Slope: Flat',
  slope_2: 'ST Slope: Downsloping',

  // Major vessels (fluoroscopy)
  ca_0: 'Major Vessels Blocked: 0',
  ca_1: 'Major Vessels Blocked: 1',
  ca_2: 'Major Vessels Blocked: 2',
  ca_3: 'Major Vessels Blocked: 3',
  ca_4: 'Major Vessels Blocked: 4',

  // Thalassemia (thallium stress test)
  thal_0: 'Thalassemia: Unknown',
  thal_1: 'Thalassemia: Normal',
  thal_2: 'Thalassemia: Reversible Defect',
  thal_3: 'Thalassemia: Fixed Defect',

  // Numeric features — keep readable as-is
  age:      'Age',
  trestbps: 'Resting Blood Pressure',
  chol:     'Cholesterol',
  thalach:  'Max Heart Rate',
  oldpeak:  'ST Depression',

  // Binary features
  sex_0: 'Sex: Female',
  sex_1: 'Sex: Male',
  fbs_0: 'Fasting Blood Sugar: Normal',
  fbs_1: 'Fasting Blood Sugar: High',
}

export function labelFeature(raw) {
  return LABELS[raw] ?? raw
}
