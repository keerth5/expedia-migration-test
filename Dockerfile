FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/ecs-sample-app-1.0.0.jar app.jar

# ECS Task Metadata environment variable
ENV ECS_CONTAINER_METADATA_URI=http://169.254.170.2/v4/metadata
ENV ECS_TASK_METADATA_URI=http://169.254.170.2/v4/metadata

# EC2 Instance Metadata environment variable
ENV EC2_METADATA_URI=http://169.254.169.254/latest/meta-data/

# ECS Task Role environment variable
ENV ECS_TASK_ROLE=arn:aws:iam::123456789012:role/ecs-task-role

# Platform-Specific APM Configuration
ENV DD_AGENT_HOST=169.254.170.2
ENV DD_ECS_COLLECT=true

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]

