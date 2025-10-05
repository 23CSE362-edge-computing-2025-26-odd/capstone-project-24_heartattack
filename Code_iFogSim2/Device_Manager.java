package Team_24_HeartAttack;

import org.fog.entities.FogDevice;
import org.fog.entities.Pe;
import org.fog.entities.RamProvisionerSimple;
import org.fog.entities.BwProvisionerOverbooking;
import org.fog.entities.Storage;
import org.fog.entities.PowerHost;
import org.fog.entities.FogDeviceCharacteristics;
import org.fog.policy.AppModuleAllocationPolicy;
import org.fog.scheduler.StreamOperatorScheduler;
import org.fog.utils.FogLinearPowerModel;
import org.fog.utils.FogUtils;

import java.util.ArrayList;
import java.util.List;

public class Device_Manager {

    // Creating the edge device (Hospital Workstation)
    public static FogDevice create_edge_device() {
        System.out.println("Creating Edge Device : Hospital Worknode");
        return create_device(
            "edge_node",      // Device name
            10000,           // MIPS (processing power)
            10000,           // RAM (MB)
            10000,           // Upload bandwidth (Mbps)
            10000,           // Download bandwidth (Mbps)
            1,               // Level (1 = edge level)
            0.01,            // Cost per MIPS
            0.001,           // Busy power consumption
            0.0,             // Idle power consumption
            1000000          // Storage capacity (MB)
        );
    }
    
    // Creating the cloud device (Central Hospital Server)
    public static FogDevice create_cloud_device() {
        System.out.println("Creating Cloud Device : Hospital Server");
        return create_device(
            "cloud_server",   // Device name
            100000,          // MIPS (more powerful)
            100000,          // RAM (more memory)
            100000,          // Upload bandwidth (faster)
            100000,          // Download bandwidth (faster)
            0,               // Level (0 = cloud level)
            0.05,            // Cost per MIPS (higher cost)
            0.02,            // Busy power consumption
            0.0,             // Idle power consumption
            10000000         // Storage capacity (larger)
        );
    }
    
    // Actual device creation with iFogSim2 components
    public static FogDevice create_device(String name, long mips, int ram, long upBw, 
                                        long downBw, int level, double ratePerMips, 
                                        double busyPower, double idlePower, long storageCapacity) {
        try {
            // 1. Create Processing Elements (CPU cores)
            List<Pe> peList = new ArrayList<>();
            peList.add(new Pe(0, new PeProvisionerOverbooking(mips)));
            
            // 2. Create Host configuration
            int hostId = FogUtils.generateEntityId();
            PowerHost host = new PowerHost(
                hostId,
                new RamProvisionerSimple(ram),           // RAM provisioner
                new BwProvisionerOverbooking(upBw),      // Bandwidth provisioner  
                storageCapacity,                         // Storage capacity
                peList,                                  // Processing elements
                new StreamOperatorScheduler(peList),     // Task scheduler
                new FogLinearPowerModel(busyPower, idlePower) // Power model
            );
            
            List<Host> hostList = new ArrayList<>();
            hostList.add(host);
            
            // 3. Set device characteristics
            String arch = "x86";
            String os = "Linux"; 
            String vmm = "Xen";
            double timeZone = 10.0;
            double cost = 3.0;
            double costPerMem = 0.05;
            double costPerStorage = 0.001;
            double costPerBw = 0.1;
            
            FogDeviceCharacteristics characteristics = new FogDeviceCharacteristics(
                arch, os, vmm, host, timeZone, cost, costPerMem, costPerStorage, costPerBw);
            
            // 4. CREATE ACTUAL FOGDEVICE OBJECT
            FogDevice device = new FogDevice(
                name,                          // Device name
                characteristics,               // Hardware specs
                new AppModuleAllocationPolicy(hostList), // Allocation policy
                new ArrayList<>(),             // Connected sensors (empty initially)
                10,                            // Uplink latency
                upBw,                          // Upload bandwidth  
                downBw,                        // Download bandwidth
                0,                             // Downlink latency
                ratePerMips                    // Cost rate per MIPS
            );
            
            device.setLevel(level); // Set device level (0=cloud, 1=edge, 2=fog, etc.)
            
            System.out.println("Device created: " + name + " (MIPS: " + mips + ", Level: " + level + ")");
            return device; // RETURN ACTUAL FOGDEVICE OBJECT
            
        } catch (Exception e) {
            System.err.println("Error creating device " + name + ": " + e.getMessage());
            return null;
        }
    }
}
