package com.expedia.ecs.service;

import com.amazonaws.services.ecs.AmazonECS;
import com.amazonaws.services.ecs.AmazonECSClientBuilder;
import com.amazonaws.services.ecs.model.DescribeTasksRequest;
import com.amazonaws.services.ecs.model.ListTasksRequest;
import com.amazonaws.services.ecs.model.RunTaskRequest;
import org.springframework.stereotype.Service;

/**
 * ECS-Specific API Calls Service
 * These patterns need to be replaced with Kubernetes API calls
 */
@Service
public class EcsApiService {

    private AmazonECS ecsClient;

    public EcsApiService() {
        // boto3.client("ecs") equivalent
        this.ecsClient = AmazonECSClientBuilder.defaultClient();
    }

    /**
     * ECS describe_tasks pattern
     */
    public void describeEcsTasks(String clusterName, String taskArn) {
        // ecs.describe_tasks pattern
        DescribeTasksRequest request = new DescribeTasksRequest()
            .withCluster(clusterName)
            .withTasks(taskArn);
        
        ecsClient.describeTasks(request);
    }

    /**
     * ECS list_tasks pattern
     */
    public void listEcsTasks(String clusterName) {
        // ecs.list_tasks pattern
        ListTasksRequest request = new ListTasksRequest()
            .withCluster(clusterName);
        
        ecsClient.listTasks(request);
    }

    /**
     * ECS run_task pattern
     */
    public void runEcsTask(String clusterName, String taskDefinition) {
        // ecs.run_task pattern
        RunTaskRequest request = new RunTaskRequest()
            .withCluster(clusterName)
            .withTaskDefinition(taskDefinition);
        
        ecsClient.runTask(request);
    }
}

