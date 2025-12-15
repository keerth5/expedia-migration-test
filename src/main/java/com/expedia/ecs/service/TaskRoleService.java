package com.expedia.ecs.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * ECS Task Role Assumptions Service
 * This needs to be updated to use IRSA
 */
@Service
public class TaskRoleService {

    // ECS_TASK_ROLE pattern
    @Value("${ecs.task.role.arn}")
    private String ecsTaskRoleArn;
    
    // task-role pattern
    private static final String TASK_ROLE_ENV = System.getenv("ECS_TASK_ROLE");

    /**
     * Get credentials using ECS task role
     * get_credentials.ecs pattern
     */
    public String getTaskRoleCredentials() {
        // ECS_TASK_ROLE usage
        String roleArn = TASK_ROLE_ENV != null ? TASK_ROLE_ENV : ecsTaskRoleArn;
        
        // task-role assumption logic
        // get_credentials.ecs equivalent
        return "Credentials from ECS task role: " + roleArn;
    }
}

