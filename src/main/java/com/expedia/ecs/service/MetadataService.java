package com.expedia.ecs.service;

import org.springframework.stereotype.Service;

import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * Metadata Service for accessing ECS Task and EC2 Instance metadata
 * These patterns need to be replaced with Kubernetes Downward API
 */
@Service
public class MetadataService {

    // ECS Task Metadata Access patterns
    private static final String ECS_CONTAINER_METADATA_URI = System.getenv("ECS_CONTAINER_METADATA_URI");
    private static final String ECS_TASK_METADATA_URI = "http://169.254.170.2/v4/metadata";
    private static final String ECS_TASK_METADATA_URI_V3 = "http://169.254.170.2/v3/metadata";
    private static final String ECS_TASK_METADATA_URI_V2 = "http://169.254.170.2/v2/metadata";

    // EC2 Instance Metadata Access patterns
    private static final String EC2_METADATA_URI = "http://169.254.169.254/latest/meta-data/";
    private static final String EC2_INSTANCE_IDENTITY_URI = "http://169.254.169.254/latest/dynamic/instance-identity/document";

    /**
     * Get ECS Task Metadata
     */
    public String getEcsTaskMetadata() {
        try {
            // ECS_CONTAINER_METADATA_URI usage
            String metadataUri = ECS_CONTAINER_METADATA_URI != null ? 
                ECS_CONTAINER_METADATA_URI : ECS_TASK_METADATA_URI;
            
            // /v4/metadata, /v3/metadata, /v2/metadata patterns
            URL url = new URL(metadataUri);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(conn.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            return response.toString();
        } catch (Exception e) {
            throw new RuntimeException("Failed to get ECS task metadata", e);
        }
    }

    /**
     * Get EC2 Instance Metadata
     */
    public String getEc2InstanceMetadata() {
        try {
            // 169.254.169.254 pattern
            // instance-identity pattern
            URL url = new URL(EC2_INSTANCE_IDENTITY_URI);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(conn.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            return response.toString();
        } catch (Exception e) {
            throw new RuntimeException("Failed to get EC2 instance metadata", e);
        }
    }

    /**
     * Get EC2 metadata using ec2.metadata pattern
     */
    public String getEc2Metadata(String path) {
        try {
            // ec2.metadata usage
            URL url = new URL(EC2_METADATA_URI + path);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(conn.getInputStream()));
            return reader.readLine();
        } catch (Exception e) {
            throw new RuntimeException("Failed to get EC2 metadata", e);
        }
    }
}

