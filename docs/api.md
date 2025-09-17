# X-Bot API Documentation

## Endpoints

### GET /
Health check endpoint.

**Response:**
```json
{
  "message": "X Bot is running"
}
```

### GET /status
Bot operational status and last activity timestamps.

**Response:**
```json
{
  "status": "running",
  "last_market_update": "2025-09-16T10:30:00Z",
  "last_engagement": "2025-09-16T10:25:00Z",
  "last_promotion": "2025-09-16T10:20:00Z"
}
```

### GET /metrics
Prometheus metrics for monitoring.

**Response:**
```
# HELP posts_counter_total Number of posts made
# TYPE posts_counter_total counter
posts_counter_total 42

# HELP likes_counter_total Number of likes given
# TYPE likes_counter_total counter
likes_counter_total 156

# HELP replies_counter_total Number of replies made
# TYPE replies_counter_total counter
replies_counter_total 23

# HELP engagements_counter_total Total engagement actions
# TYPE engagements_counter_total counter
engagements_counter_total 221
```

## Bot Functionality

### Market Updates
- Posts trending memecoin information every 30 minutes
- Fetches data from CoinGecko API
- Includes price and hashtag information

### Community Engagement
- Searches for $wifDOG related tweets every 15 minutes
- Likes and replies to relevant tweets
- Filters out spam content

### Community Promotion
- Posts promotional content every hour
- Drives traffic to community links

## Configuration

### Rate Limiting
- 10 requests per minute default
- Configurable via `RATE_LIMIT_PER_MINUTE` environment variable

### Spam Detection
- Threshold of 5 spam keywords default
- Configurable via `SPAM_THRESHOLD` environment variable

### Logging
- Structured logging with context
- Cloud Logging integration in production
- Configurable log levels