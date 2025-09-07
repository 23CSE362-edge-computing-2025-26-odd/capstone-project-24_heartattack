package Team_24_HeartAttack;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.*;

// Priority Manager reads sensor values and calculate the priority of each task
// It also decides if the task goes to the edge_queue or cloud_queue

public class Priority_Manager
{
    // Health value ranges for a normal human
    public static double HEART_RATE_MIN=60.0,HEART_RATE_MAX=100.0;
    public static double BLOOD_PRESSURE_MIN=90.0,BLOOD_PRESSURE_MAX=120.0;
    public static double GLUCOSE_MIN=70.0,GLUCOSE_MAX=140.0;
    
    // Creating priority queue for edge
    public static PriorityQueue<HealthTask> edge_queue=new PriorityQueue<>((t1,t2)->Double.compare(t2.priority,t1.priority));
    
    // Creating priority queue for cloud
    public static PriorityQueue<HealthTask> cloud_queue=new PriorityQueue<>((t1,t2)->Double.compare(t2.priority,t1.priority));
    
    public static void initialize()
    {
        System.out.println("Priority Manager initialized");
    }

    public static boolean file_processed=false;
    
    public static void process_file()
    {
        if (file_processed)
        {
            return;
        }
        System.out.println("Processing sensor data...");
        check_for_new_data();
        file_processed=true;
        System.out.println("Total tasks: "+(edge_queue.size()+cloud_queue.size()));
    }

    // Reading sensor data from file
    public static void check_for_new_data()
    {
        try (BufferedReader reader=new BufferedReader(new FileReader("sensor_data.csv")))
        {
            String line;
            boolean is_header=true;
            while ((line=reader.readLine())!=null)
            {
                if (is_header)
                {
                	is_header=false;
                	continue;
                }
                process_sensor_reading(line);
            }
        }
        catch (Exception e)
        {
            System.out.println("Error reading sensor_data.csv:"+e.getMessage());
        }
    }

    // Deciding task off-loading to queues
    public static void process_sensor_reading(String line)
    {
        try {
            String[] values=line.split(",");
            String patient_id=values[0].trim();
            double heart_rate=Double.parseDouble(values[1].trim());
            double blood_pressure=Double.parseDouble(values[2].trim());
            double glucose_level=Double.parseDouble(values[3].trim());
            HealthTask task=new HealthTask(patient_id,heart_rate,blood_pressure,glucose_level);
            double priority=calculate_priority(task);
            task.priority=priority;
            if (priority>=1.0)
            {
                edge_queue.add(task);
                System.out.println("→ EDGE: Patient "+patient_id+" (Priority:"+String.format("%.2f",priority)+")");
                if (priority>1.5)
                {
                    trigger_alarm(task);
                }
            }
            else
            {
                cloud_queue.add(task);
                System.out.println("→ CLOUD: Patient "+patient_id+" (Priority: "+String.format("%.2f",priority)+")");
            }
            
        }
        catch (Exception e)
        {
            System.out.println("Error processing sensor data: "+line);
        }
    }
    
    // Calculating priority of a task
    public static double calculate_priority(HealthTask task)
    {
        double hrPriority=calculate_parameter_priority(task.heart_rate,HEART_RATE_MIN,HEART_RATE_MAX);
        double bpPriority=calculate_parameter_priority(task.blood_pressure,BLOOD_PRESSURE_MIN,BLOOD_PRESSURE_MAX);
        double glucosePriority=calculate_parameter_priority(task.glucose_level,GLUCOSE_MIN,GLUCOSE_MAX);
        double priority=Math.max(hrPriority,Math.max(bpPriority,glucosePriority));
        return Math.max(0,Math.min(2,priority));
    }
    
    // Finding priority of each individual parameter
    public static double calculate_parameter_priority(double value,double min_normal,double max_normal)
    {
    	 double numerator=Math.abs(Math.pow(max_normal-value,2)-Math.pow(min_normal-value,2));
         double denominator=Math.pow(max_normal-min_normal,2);
         return numerator/denominator;
    }
    
    // Alarm for priority value > 1.5
    public static void trigger_alarm(HealthTask task)
    {
        System.out.println("!!! ALARM !!! Patient "+task.patient_id+" needs immediate attention! (Priority: "+String.format("%.2f",task.priority)+")");
    }
    
    public static List<HealthTask> get_edge_tasks() { return new ArrayList<>(edge_queue); }
    public static List<HealthTask> get_cloud_tasks() { return new ArrayList<>(cloud_queue); }
    
    // Task class
    public static class HealthTask
    {
        public String patient_id;
        public double heart_rate;
        public double blood_pressure;
        public double glucose_level;
        public double priority;
        
        public HealthTask(String patient_id,double heart_rate,double blood_pressure,double glucose_level)
        {
            this.patient_id=patient_id;
            this.heart_rate=heart_rate;
            this.blood_pressure=blood_pressure;
            this.glucose_level=glucose_level;
        }
    }
}