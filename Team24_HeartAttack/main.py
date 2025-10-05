import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.simulation_manager import HealthcareEdgeSystem

def main():
    """Main function to run the healthcare edge computing simulation"""
    print("TEAM24 HEARTATTACK - Healthcare Edge Computing System")
    print("=" * 50)
    
    # Initialize the healthcare edge system
    healthcare_system = HealthcareEdgeSystem()
    
    # Run the simulation
    healthcare_system.run_simulation()
    
    # Analyze and display results
    healthcare_system.analyze_performance()
    
    # Demonstrate priority calculation with examples
    print("\n" + "="*60)
    print("PRIORITY CALCULATION EXAMPLES")
    print("="*60)
    
    from src.models import HealthTask, Patient
    
    # Create a new priority calculator for examples (avoid re-training)
    example_calc = healthcare_system.priority_calculator
    
    # Example 1: Normal readings (general patient)
    print("\nExample 1: Normal health readings")
    normal_task = HealthTask('P999', 72, 100, 95, 'general')
    normal_patient = Patient('P999', 'general', 45, 175, 70, 'M')
    normal_task = example_calc.calculate_task_priority(normal_task, normal_patient)
    print(f"Normal readings (HR=72, BP=120, Glucose=95): k={normal_task.k_value:.2f}, m={normal_task.m_value:.1f}")
    
    # Example 2: Critical heart rate
    print("\nExample 2: Critical heart rate")
    critical_task = HealthTask('P999', 180, 120, 95, 'general')
    critical_task = example_calc.calculate_task_priority(critical_task, normal_patient)
    print(f"Critical HR (HR=180, BP=120, Glucose=95): k={critical_task.k_value:.2f}, m={critical_task.m_value:.1f}")
    
    # Example 3: High blood pressure
    print("\nExample 3: High blood pressure")
    high_bp_task = HealthTask('P999', 72, 180, 95, 'general')
    high_bp_task = example_calc.calculate_task_priority(high_bp_task, normal_patient)
    print(f"High BP (HR=72, BP=180, Glucose=95): k={high_bp_task.k_value:.2f}, m={high_bp_task.m_value:.1f}")
    
    # Example 4: High glucose level
    print("\nExample 4: High glucose level")
    high_glucose_task = HealthTask('P999', 72, 120, 250, 'general')
    high_glucose_task = example_calc.calculate_task_priority(high_glucose_task, normal_patient)
    print(f"High Glucose (HR=72, BP=120, Glucose=250): k={high_glucose_task.k_value:.2f}, m={high_glucose_task.m_value:.1f}")
    
    print("\n" + "="*50)
    print("SIMULATION COMPLETED SUCCESSFULLY!")
    print("="*50)

if __name__ == "__main__":
    main()