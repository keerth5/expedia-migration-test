package com.expedia.ecs;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

/**
 * Sample ECS application demonstrating platform-specific patterns
 * that need to be migrated for RCP compatibility
 */
@SpringBootApplication
@EnableEurekaClient
public class EcsSampleApplication {

    public static void main(String[] args) {
        SpringApplication.run(EcsSampleApplication.class, args);
    }
}

