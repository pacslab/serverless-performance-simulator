IMAGE_NAME=nimamahmoudi/simfaas-api

docker build -t $IMAGE_NAME:latest -f Dockerfile ../
docker run -it --rm -p 5000:5000 --name simfaasapi $IMAGE_NAME
