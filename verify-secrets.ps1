# Verify X-Bot Secret Manager Setup
# This script checks if your secrets are properly configured

Write-Host "🔍 X-Bot Secret Verification" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# Check if secrets exist
Write-Host "📋 Checking secret existence:" -ForegroundColor Yellow
$secrets = @("twitter-client-id", "twitter-client-secret", "twitter-bearer-token", "twitter-access-token", "twitter-access-token-secret", "coingecko-api-key")

foreach ($secret in $secrets) {
    try {
        $result = gcloud secrets describe $secret --format="value(name)" 2>$null
        if ($result) {
            Write-Host "✅ $secret - EXISTS" -ForegroundColor Green
        }
        else {
            Write-Host "❌ $secret - MISSING" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ $secret - MISSING" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔗 Testing bot endpoints:" -ForegroundColor Yellow

# Test status endpoint
try {
    $statusResponse = Invoke-WebRequest -Uri "https://x-bot-631505722920.us-central1.run.app/status" -TimeoutSec 10
    if ($statusResponse.StatusCode -eq 200) {
        Write-Host "✅ /status endpoint - RESPONDING" -ForegroundColor Green
        $status = $statusResponse.Content | ConvertFrom-Json
        Write-Host "   Status: $($status.status)" -ForegroundColor White
    }
    else {
        Write-Host "❌ /status endpoint - ERROR ($($statusResponse.StatusCode))" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ /status endpoint - UNREACHABLE" -ForegroundColor Red
}

# Test metrics endpoint
try {
    $metricsResponse = Invoke-WebRequest -Uri "https://x-bot-631505722920.us-central1.run.app/metrics" -TimeoutSec 10
    if ($metricsResponse.StatusCode -eq 200) {
        Write-Host "✅ /metrics endpoint - RESPONDING" -ForegroundColor Green
        if ($metricsResponse.Content -match "posts_total") {
            Write-Host "   Metrics: Prometheus format detected" -ForegroundColor White
        }
    }
    else {
        Write-Host "❌ /metrics endpoint - ERROR ($($metricsResponse.StatusCode))" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ /metrics endpoint - UNREACHABLE" -ForegroundColor Red
}

Write-Host ""
Write-Host "📊 Secret Access Audit:" -ForegroundColor Yellow
Write-Host "Recent secret access logs:" -ForegroundColor White
gcloud logging read "resource.type=secretmanager.googleapis.com/Secret" --limit=5 --format="table(timestamp,severity,resource.labels.secret_id,textPayload)" --freshness=1h

Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "========" -ForegroundColor Cyan
Write-Host "• If secrets are missing, run: .\setup-secrets.ps1"
Write-Host "• Check Cloud Run logs for authentication errors"
Write-Host "• Secrets are automatically rotated when updated"
Write-Host "• All access is logged for audit purposes"