package Team_24_HeartAttack;
import org.fog.entities.FogDevice;

// Device_Manager creates and manages the edge and cloud devices
// Sample implementation to create devices

public class Device_Manager
{

	// Creating the edge device
    public static FogDevice create_edge_device()
    {
        System.out.println("Creating Edge Device : Hospital Worknode");
        return create_device("edge_node",10000,10000,10000,10000,1);
    }
    
    // Creating the cloud device
    public static FogDevice create_cloud_device()
    {
        System.out.println("Creating Cloud Device : Hospital Server");
        return create_device("cloud_server",100000,100000,100000,100000,0);
    }
    
    // Creating a device
    public static FogDevice create_device(String name,long processing_power,int memory,long upload_speed,long download_speed,int location)
    {
        System.out.println("Device created:"+name+"(Power:"+processing_power+" MIPS)");
        return null;
    }
}