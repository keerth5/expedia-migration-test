package com.expedia.ecs.logging;

import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.AppenderBase;
import com.amazonaws.services.logs.AWSLogs;
import com.amazonaws.services.logs.AWSLogsClientBuilder;
import com.amazonaws.services.logs.model.PutLogEventsRequest;
import com.amazonaws.services.logs.model.InputLogEvent;

import java.util.ArrayList;
import java.util.List;

/**
 * CloudWatch Log Handler
 * CloudWatchLogHandler pattern for direct CloudWatch logging
 */
public class CloudWatchLogHandler extends AppenderBase<ILoggingEvent> {

    private String logGroupName;
    private String logStreamName;
    private AWSLogs logsClient;

    public CloudWatchLogHandler() {
        // boto3.client("logs") equivalent
        this.logsClient = AWSLogsClientBuilder.defaultClient();
    }

    public void setLogGroupName(String logGroupName) {
        this.logGroupName = logGroupName;
    }

    public void setLogStreamName(String logStreamName) {
        this.logStreamName = logStreamName;
    }

    @Override
    protected void append(ILoggingEvent event) {
        // put_log_events pattern
        List<InputLogEvent> logEvents = new ArrayList<>();
        InputLogEvent logEvent = new InputLogEvent()
            .withMessage(event.getFormattedMessage())
            .withTimestamp(event.getTimeStamp());
        logEvents.add(logEvent);

        PutLogEventsRequest request = new PutLogEventsRequest()
            .withLogGroupName(logGroupName)
            .withLogStreamName(logStreamName)
            .withLogEvents(logEvents);

        try {
            logsClient.putLogEvents(request);
        } catch (Exception e) {
            // Log error but don't fail
            System.err.println("Failed to send log to CloudWatch: " + e.getMessage());
        }
    }
}

