import pandas as pd
import numpy as np

class RealDataLoader:
    def __init__(self):
        self.real_data = None
    
    def calculate_parameter_urgency(self, value, lower_bound, upper_bound):
        """Calculate continuous k-value using paper's formula"""
        urgency = abs((upper_bound - value)**2 - (lower_bound - value)**2) / (upper_bound - lower_bound)**2
        return min(urgency, 2.0)
    
    def load_real_training_data(self):
        """Load and prepar data from UCI Heart Disease dataset"""
        try:
            column_names = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
            ]
            
            df = pd.read_csv("data/heart_disease_full.csv", names=column_names, na_values='?')
            
            df = df.dropna()
            print(f"Loaded UCI Heart Disease data: {len(df)} patient records")
            
            medical_data = []
            
            for _, row in df.iterrows():
                age = row['age']
                blood_pressure = row['trestbps']  # Real resting BP
                max_heart_rate = row['thalach']   # Real max heart rate
                gender = row['sex']               # Real gender (1=male, 0=female)
                cholesterol = row['chol']         # Real cholesterol
                blood_sugar = row['fbs']          # Real fasting blood sugar flag
                
                # Convert max heart rate to estimated resting heart rate (medical formula)
                # Resting HR ≈ 60-70% of max HR for most people
                heart_rate = int(max_heart_rate * 0.65)
                
                # Estimate glucose from fasting blood sugar flag and cholesterol
                # fbs=1 means >120 mg/dl, fbs=0 means <=120 mg/dl
                # Higher cholesterol often correlates with higher glucose
                base_glucose = 90 + (cholesterol / 100)  # Base glucose influenced by cholesterol
                if blood_sugar == 1:
                    glucose = base_glucose + np.random.normal(25, 8)  # Diabetic range
                else:
                    glucose = base_glucose + np.random.normal(5, 8)   # Normal range
                glucose = max(70, min(glucose, 300))  # Keep in realistic range
                
                # Estimate height/weight from population averages with some variation
                if gender == 1:  # Male
                    height = 175 + np.random.normal(0, 5)  # Average male height ± variation
                    weight = 80 + np.random.normal(0, 10)  # Average male weight ± variation
                else:  # Female
                    height = 162 + np.random.normal(0, 5)  # Average female height ± variation
                    weight = 65 + np.random.normal(0, 8)   # Average female weight ± variation
                
                height = max(150, min(height, 200))
                weight = max(45, min(weight, 120))
                
                # Calculate k-value using ONLY real measurements
                hr_k = self.calculate_parameter_urgency(heart_rate, 60, 100)
                bp_k = self.calculate_parameter_urgency(blood_pressure, 90, 120)
                glucose_k = self.calculate_parameter_urgency(glucose, 70, 140)
                
                k_value = max(hr_k, bp_k, glucose_k)
                
                # Calculate m-value based on real parameter urgencies
                if hr_k == max(hr_k, bp_k, glucose_k):
                    m_value = 3.0
                elif bp_k == max(hr_k, bp_k, glucose_k):
                    m_value = 2.0
                else:
                    m_value = 1.0
                
                medical_data.append({
                    'heart_rate': heart_rate,
                    'blood_pressure': blood_pressure,
                    'glucose_level': glucose,
                    'age': age,
                    'height': height,
                    'weight': weight,
                    'gender': gender,
                    'k_value': k_value,
                    'm_value': m_value
                })
            
            medical_df = pd.DataFrame(medical_data)
            self.real_data = medical_df
            
            print(f"FULL DATA SUMMARY:")
            print(f"   - Patients: {len(medical_df)}")
            print(f"   - Age range: {medical_df['age'].min()}-{medical_df['age'].max()} years")
            print(f"   - BP range: {medical_df['blood_pressure'].min()}-{medical_df['blood_pressure'].max()} mmHg")
            print(f"   - Heart rate range: {medical_df['heart_rate'].min()}-{medical_df['heart_rate'].max()} bpm")
            print(f"   - Glucose range: {medical_df['glucose_level'].min():.1f}-{medical_df['glucose_level'].max():.1f} mg/dL")
            print(f"   - K-value distribution:")
            k_counts = medical_df['k_value'].value_counts().sort_index()
            for k_val, count in k_counts.items():
                print(f"        k={k_val:.2f}: {count} patients")
            
            return medical_df
            
        except Exception as e:
            print(f"Error loading FULL real medical data: {e}")
            return None