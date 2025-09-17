package Team_24_HeartAttack;

import org.fog.entities.Actuator;

public class Actuator_Manager {
    
    // Creating actual emergency alarm actuator
    public static Actuator create_actuator() {
        System.out.println("Creating Actuator : Emergency Alarm");
        try {
            Actuator actuator = new Actuator(
                "emergency_alarm",    // Actuator name
                "ACTUATOR",           // Actuator type
                "HEALTHCARE",         // User ID (application context)
                "ALARM_SIGNAL"        // Tuple type (what signal it receives)
            );
            System.out.println("Actuator created: Emergency Alert System");
            return actuator;
        } catch (Exception e) {
            System.err.println("Error creating actuator: " + e.getMessage());
            return null;
        }
    }
}
