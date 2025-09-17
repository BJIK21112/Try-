# X-Bot Production Deployment Guide

## Overview
This guide covers deploying the X-Bot to Google Cloud Run for production use.

## Prerequisites

### Google Cloud Setup
1. **GCP Project**: Create or use existing GCP project
2. **Service Account**: Create service account with these roles:
   - Cloud Run Admin
   - Secret Manager Secret Accessor
   - Storage Admin (for Container Registry)
   - Cloud Logging Writer
   - Cloud Monitoring Editor

3. **Enable APIs**:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable logging.googleapis.com
   gcloud services enable monitoring.googleapis.com
   ```

### Secrets Setup
Create the following secrets in Google Cloud Secret Manager:

1. **twitter-client-id**: Your Twitter API client ID
2. **twitter-client-secret**: Your Twitter API client secret
3. **twitter-bearer-token**: Your Twitter API bearer token
4. **twitter-access-token**: Your Twitter API access token
5. **twitter-access-token-secret**: Your Twitter API access token secret
6. **coingecko-api-key**: Your CoinGecko API key (optional)

### GitHub Repository Setup
1. Create GitHub repository
2. Add these repository secrets in Settings > Secrets and variables > Actions:
   - `GCP_SA_KEY`: JSON content of your service account key
   - `GCP_PROJECT_ID`: Your GCP project ID
   - `GOOGLE_CREDENTIALS`: Same as GCP_SA_KEY

## Deployment Steps

### 1. Initial Deployment
```bash
# Clone and setup
git clone <your-repo-url>
cd x-bot
pip install -r requirements.txt

# Build and test locally
make test
make build

# Push to GitHub (triggers CI/CD)
git add .
git commit -m "Initial production deployment"
git push origin main
```

### 2. Monitor Deployment
- Check GitHub Actions tab for CI/CD pipeline status
- Monitor Cloud Run service in GCP Console
- Check logs in Cloud Logging

### 3. Verify Bot Operation
```bash
# Check service health
curl https://x-bot-<hash>-uc.a.run.app/

# Check metrics
curl https://x-bot-<hash>-uc.a.run.app/metrics

# Check status
curl https://x-bot-<hash>-uc.a.run.app/status
```

## Configuration

### Environment Variables
The bot supports these environment variables:

- `LOG_LEVEL`: Logging level (default: INFO)
- `RATE_LIMIT_PER_MINUTE`: API rate limit (default: 10)
- `SPAM_THRESHOLD`: Spam detection threshold (default: 5)
- `GOOGLE_CLOUD_PROJECT`: GCP project ID (auto-set by Cloud Run)

### Scaling Configuration
Current Cloud Run settings:
- Memory: 1Gi
- CPU: 1
- Min instances: 1
- Max instances: 3

Adjust based on load:
```bash
gcloud run services update x-bot \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

## Troubleshooting

### Common Issues

1. **Secret Access Denied**
   - Ensure service account has Secret Manager access
   - Check secret names match exactly

2. **Rate Limiting**
   - Monitor Twitter API usage
   - Adjust `RATE_LIMIT_PER_MINUTE`

3. **Container Build Failures**
   - Check Dockerfile syntax
   - Verify dependencies in requirements.txt

4. **Health Check Failures**
   - Check application logs
   - Verify all secrets are accessible

### Logs and Monitoring
- **Application Logs**: Cloud Logging
- **Metrics**: Cloud Monitoring
- **Alerts**: Set up based on error rates, latency, etc.

## Cost Optimization

### Cloud Run Costs
- Pay per request and CPU/memory usage
- Current config: ~$10-20/month for moderate usage

### Optimization Strategies
1. **Right-size resources**: Monitor and adjust CPU/memory
2. **Implement caching**: Reduce API calls
3. **Batch operations**: Combine multiple actions
4. **Use Cloud Scheduler**: For periodic tasks instead of always-on

## Security Considerations

- Service account uses principle of least privilege
- Secrets encrypted at rest and in transit
- API keys never logged or exposed
- Regular key rotation recommended
- Network access restricted to necessary services