# Cloud Secret Manager Setup for X-Bot
# Run these commands to populate your secrets with actual values

# Twitter API Credentials
echo "your-twitter-client-id-here" | gcloud secrets versions add twitter-client-id --data-file=-
echo "your-twitter-client-secret-here" | gcloud secrets versions add twitter-client-secret --data-file=-
echo "your-twitter-bearer-token-here" | gcloud secrets versions add twitter-bearer-token --data-file=-
echo "your-twitter-access-token-here" | gcloud secrets versions add twitter-access-token --data-file=-
echo "your-twitter-access-token-secret-here" | gcloud secrets versions add twitter-access-token-secret --data-file=-

# CoinGecko API Key
echo "your-coingecko-api-key-here" | gcloud secrets versions add coingecko-api-key --data-file=-

# Verification - list all secrets
gcloud secrets list

# Verification - check a secret version
gcloud secrets versions list twitter-client-id