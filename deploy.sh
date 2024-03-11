#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Error: No tag version provided. Please provide a tag version. Example: ./deploy.sh 1.0.0"
  exit 1
fi

TAG_VERSION=$1

TARGET=prod docker-compose -f Dockerfiles/docker-compose.yaml --env-file .env build --no-cache && \
docker tag dockerfiles-back ypeskov/djangogramm:"$TAG_VERSION" && \
docker push ypeskov/djangogramm:"$TAG_VERSION" && \
gcloud run deploy djangogramm \
 --image ypeskov/djangogramm:"$TAG_VERSION" \
 --platform managed \
 --region us-central1 \
 --allow-unauthenticated && \
gcloud run services update-traffic djangogramm \
 --to-latest \
 --project djangogramm-411918 \
 --region us-central1 && \
echo "$TAG_VERSION" > version.txt && \
echo "The image has been pushed to the Docker Hub and deployed to the Google Cloud Run. Traffic updated to the latest version. Version saved to version.txt: $TAG_VERSION"
