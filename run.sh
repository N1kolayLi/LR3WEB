#!/bin/bash
# Gunicorn startup script for Linux/macOS/WSL

set -e

# Load environment variables from .env if it exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Set defaults if not defined
BIND="${GUNICORN_BIND:-0.0.0.0:8000}"
WORKERS="${GUNICORN_WORKERS:-4}"
WORKER_CLASS="${GUNICORN_WORKER_CLASS:-sync}"
LOG_LEVEL="${GUNICORN_LOG_LEVEL:-info}"

echo "Starting LR3WEB with Gunicorn..."
echo "Bind: $BIND"
echo "Workers: $WORKERS"
echo "Worker Class: $WORKER_CLASS"
echo "Log Level: $LOG_LEVEL"
echo ""

# Activate virtual environment if it exists
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Install/upgrade packages
echo "Ensuring dependencies are installed..."
pip install -q -r requirements.txt

# Run Gunicorn
gunicorn \
    --bind=$BIND \
    --workers=$WORKERS \
    --worker-class=$WORKER_CLASS \
    --log-level=$LOG_LEVEL \
    --config=gunicorn_config.py \
    LR3_WEB:app

echo "Gunicorn server stopped."
