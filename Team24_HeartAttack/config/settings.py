# Configuration settings for the healthcare edge computing system

# Normal health ranges (taken from www.heart.org and www.medscape.com)
NORMAL_RANGES = {
    'heart_rate': (60, 100),      # bpm
    'blood_pressure': (90, 120),  # mmHg  
    'glucose_level': (70, 140)    # mg/dL
}

# Parameter weights for m-value (tie-breaking mechanism)
PARAMETER_WEIGHTS = {
    'heart_rate': 3.0,
    'blood_pressure': 2.0,
    'glucose_level': 1.0
}

# Edge device configurations
EDGE_DEVICE_SPECS = {
    'cpu_capacity': 8,           # CPU cores
    'memory_capacity': 16384,    # MB RAM
    'disk_capacity': 500000,     # MB storage
    'bandwidth_capacity': 1000   # Mbps
}

# Cloud device configurations  
CLOUD_DEVICE_SPECS = {
    'cpu_capacity': 32,
    'memory_capacity': 65536, 
    'disk_capacity': 2000000,
    'bandwidth_capacity': 10000
}

# Simulation settings
SIMULATION_SETTINGS = {
    'base_processing_time': 0.1,  # seconds
    'task_generation_interval': 1.0
}