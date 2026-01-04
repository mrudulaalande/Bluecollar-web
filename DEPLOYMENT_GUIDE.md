# 🚀 Senior DevOps Deployment Guide: Cloud Run (India)

This guide provides the exact terminal commands to build, push, and deploy the **Blue Collar Hub** application to Google Cloud Run in the `asia-south1` region.

## 📁 0. Project Structure Check
After deployment, your root directory should look like this:
```text
.
├── backend/            # FastAPI Source
├── frontend/           # Streamlit Source
├── Dockerfile          # Optimized Multi-role Dockerfile
├── start.sh            # Production Startup Script
├── requirements.txt    # Audited Dependencies (inc. gunicorn)
└── DEPLOYMENT_GUIDE.md # This Guide
```

## 🛠️ 1. Setup & Configuration
Set your variables first:
```powershell
$PROJECT_ID = "YOUR_PROJECT_ID"
$REGION = "asia-south1"
$REPO_NAME = "bluecollar-app"
$IMAGE_NAME = "bluecollar-hub"
$AR_URL = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME"

gcloud config set project $PROJECT_ID
```

## 📦 2. Google Cloud Infrastructure
Enable services and create the Artifact Registry:
```powershell
# Enable APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Create Repository
gcloud artifacts repositories create $REPO_NAME `
    --repository-format=docker `
    --location=$REGION `
    --description="Docker repository for Blue Collar Hub"

# Configure Auth
gcloud auth configure-docker $REGION-docker.pkg.dev
```

## 🏗️ 3. Build & Push Image
Build the unified production-ready image:
```powershell
docker build -t $AR_URL:latest .
docker push $AR_URL:latest
```

## 🚀 4. Cloud Run Deployment

### Option A: Automated Script (Recommended)
We have provided a PowerShell script to automate the entire process (Build + Deploy Backend + Deploy Frontend).
1. Open PowerShell in the project root.
2. Run: `./deploy_to_cloud.ps1`
3. Follow the prompts for your Project ID.

### Option B: Manual Commands
#### 1. Deploy Backend API
```powershell
gcloud run deploy bluecollar-api `
    --source . `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="SERVICE_TYPE=api" `
    --port 8080
```
**🔔 NOTE:** Copy the URL output (e.g., `https://api-xxx.a.run.app`) for the next step.

#### 2. Deploy Frontend UI
Replace `[BACKEND_URL]` with the URL from Step 1:
```powershell
gcloud run deploy bluecollar-ui `
    --source . `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars="SERVICE_TYPE=ui,API_BASE_URL=[BACKEND_URL]" `
    --port 8080
```

## 🔍 5. Verification & Logs
**Final Public URL:** Follow the output of the Frontend deployment.

**View Production Logs:**
```powershell
# For Backend
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=bluecollar-api" --limit 20

# For Frontend
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=bluecollar-ui" --limit 20
```

## 💡 Senior DevOps Recommendations
1.  **Database**: Cloud Run is stateless. SQLite is fine for demos, but for production, use **Cloud SQL (MySQL)**. Update `DATABASE_URL` in env vars.
2.  **Statelessness**: Uploaded files (`uploads/`) will be lost on container restart. Use **Cloud Storage** for permanent file storage.
3.  **Secrets**: Use **Secret Manager** for API keys like Razorpay/Stripe secrets instead of plain environment variables.
4.  **Scaling**: Cloud Run scales to zero. These commands provide a "Managed" experience with automatic scaling.
