$PROJECT_ID = "team-2-1771992442"
$SERVICE_NAME = "interactive-graph-v1"
$REGION = "us-central1"

# Submit build to Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --project $PROJECT_ID