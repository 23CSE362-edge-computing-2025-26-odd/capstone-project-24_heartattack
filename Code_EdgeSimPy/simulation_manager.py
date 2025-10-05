import edge_sim_py as es
import pandas as pd
import random
import sys
import os

# Add the parent directory to Python path to import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import our custom modules
try:
    from src.models import HealthTask, PatientDatabase
    from src.priority_calculator import PriorityCalculator
    print("Custom modules imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class HealthcareEdgeSystem:
    def __init__(self):
        self.simulator = None
        self.priority_calculator = PriorityCalculator()
        self.patient_db = PatientDatabase()
        self.edge_devices = []
        self.cloud_device = None
        self.tasks_processed = []
        self.metrics = {
            'latency': [],
            'edge_utilization': [],
            'cloud_utilization': [],
            'tasks_scheduled': []
        }
        
        # Load patient data for both edge devices
        self.setup_patient_data()
        
    def setup_patient_data(self):
        """Load patient data for both edge devices from CSV files"""
        print("Loading patient data...")
        
        # Load patients for edge device 1
        patients_edge1 = self.patient_db.load_patients_from_csv(
            "data/edge_device_1_patients.csv", 
            edge_device_id=1
        )
        
        # Load patients for edge device 2  
        patients_edge2 = self.patient_db.load_patients_from_csv(
            "data/edge_device_2_patients.csv",
            edge_device_id=2
        )
        
        print(f"Total patients loaded: Edge1={len(patients_edge1)}, Edge2={len(patients_edge2)}")
    
    def setup_infrastructure(self):
        """Setup edge devices, cloud, and network using EdgeSimPy"""
        print("Setting up edge computing infrastructure...")
    
        self.simulator = es.Simulator()
    
        # Create two edge devices (Hospital Workstations)
        edge_device_1 = es.EdgeServer(
            model_name="edge_device_1",
            cpu=8,           # 8 CPU cores
            memory=16384,    # 16 GB RAM
            disk=500000      # 500 GB storage
        )
    
        edge_device_2 = es.EdgeServer(
            model_name="edge_device_2", 
            cpu=8,
            memory=16384,
         disk=500000
        )
    
        self.edge_devices = [edge_device_1, edge_device_2]
    
        # Create cloud device
        self.cloud_device = es.EdgeServer(
            model_name="cloud_dc",
            cpu=32,
            memory=65536,
            disk=2000000
        )
    
        print("Infrastructure setup completed!")
        print(f"- Edge devices: {len(self.edge_devices)}")
        print(f"- Cloud device: {self.cloud_device.model_name}")
    
    def load_sensor_readings(self, edge_device_id: int) -> pd.DataFrame:
        """Load sensor readings for a specific edge device from CSV"""
        csv_file = f"data/sensor_readings_edge{edge_device_id}.csv"
        try:
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} sensor readings for edge device {edge_device_id}")
            return df
        except Exception as e:
            print(f"Error loading sensor readings from {csv_file}: {e}")
            return pd.DataFrame()
    
    def create_health_task(self, sensor_row: pd.Series, edge_device_id: int) -> HealthTask:
        """Create a HealthTask from sensor reading"""
        patient = self.patient_db.get_patient(sensor_row['patient_id'], edge_device_id)
        
        if patient is None:
            print(f"Warning: Patient {sensor_row['patient_id']} not found in database")
            return None
        
        task = HealthTask(
            patient_id=sensor_row['patient_id'],
            heart_rate=int(sensor_row['heart_rate']),
            blood_pressure=int(sensor_row['blood_pressure']),
            glucose_level=float(sensor_row['glucose_level']),
            task_type=patient.type,
            timestamp=float(sensor_row['timestamp']),
            edge_device_id=edge_device_id
        )
        
        return task
    
    def schedule_task(self, task: HealthTask) -> dict:
        """Schedule task to edge or cloud based on priority (k-value)"""
        edge_device = self.edge_devices[task.edge_device_id - 1]
        
        # Decision logic based on k-value (from research paper)
        if task.k_value > 1.0:  # Urgent task - schedule on edge
            target_device = edge_device
            location = "edge"
            processing_time = self.calculate_processing_time(task, target_device, is_edge=True)
        else:  # Non-urgent task - schedule on cloud
            target_device = self.cloud_device
            location = "cloud" 
            processing_time = self.calculate_processing_time(task, target_device, is_edge=False)
        
        # Record metrics
        task_metrics = {
            'patient_id': task.patient_id,
            'task_type': task.task_type,
            'k_value': task.k_value,
            'm_value': task.m_value,
            'scheduled_location': location,
            'processing_time': processing_time,
            'edge_device': task.edge_device_id,
            'heart_rate': task.heart_rate,
            'blood_pressure': task.blood_pressure,
            'glucose_level': task.glucose_level
        }
        
        self.tasks_processed.append(task_metrics)
        
        return task_metrics
    
    def calculate_processing_time(self, task: HealthTask, device, is_edge: bool) -> float:
        """Calculate processing time based on task complexity and device capability"""
        base_processing_time = 0.1  # 100ms base time
        
        # More complex tasks take longer (based on urgency)
        complexity_factor = 1.0
        if task.k_value > 1.5:
            complexity_factor = 2.0  # High urgency tasks might be more complex
        elif task.task_type == 'specific':
            complexity_factor = 1.5  # Specific patient tasks need more processing
        
        # Device capability factor
        if is_edge:
            device_factor = 1.0  # Edge devices are slower
        else:
            device_factor = 0.5  # Cloud is faster
        
        processing_time = base_processing_time * complexity_factor * device_factor
        
        # Add some randomness to simulate real-world variation
        processing_time *= random.uniform(0.8, 1.2)
        
        return processing_time
    
    def run_simulation(self):
        """Run the complete healthcare edge computing simulation"""
        print("\n" + "="*50)
        print("STARTING HEALTHCARE EDGE COMPUTING SIMULATION")
        print("="*50)
        
        self.setup_infrastructure()
        
        # Process sensor readings for both edge devices
        for edge_id in [1, 2]:
            print(f"\nProcessing sensor readings for Edge Device {edge_id}...")
            
            sensor_readings = self.load_sensor_readings(edge_id)
            
            for _, sensor_row in sensor_readings.iterrows():
                # Create health task from sensor reading
                task = self.create_health_task(sensor_row, edge_id)
                
                if task is None:
                    continue
                
                # Get patient for priority calculation
                patient = self.patient_db.get_patient(task.patient_id, edge_id)
                
                # Calculate priority values
                task = self.priority_calculator.calculate_task_priority(task, patient)
                
                # Schedule task based on priority
                task_metrics = self.schedule_task(task)
                
                print(f"Time {task.timestamp:6.1f}: {task.task_type:8} task for {task.patient_id} "
                      f"(HR={task.heart_rate}, BP={task.blood_pressure}, Glucose={task.glucose_level}) "
                      f"-> k={task.k_value:.2f}, m={task.m_value:.1f} -> "
                      f"{'EDGE' if task.k_value > 1.0 else 'CLOUD'} "
                      f"in {task_metrics['processing_time']:.3f}s")
        
        print(f"\nSimulation completed! Processed {len(self.tasks_processed)} tasks.")
    
    def analyze_performance(self):
        """Analyze and display simulation results"""
        if not self.tasks_processed:
            print("No tasks processed for analysis.")
            return None
        
        import pandas as pd
        
        # Convert to DataFrame for easier analysis
        tasks_df = pd.DataFrame(self.tasks_processed)
        
        print("\n" + "="*60)
        print("PERFORMANCE ANALYSIS RESULTS")
        print("="*60)
        
        # Basic statistics
        print(f"\nTotal Tasks Processed: {len(tasks_df)}")
        print(f"Edge Tasks: {len(tasks_df[tasks_df['scheduled_location'] == 'edge'])}")
        print(f"Cloud Tasks: {len(tasks_df[tasks_df['scheduled_location'] == 'cloud'])}")
        
        # Average processing time by location
        avg_processing = tasks_df.groupby('scheduled_location')['processing_time'].mean()
        print(f"\nAverage Processing Time:")
        for location, time in avg_processing.items():
            print(f"  {location.upper()}: {time:.3f}s")
        
        # Priority distribution
        print(f"\nPriority Distribution (k-value):")
        urgent_tasks = len(tasks_df[tasks_df['k_value'] > 1.0])
        non_urgent_tasks = len(tasks_df[tasks_df['k_value'] <= 1.0])
        print(f"  Urgent (k > 1.0): {urgent_tasks}")
        print(f"  Non-urgent (k ≤ 1.0): {non_urgent_tasks}")
        
        # Task type distribution
        task_type_counts = tasks_df['task_type'].value_counts()
        print(f"\nTask Type Distribution:")
        for task_type, count in task_type_counts.items():
            print(f"  {task_type}: {count}")
        
        # Edge device distribution
        edge_counts = tasks_df['edge_device'].value_counts().sort_index()
        print(f"\nTasks per Edge Device:")
        for edge_id, count in edge_counts.items():
            print(f"  Edge Device {edge_id}: {count} tasks")
        
        # Display tasks for verification
        print(f"\nAll Tasks Processed:")
        print(tasks_df.to_string(index=False))
        
        return tasks_df