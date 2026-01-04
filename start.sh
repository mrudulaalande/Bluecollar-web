#!/bin/bash

# Use the PORT environment variable provided by Cloud Run, or default to 8080
PORT=${PORT:-8080}

if [ "$SERVICE_TYPE" == "api" ]; then
    echo "🚀 Starting Backend API on port $PORT..."
    # Using gunicorn with uvicorn workers for production
    exec gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
elif [ "$SERVICE_TYPE" == "ui" ]; then
    echo "🎨 Starting Frontend UI on port $PORT..."
    if [ -z "$API_BASE_URL" ]; then
        echo "⚠️ WARNING: API_BASE_URL is not set."
    fi
    exec streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
else
    echo "🏠 Starting both services (Development Mode)..."
    python -m backend.init_db
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
    sleep 5
    python -m streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
fi
