# X-Bot: Enterprise Twitter Automation for $wifDOG Community

A production-ready, enterprise-grade Twitter bot for $wifDOG community promotion with comprehensive monitoring, security, and DevSecOps practices.

<!-- Updated: 2025-09-16 - Testing deployment after Twitter credential update -->


<!-- Updated: 2025-09-16 - Testing deployment after IAM permission fix -->


## 🚀 Features

### Core Functionality
- **Market Intelligence**: Automated trending memecoin posts with real-time pricing
- **Community Engagement**: Smart tweet interactions with spam filtering
- **Promotional Content**: Scheduled community promotion posts
- **Rate Limiting**: Twitter API compliance with intelligent throttling

### Enterprise Features
- **Google Cloud Integration**: Secret Manager, Cloud Run, Cloud Logging, Cloud Monitoring
- **Comprehensive Monitoring**: Prometheus metrics, structured logging, alerting
- **Security First**: OAuth 2.0, encrypted secrets, principle of least privilege
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Code Quality**: 100% test coverage, type checking, linting

### Technical Stack
- **Backend**: FastAPI, Uvicorn, Python 3.10
- **APIs**: Twitter API v2, CoinGecko API
- **Cloud**: Google Cloud Platform (Cloud Run, Secret Manager, Cloud Logging)
- **Monitoring**: Prometheus, Cloud Monitoring, structured logging
- **Development**: pytest, mypy, flake8, black, isort, pre-commit hooks

## 📋 Prerequisites

### Local Development
- Python 3.10+
- Docker
- Twitter Developer Account with API v2 access
- CoinGecko API key (optional)

### Production Deployment
- Google Cloud Platform account
- GitHub repository with Actions enabled
- Service account with appropriate GCP roles

## 🛠️ Quick Start (Development)

```bash
# Clone repository
git clone <your-repo-url>
cd x-bot

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
make test

# Run locally
python -m src.main
```

## 🚀 Production Deployment

### 1. Google Cloud Setup
```bash
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com

# Create service account
gcloud iam service-accounts create x-bot-sa \
  --description="X-Bot service account" \
  --display-name="X-Bot SA"
```

### 2. Secrets Configuration
Create secrets in Google Cloud Secret Manager:
- `twitter-client-id`
- `twitter-client-secret`
- `twitter-bearer-token`
- `twitter-access-token`
- `twitter-access-token-secret`
- `coingecko-api-key` (optional)

### 3. GitHub Repository Setup
Add these secrets in GitHub repository settings:
- `GCP_SA_KEY`: Service account JSON key
- `GCP_PROJECT_ID`: Your GCP project ID
- `GOOGLE_CREDENTIALS`: Same as GCP_SA_KEY

### 4. Deploy
```bash
# Push to GitHub (triggers CI/CD)
git add .
git commit -m "Production deployment"
git push origin main

# Monitor deployment in GitHub Actions
# Check Cloud Run service in GCP Console
```

## 📊 Monitoring & Health Checks

### Application Endpoints
- `GET /` - Health check
- `GET /status` - Bot status and last activities
- `GET /metrics` - Prometheus metrics

### Cloud Monitoring
- **Dashboards**: CPU, memory, request metrics
- **Alerts**: Service down, high error rates, rate limits
- **Logs**: Structured logging with Cloud Logging

## 🧪 Development

### Code Quality
```bash
# Run all quality checks
make format    # Black + isort
make lint      # flake8
make type-check # mypy
make test      # pytest with coverage
make security  # Security checks
```

### Testing
```bash
# Run tests
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_bot.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## 📚 Documentation

- **[API Documentation](docs/api.md)** - Endpoint specifications and bot functionality
- **[Deployment Guide](docs/deployment.md)** - Detailed production deployment steps
- **[Monitoring Setup](docs/monitoring.md)** - Monitoring, alerting, and troubleshooting

## 🔒 Security

### Secrets Management
- All credentials stored in Google Cloud Secret Manager
- No secrets in code or environment variables
- Service account with minimal required permissions

### API Security
- OAuth 2.0 authentication with Twitter
- Rate limiting to prevent API abuse
- Input validation and sanitization

### Code Security
- Dependency vulnerability scanning
- Static code analysis
- Pre-commit hooks for code quality

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Twitter API   │    │  CoinGecko API  │    │  Cloud Logging  │
│     (OAuth2)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │    X-Bot       │
                    │  (FastAPI)     │
                    │                 │
                    │ • Engagement   │
                    │ • Market Data  │
                    │ • Rate Limiter │
                    │ • Spam Detect  │
                    │ • Scheduler    │
                    │ • Metrics      │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Cloud Run     │
                    │  (Container)   │
                    └─────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all quality checks pass
5. Submit pull request

## 📄 License

This project is proprietary software for $wifDOG community use.

## 🆘 Support

For issues and questions:
1. Check the [troubleshooting guide](docs/monitoring.md)
2. Review application logs in Cloud Logging
3. Check GitHub Actions for deployment issues
4. Monitor metrics in Cloud Monitoring

---

**Built with ❤️ for the $wifDOG community**
