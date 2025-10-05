from dataclasses import dataclass
import pandas as pd

@dataclass
class Patient:
    patient_id: str
    type: str  # 'general' or 'specific'
    age: int
    height: float  # in cm
    weight: float  # in kg
    gender: str    # 'M' or 'F'

@dataclass
class HealthTask:
    patient_id: str
    heart_rate: int
    blood_pressure: int
    glucose_level: float
    task_type: str
    k_value: float = 0.0
    m_value: float = 0.0
    timestamp: float = 0.0
    edge_device_id: int = 0

class PatientDatabase:
    def __init__(self):
        self.patients = {}
    
    def load_patients_from_csv(self, csv_file_path: str, edge_device_id: int):
        """Load patients from CSV file for a specific edge device"""
        try:
            df = pd.read_csv(csv_file_path)
            patients = []
            for _, row in df.iterrows():
                patient = Patient(
                    patient_id=row['patient_id'],
                    type=row['type'],
                    age=row['age'],
                    height=row['height'],
                    weight=row['weight'],
                    gender=row['gender']
                )
                patients.append(patient)
            
            self.patients[edge_device_id] = patients
            print(f"Loaded {len(patients)} patients for edge device {edge_device_id}")
            return patients
        except Exception as e:
            print(f"Error loading patients from {csv_file_path}: {e}")
            return []
    
    def get_patient(self, patient_id: str, edge_device_id: int) -> Patient:
        """Get patient by ID from specific edge device"""
        if edge_device_id in self.patients:
            for patient in self.patients[edge_device_id]:
                if patient.patient_id == patient_id:
                    return patient
        return None