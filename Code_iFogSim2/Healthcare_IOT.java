package Team_24_HeartAttack;

// Simulation class
public class Healthcare_IOT
{
    
	// Initialization
    public static void main(String[] args)
    {
        try {
            System.out.println("=== Starting Healthcare IoT Simulation ===");
            Device_Manager.create_edge_device();
            Device_Manager.create_cloud_device();
            Sensor_Manager.create_sensor();
            Actuator_Manager.create_actuator();
            Priority_Manager.initialize();
            Priority_Manager.process_file();
            show_results();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
    
    // Output
    public static void show_results()
    {
        System.out.println("\n=== SIMULATION RESULTS ===");
        System.out.println("Edge Tasks: "+Priority_Manager.get_edge_tasks().size());
        System.out.println("Cloud Tasks: "+Priority_Manager.get_cloud_tasks().size());
        display_queues();
    }
    
    // displaying edge and cloud queues
    public static void display_queues()
    {
        System.out.println("EDGE QUEUE :");
        for (Priority_Manager.HealthTask task:Priority_Manager.get_edge_tasks())
        {
            System.out.printf(" Patient: %s | Priority: %.2f | HR: %.1f | BP: %.1f | Glucose: %.1f%n",task.patient_id,task.priority,task.heart_rate,task.blood_pressure,task.glucose_level);
        }
        System.out.println("\nCLOUD QUEUE :");
        for (Priority_Manager.HealthTask task:Priority_Manager.get_cloud_tasks())
        {
            System.out.printf("  Patient: %s | Priority: %.2f | HR: %.1f | BP: %.1f | Glucose: %.1f%n",task.patient_id,task.priority,task.heart_rate,task.blood_pressure,task.glucose_level);
        }
    }
}
