package com.expedia.ecs.service;

import com.amazonaws.services.logs.AWSLogs;
import com.amazonaws.services.logs.AWSLogsClientBuilder;
import com.amazonaws.services.logs.model.PutLogEventsRequest;
import com.amazonaws.services.logs.model.InputLogEvent;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * CloudWatch Direct Logging Service
 * This should be replaced with stdout/stderr logging for RCP
 */
@Service
public class CloudWatchLoggingService {

    // CloudWatchLogHandler pattern
    private AWSLogs cloudWatchLogsClient;

    public CloudWatchLoggingService() {
        // boto3.client("logs") equivalent in Java
        this.cloudWatchLogsClient = AWSLogsClientBuilder.defaultClient();
    }

    /**
     * Direct CloudWatch logging using put_log_events pattern
     */
    public void logToCloudWatch(String logGroupName, String logStreamName, String message) {
        // put_log_events pattern
        List<InputLogEvent> logEvents = new ArrayList<>();
        InputLogEvent logEvent = new InputLogEvent()
            .withMessage(message)
            .withTimestamp(new Date().getTime());
        logEvents.add(logEvent);

        PutLogEventsRequest request = new PutLogEventsRequest()
            .withLogGroupName(logGroupName)
            .withLogStreamName(logStreamName)
            .withLogEvents(logEvents);

        cloudWatchLogsClient.putLogEvents(request);
    }
}

