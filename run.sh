#!/bin/bash

cat <<EOF >.env
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_DB=test
MONGO_USER=test
MONGO_PASSWORD=test
BACKEND_URL=http://127.0.0.1:5000
EMAIL_EMAIL=
EMAIL_TOKEN=
EOF

docker build -t smartcmms-backend . -f backend/Dockerfile --target build
docker build -t smartcmms-frontend . -f frontend/Dockerfile --target build

docker compose up
