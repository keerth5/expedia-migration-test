package com.expedia.ecs.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * API Controller
 * Note: This intentionally does NOT have health check endpoints
 * to trigger the "Missing Health Check Endpoints" rule
 */
@RestController
@RequestMapping("/api")
public class ApiController {

    @GetMapping("/status")
    public String getStatus() {
        return "Application is running";
    }

    @GetMapping("/info")
    public String getInfo() {
        return "ECS Sample Application v1.0.0";
    }
}

