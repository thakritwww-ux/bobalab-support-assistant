#!/usr/bin/env sh
set -eu
python -m app.cli migrate
python -m app.cli seed
exec gunicorn 'app:create_app()' --bind "0.0.0.0:${PORT:-8000}" --workers 1 --threads 4 --timeout 120 --error-logfile -
