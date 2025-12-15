package com.expedia.ecs.service;

import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.simplesystemsmanagement.AWSSimpleSystemsManagement;
import com.amazonaws.services.simplesystemsmanagement.AWSSimpleSystemsManagementClientBuilder;
import com.amazonaws.services.simplesystemsmanagement.model.GetParameterRequest;
import com.amazonaws.services.simplesystemsmanagement.model.GetParameterResult;
import com.amazonaws.services.simplesystemsmanagement.model.GetParametersByPathRequest;
import com.amazonaws.services.simplesystemsmanagement.model.GetParametersByPathResult;
import com.amazonaws.services.secretsmanager.AWSSecretsManager;
import com.amazonaws.services.secretsmanager.AWSSecretsManagerClientBuilder;
import com.amazonaws.services.secretsmanager.model.GetSecretValueRequest;
import com.amazonaws.services.secretsmanager.model.GetSecretValueResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * AWS Configuration Service using Parameter Store and Secrets Manager
 * These patterns need to be migrated to EG Vault
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
     * AWS Parameter Store Usage - GetParameter pattern
     */
    public String getParameterFromStore(String parameterName) {
        AWSCredentials credentials = new BasicAWSCredentials(awsAccessKeyId, awsSecretAccessKey);
        AWSSimpleSystemsManagement ssmClient = AWSSimpleSystemsManagementClientBuilder.standard()
            .withCredentials(new AWSStaticCredentialsProvider(credentials))
            .build();

        // GetParameter call
        GetParameterRequest request = new GetParameterRequest()
            .withName(parameterName)
            .withWithDecryption(true);
        
        GetParameterResult result = ssmClient.getParameter(request);
        return result.getParameter().getValue();
    }

    /**
     * AWS Parameter Store Usage - get_parameters_by_path pattern
     */
    public GetParametersByPathResult getParametersByPath(String path) {
        AWSCredentials credentials = new BasicAWSCredentials(awsAccessKeyId, awsSecretAccessKey);
        AWSSimpleSystemsManagement ssmClient = AWSSimpleSystemsManagementClientBuilder.standard()
            .withCredentials(new AWSStaticCredentialsProvider(credentials))
            .build();

        // get_parameters_by_path call
        GetParametersByPathRequest request = new GetParametersByPathRequest()
            .withPath(path)
            .withRecursive(true)
            .withWithDecryption(true);
        
        return ssmClient.getParametersByPath(request);
    }

    /**
     * AWS Secrets Manager Usage - GetSecretValue pattern
     */
    public String getSecretFromManager(String secretName) {
        AWSCredentials credentials = new BasicAWSCredentials(awsAccessKeyId, awsSecretAccessKey);
        AWSSecretsManager secretsClient = AWSSecretsManagerClientBuilder.standard()
            .withCredentials(new AWSStaticCredentialsProvider(credentials))
            .build();

        // GetSecretValue call
        GetSecretValueRequest request = new GetSecretValueRequest()
            .withSecretId(secretName);
        
        GetSecretValueResult result = secretsClient.getSecretValue(request);
        return result.getSecretString();
    }
}

