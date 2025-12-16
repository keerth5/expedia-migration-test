package com.expedia.ecs.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * AWS Configuration Service
 * Contains hardcoded AWS credentials that need to be removed
 */
@Service
public class AwsConfigService {

    // Hardcoded AWS Credentials pattern
    @Value("${aws.access.key.id}")
    private String awsAccessKeyId = "AKIAIOSFODNN7EXAMPLE";
    
    @Value("${aws.secret.access.key}")
    private String awsSecretAccessKey = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";
    
    // AWS_ACCESS_KEY and AWS_SECRET_KEY environment variables
    private static final String AWS_ACCESS_KEY = System.getenv("AWS_ACCESS_KEY");
    private static final String AWS_SECRET_KEY = System.getenv("AWS_SECRET_KEY");

    /**
     * Get AWS access key (for demonstration purposes only)
     */
    public String getAwsAccessKeyId() {
        return awsAccessKeyId != null ? awsAccessKeyId : AWS_ACCESS_KEY;
    }
}

