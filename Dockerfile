FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/ecs-sample-app-1.0.0.jar app.jar

# ECS Task Role environment variable
ENV ECS_TASK_ROLE=arn:aws:iam::123456789012:role/ecs-task-role

# Platform-Specific APM Configuration
ENV DD_AGENT_HOST=169.254.170.2
ENV DD_ECS_COLLECT=true

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]

