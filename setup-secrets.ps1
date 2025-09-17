# Secure Secret Setup for X-Bot
# This script securely adds your API credentials to Cloud Secret Manager
# Run this in PowerShell to interactively add your secrets

Write-Host "🔐 X-Bot Secret Manager Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will securely add your API credentials to Google Cloud Secret Manager."
Write-Host "Your secrets will be encrypted and stored securely in the cloud."
Write-Host ""

# Function to add a secret
function Add-Secret {
    param(
        [string]$SecretName,
        [string]$Description
    )

    Write-Host "📝 $Description" -ForegroundColor Yellow
    $secretValue = Read-Host "Enter your $SecretName" -AsSecureString
    $plainText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretValue))

    if ($plainText) {
        Write-Host "🔒 Adding $SecretName to Secret Manager..." -ForegroundColor Green
        $plainText | gcloud secrets versions add $SecretName --data-file=-
        Write-Host "✅ $SecretName added successfully!" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Skipped $SecretName" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Add Twitter API credentials
Write-Host "🐦 Twitter API Credentials" -ForegroundColor Magenta
Write-Host "-------------------------" -ForegroundColor Magenta
Add-Secret "twitter-client-id" "Twitter Client ID (from Twitter Developer Portal)"
Add-Secret "twitter-client-secret" "Twitter Client Secret (from Twitter Developer Portal)"
Add-Secret "twitter-bearer-token" "Twitter Bearer Token (from Twitter Developer Portal)"
Add-Secret "twitter-access-token" "Twitter Access Token (from Twitter Developer Portal)"
Add-Secret "twitter-access-token-secret" "Twitter Access Token Secret (from Twitter Developer Portal)"

# Add CoinGecko API key
Write-Host "📈 CoinGecko API Key" -ForegroundColor Magenta
Write-Host "-------------------" -ForegroundColor Magenta
Add-Secret "coingecko-api-key" "CoinGecko API Key (from CoinGecko Developer Portal - optional)"

# Verification
Write-Host "🔍 Verification" -ForegroundColor Cyan
Write-Host "==============" -ForegroundColor Cyan
Write-Host "Listing all secrets:" -ForegroundColor White
gcloud secrets list --format="table(name,createTime)"

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host "Your secrets are now securely stored in Google Cloud Secret Manager."
Write-Host "The X-Bot will automatically retrieve them at runtime."
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Test the bot by checking the /status endpoint"
Write-Host "2. Monitor the logs for any authentication issues"
Write-Host "3. The bot should start posting and engaging once secrets are available"