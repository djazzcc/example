#!/usr/bin/env bash
# -------------------------
# Docker Entrypoint script.
# Author: @azataiot
# Last update: 2024-05-13
# -----------------------
cat <<-'EOF'
----------------------------
     _  _                  
    | |(_)                 
  __| | _   __ _  ____ ____
 / _` || | / _` ||_  /|_  /
| (_| || || (_| | / /  / / 
 \__,_|| | \__,_|/___|/___|
      _/ |                 
     |__/                  
     @azataiot - 2025 
----------------------------
EOF

set -eux; # Enable debug mode

# Except that the NUM_WORKERS variable is set, the default value is 2
NUM_WORKERS=${NUM_WORKERS:-2};
echo "Number of workers: $NUM_WORKERS"

# Preparation work before starting the Django server
migrate() {
  echo "Applying database migrations..."
  # Apply database migrations
  python manage.py migrate --noinput;
}

# Run the debug server
runserver() {
    echo "Running the development server..."
    python manage.py runserver 0.0.0.0:8000
}

# Run the production server
start_gunicorn() {
    echo "Running the gunicorn production server with $NUM_WORKERS workers..."
    gunicorn djazz.wsgi:application \
          --bind 0.0.0.0:8000 \
          --workers "$NUM_WORKERS" \
          --access-logfile '-' \
          --error-logfile '-' \
          --log-level warning \
          --timeout 300
}

CMD="$1"
echo "Command: $CMD"

if [ "$1" = 'gunicorn' ]; then
    migrate
    start_gunicorn
elif [ "$1" = 'debug' ]; then
    migrate
    runserver
else
    echo "No valid arguments provided; Running the command ($1)..."
    exec "$@"
fi



