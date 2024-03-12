#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Error: No tag version provided. Please provide a tag version. Example: ./deploy.sh 1.0.0"
  exit 1
fi

TAG_VERSION=$1

TARGET=prod docker-compose -f Dockerfiles/docker-compose.dev.yaml --env-file .env build --no-cache && \
docker tag dockerfiles-back ypeskov/djw:"$TAG_VERSION" && \
docker push ypeskov/djw:"$TAG_VERSION" && \

echo "The image has been pushed to the Docker Hub: $TAG_VERSION"
echo "-------------------"

gcloud run deploy djw-app \
 --image ypeskov/djw:"$TAG_VERSION" \
 --platform managed \
 --region us-central1 \
 --update-env-vars=DB_HOST=34.88.248.216,DB_NAME=djw,DB_USER=djw,DB_PASSWORD=djw,DJANGO_DEBUG='False',DJANGO_ALLOWED_HOSTS=djw-app-pcyblpll6a-uc.a.run.app,TOMORROW_IO_API_KEY=hVAcvTA7FJ4R7VWdP36CwduuEIxe0wq4,EMAIL_HOST=smtp.gmail.com,EMAIL_PORT='587',EMAIL_USE_TLS='True',EMAIL_HOST_USER=yuriy.peskov@gmail.com,EMAIL_HOST_PASSWORD='aaaa',EMAIL_FROM=yuriy.peskov@gmail.com,HOST_REDIS='redis://34.88.248.216:6379' \
 --allow-unauthenticated && \

echo "The image has been deplosyed to the Google Cloud Run: $TAG_VERSION" && \
echo "-------------------" && \

gcloud run services update-traffic djw-app \
 --to-latest \
 --project dj-weather-417004 \
 --region us-central1 && \
echo "$TAG_VERSION" > version.txt && \
echo "The image has been pushed to the Docker Hub and deployed to the Google Cloud Run. Traffic updated to the latest version. Version saved to version.txt: $TAG_VERSION"
echo "-------------------" && \

#gcloud run deploy djw-celery \
# --image ypeskov/djw:"$TAG_VERSION" \
# --platform managed \
# --region us-central1 \
# --command "poetry" \
# --args "run,celery,-A,djweather,worker,-l,info" \
# --update-env-vars=DB_HOST=34.88.248.216,DB_NAME=djw,DB_USER=djw,DB_PASSWORD=djw,DJANGO_DEBUG='False',DJANGO_ALLOWED_HOSTS=djw-app-pcyblpll6a-uc.a.run.app,TOMORROW_IO_API_KEY=hVAcvTA7FJ4R7VWdP36CwduuEIxe0wq4,EMAIL_HOST=smtp.gmail.com,EMAIL_PORT='587',EMAIL_USE_TLS='True',EMAIL_HOST_USER=yuriy.peskov@gmail.com,EMAIL_HOST_PASSWORD='aaaa',EMAIL_FROM=yuriy.peskov@gmail.com,HOST_REDIS='redis://34.88.248.216:6379' \
# --allow-unauthenticated && \
#
#echo "djw-celery has been deployed to the Google Cloud Run: $TAG_VERSION" && \
#echo "-------------------"

#gcloud run deploy djw-celery-beat \
# --image ypeskov/djw:"$TAG_VERSION" \
# --platform managed \
# --region us-central1 \
# --allow-unauthenticated && \
#
#echo "djw-celery-beat has been deplosyed to the Google Cloud Run: $TAG_VERSION" && \
#echo "-------------------"