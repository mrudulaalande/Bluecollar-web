# 🚀 Blue Collar Hub Cloud Run Deployment Script
# This script automates the deployment of both Backend and Frontend to Google Cloud Run.

$PROJECT_ID = Read-Host "`nEnter your Google Cloud Project ID"
$REGION = "asia-south1"

if (-not $PROJECT_ID) {
    Write-Host "❌ Error: Project ID is required." -ForegroundColor Red
    exit
}

Write-Host "`n🛠️  Setting up Google Cloud configuration..." -ForegroundColor Cyan
gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

Write-Host "`n📦  Step 1: Deploying Backend API..." -ForegroundColor Cyan
# This will build the image and handle deployment in one step using Cloud Build
gcloud run deploy bluecollar-api `
    --source . `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="SERVICE_TYPE=api" `
    --port 8080 `
    --timeout 300 `
    --quiet

# Get the URL of the deployed backend
$BACKEND_URL = (gcloud run services describe bluecollar-api --region $REGION --format='value(status.url)')
Write-Host "`n✅ Backend deployed at: $BACKEND_URL" -ForegroundColor Green

Write-Host "`n🎨  Step 2: Deploying Frontend UI..." -ForegroundColor Cyan
gcloud run deploy bluecollar-ui `
    --source . `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="SERVICE_TYPE=ui,API_BASE_URL=$BACKEND_URL" `
    --port 8080 `
    --timeout 300 `
    --quiet

$FRONTEND_URL = (gcloud run services describe bluecollar-ui --region $REGION --format='value(status.url)')

Write-Host "`n🎉  Deployment Complete!" -ForegroundColor Green
Write-Host "-------------------------------------------"
Write-Host "🔗 Backend API:  $BACKEND_URL"
Write-Host "🔗 Frontend UI:  $FRONTEND_URL" -ForegroundColor Yellow
Write-Host "-------------------------------------------"
Write-Host "Access your application using the Frontend URL above."
