import numpy as np
import sys
import os
from sklearn.ensemble import RandomForestRegressor

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.models import HealthTask, Patient

class PriorityCalculator:
    def __init__(self):
        # Normal ranges for general patients (taken from www.heart.org and www.medscape.com)
        self.normal_ranges = {
            'heart_rate': (60, 100),      # bpm
            'blood_pressure': (90, 120),   # mmHg
            'glucose_level': (70, 140)     # mg/dL
        }
        
        # Parameter weights for m-value (urgency hierarchy/tie breaking mechanism)
        self.parameter_weights = {
            'heart_rate': 3.0,
            'blood_pressure': 2.0,
            'glucose_level': 1.0
        }
        
        # ML models for specific patients
        self.ml_model_k = None
        self.ml_model_m = None
        self.train_ml_models()
    
    def train_ml_models(self):
        """Train ML models using medical data"""
        try:
            # Import our real data loader
            from src.real_data_loader import RealDataLoader
            
            # Load real medical data
            data_loader = RealDataLoader()
            real_data = data_loader.load_real_training_data()
            
            # Prepare features for ML model
            feature_columns = ['heart_rate', 'blood_pressure', 'glucose_level', 'age', 'height', 'weight', 'gender']
            X = real_data[feature_columns].values
            
            # Use calculated k and m values
            y_k = real_data['k_value'].values
            y_m = real_data['m_value'].values
            
            # Train models with real medical patterns
            self.ml_model_k = RandomForestRegressor(n_estimators=100, random_state=42)
            self.ml_model_m = RandomForestRegressor(n_estimators=100, random_state=42)
            
            self.ml_model_k.fit(X, y_k)
            self.ml_model_m.fit(X, y_m)
            
        except Exception as e:
            print(f"Error in real data training: {e}")  
    
    def _calculate_parameter_urgency(self, value: float, lower_bound: float, upper_bound: float) -> float:
        """Calculate urgency for a single parameter using research paper's formula"""
        # Research Paper's urgency formula: |(ub - value)² - (lb - value)²| / (ub - lb)²
        urgency = abs((upper_bound - value)**2 - (lower_bound - value)**2) / (upper_bound - lower_bound)**2
        return min(urgency, 2.0)  # Cap at 2.0
    
    def calculate_general_priority(self, task: HealthTask) -> tuple[float, float]:
        """Calculate priority for general patient type using rule-based approach"""
        # Calculate k-value for each parameter
        hr_k = self._calculate_parameter_urgency(
            task.heart_rate, *self.normal_ranges['heart_rate']
        )
        bp_k = self._calculate_parameter_urgency(
            task.blood_pressure, *self.normal_ranges['blood_pressure']
        )
        glucose_k = self._calculate_parameter_urgency(
            task.glucose_level, *self.normal_ranges['glucose_level']
        )
        
        # k-value is maximum of all parameter urgencies
        k_value = max(hr_k, bp_k, glucose_k)
        
        # Calculate m-value based on most critical parameter
        urgencies = {
            'heart_rate': hr_k,
            'blood_pressure': bp_k,
            'glucose_level': glucose_k
        }
        
        most_critical = max(urgencies, key=urgencies.get)
        m_value = self.parameter_weights[most_critical]
        
        return k_value, m_value
    
    def calculate_specific_priority(self, task: HealthTask, patient: Patient) -> tuple[float, float]:
        """Calculate priority for specific patient type using ML model"""
        # Prepare features for ML model
        features = np.array([[
            task.heart_rate,
            task.blood_pressure,
            task.glucose_level,
            patient.age,
            patient.height,
            patient.weight,
            1 if patient.gender == 'M' else 0
        ]])
        
        k_value = float(self.ml_model_k.predict(features)[0])
        m_value = float(self.ml_model_m.predict(features)[0])
        
        # Ensure k-value is in [0, 2] range
        k_value = max(0.0, min(k_value, 2.0))
        
        return k_value, m_value
    
    def calculate_task_priority(self, task: HealthTask, patient: Patient) -> HealthTask:
        """Calculate priority values for a task based on patient type"""
        if task.task_type == 'general':
            k_value, m_value = self.calculate_general_priority(task)
        else:
            k_value, m_value = self.calculate_specific_priority(task, patient)
        
        task.k_value = k_value
        task.m_value = m_value
        return task