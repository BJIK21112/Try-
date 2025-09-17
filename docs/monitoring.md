# X-Bot Monitoring Setup

## Google Cloud Monitoring

### Dashboards
Create a custom dashboard in Cloud Monitoring:

1. **Go to Cloud Monitoring > Dashboards > Create Dashboard**
2. **Add widgets for:**
   - CPU Utilization (Cloud Run)
   - Memory Utilization (Cloud Run)
   - Request Count (Cloud Run)
   - Error Rate (Logs-based metric)

### Key Metrics to Monitor

#### Application Metrics (Prometheus)
- `posts_counter_total`: Number of posts made
- `likes_counter_total`: Number of likes given
- `replies_counter_total`: Number of replies made
- `engagements_counter_total`: Total engagement actions

#### Cloud Run Metrics
- Request latency
- Error rate
- CPU/Memory usage
- Instance count

#### Log-based Metrics
- Rate limit exceeded events
- API failures
- Spam detection events

## Alerts Setup

### Critical Alerts
1. **Service Down**
   - Condition: Uptime < 99.9%
   - Threshold: 5 minutes
   - Notification: Email + SMS

2. **High Error Rate**
   - Condition: Error rate > 5%
   - Threshold: 5 minutes
   - Notification: Email

3. **Rate Limit Exceeded**
   - Log-based metric for rate limit warnings
   - Threshold: 10 occurrences per hour
   - Notification: Email

### Warning Alerts
1. **High Memory Usage**
   - Condition: Memory > 80%
   - Threshold: 10 minutes
   - Notification: Email

2. **Low Engagement Rate**
   - Custom metric for engagement success rate
   - Condition: Success rate < 50%
   - Notification: Email

## Log Analysis

### Structured Logging
The bot uses structured logging with these fields:
- `action`: The operation being performed
- `success`: Boolean success indicator
- `tweet_id`: Twitter tweet ID when applicable
- `coin`: Cryptocurrency symbol
- `price`: Price information
- `engagement_type`: Type of engagement action

### Useful Log Queries

```sql
-- Recent errors
resource.type="cloud_run_revision"
resource.labels.service_name="x-bot"
severity>=ERROR

-- Rate limit events
resource.type="cloud_run_revision"
resource.labels.service_name="x-bot"
textPayload:"rate limit"

-- Successful engagements
resource.type="cloud_run_revision"
resource.labels.service_name="x-bot"
textPayload:"Successfully engaged"
```

## Health Checks

### Application Health
- Endpoint: `GET /`
- Expected: HTTP 200 with JSON response

### Status Check
- Endpoint: `GET /status`
- Expected: Current timestamps for bot activities

### Metrics Check
- Endpoint: `GET /metrics`
- Expected: Prometheus format metrics

## Troubleshooting

### Common Issues

1. **High Latency**
   - Check Cloud Run instance count
   - Monitor API response times
   - Consider increasing CPU allocation

2. **Memory Issues**
   - Monitor memory usage patterns
   - Check for memory leaks in dependencies
   - Increase memory allocation if needed

3. **API Rate Limits**
   - Monitor Twitter API usage
   - Implement exponential backoff
   - Consider upgrading API tiers

4. **Container Restarts**
   - Check application logs for crashes
   - Verify all secrets are accessible
   - Check resource limits vs usage