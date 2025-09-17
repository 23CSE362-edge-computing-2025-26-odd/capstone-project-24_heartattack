package Team_24_HeartAttack;

import org.fog.entities.Sensor;
import org.fog.utils.distribution.DeterministicDistribution;

public class Sensor_Manager {
    
    // Creating actual healthcare sensor
    public static Sensor create_sensor() {
        System.out.println("Creating Healthcare Sensor");
        try {
            // Create sensor that generates data every 5 seconds
            Sensor sensor = new Sensor(
                "health_sensor",           // Sensor name
                "SENSOR",                  // Sensor type
                new DeterministicDistribution(5), // Data generation interval (5 seconds)
                "HEALTHCARE",              // User ID (application context)
                "HEALTH_DATA",             // Tuple type (what data it sends)
                1                          // Sensor ID
            );
            System.out.println("Sensor created: Healthcare Monitoring Device");
            return sensor;
        } catch (Exception e) {
            System.err.println("Error creating sensor: " + e.getMessage());
            return null;
        }
    }
}
