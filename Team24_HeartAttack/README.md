# Team24 HeartAttack - Healthcare Edge Computing System

A priority-based task scheduling and resource allocation system for healthcare IoT using edge computing, implementing the PTS mechanism from research papers.

## Project Overview

This system monitors patient health data in real-time using IoT sensors and intelligently schedules tasks between edge devices and cloud based on medical urgency levels. It implements the Priority-based Task Scheduling (PTS) mechanism for smart hospital environments.

## Key Features

- **Real-time Health Monitoring**: Continuous monitoring of heart rate, blood pressure, and glucose levels
- **Intelligent Priority System**: Calculates urgency levels (k-values) using medical emergency criteria
- **Edge-Cloud Decision Making**: Automatically routes tasks to edge devices or cloud based on urgency
- **Machine Learning Integration**: Uses RandomForest models for specific patient priority calculation
- **Real Medical Data**: Trained on UCI Heart Disease dataset with 200+ real patient records

## Installation & Setup

1. Clone the repository
   git clone <repository-url>
   cd Team24_Heartattack

2. Create virtual environment
    heartattack_env\Scripts\activate

3. Install dependencies
    pip install -r requirements.txt

4. Run the simulation
    python main.py