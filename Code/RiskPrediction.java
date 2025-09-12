import weka.classifiers.trees.RandomForest;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.CSVLoader;

import java.io.File;

public class RiskPrediction {
    public static void main(String[] args) throws Exception {
        System.setProperty("weka.core.noPackageManager", "true");

        // Load training dataset
        CSVLoader trainLoader = new CSVLoader();
        trainLoader.setSource(new File("patient_data.csv"));
        Instances trainData = trainLoader.getDataSet();

        // Remove patient_id column (first column)
        trainData.deleteAttributeAt(0);
        trainData.setClassIndex(trainData.numAttributes() - 1);

        // Train RandomForest regression model
        RandomForest rf = new RandomForest();
        rf.setOptions(Utils.splitOptions("-I 100"));
        rf.buildClassifier(trainData);
        System.out.println("Model trained on " + trainData.numInstances() + " instances.");

        // Load test dataset
        CSVLoader testLoader = new CSVLoader();
        testLoader.setSource(new File("test_data.csv"));
        Instances testData = testLoader.getDataSet();

        // Extract patient IDs before removing column
        String[] patientIds = new String[testData.numInstances()];
        for (int i = 0; i < testData.numInstances(); i++) {
            patientIds[i] = testData.instance(i).stringValue(0);
        }

        // Remove patient_id column from test data
        testData.deleteAttributeAt(0);

        // Add dummy class attribute for prediction
        testData.insertAttributeAt(trainData.classAttribute(), testData.numAttributes());
        testData.setClassIndex(testData.numAttributes() - 1);

        // Print header
        System.out.println("\n=== Predictions on test_data.csv ===");
        System.out.printf("%-10s | %-10s | %-15s | %-10s | %-5s | %-7s | %-7s | %-15s | %-30s%n",
                "PatientID", "HR", "BloodPressure", "Glucose", "Age", "Weight", "Height", "PredRisk", "Status");
        System.out.println("-------------------------------------------------------------------------------------------------------------------");

        // Predictions
        for (int i = 0; i < testData.numInstances(); i++) {
            Instance inst = testData.instance(i);
            inst.setClassMissing();
            double prediction = rf.classifyInstance(inst);

            // Extract patient details
            double heartRate = inst.value(0);       // assuming 1st column is heart_rate
            double bloodPressure = inst.value(1);   // 2nd column
            double glucose = inst.value(2);         // 3rd column
            double age = inst.value(3);             // 4th column
            double weight = inst.value(4);          // 5th column
            double height = inst.value(5);          // 6th column

            // Predicted risk level
            String riskLevel = String.format("%.2f", prediction);

            // Determine status
            String status = (prediction > 1.5) ? "⚠ Immediate Attention Needed" : "Normal/Moderate";

            // Print row
            System.out.printf("%-10s | %-10.2f | %-15.2f | %-10.2f | %-5.0f | %-7.2f | %-7.2f | %-15s | %-30s%n",
                    patientIds[i], heartRate, bloodPressure, glucose, age, weight, height, riskLevel, status);
        }
    }
}
