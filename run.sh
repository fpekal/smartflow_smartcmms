#!/bin/bash

cat <<EOF > .env
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_DB=test
MONGO_USER=test
MONGO_PASSWORD=test
EOF

docker build -t smartcmms-backend . -f backend/Dockerfile --target build
docker build -t smartcmms-frontend . -f frontend/Dockerfile --target build

docker compose up
