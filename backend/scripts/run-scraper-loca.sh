#!/bin/bash
set -e

# Env variables
PRODUCTS_TABLE="products-dev"
PRICE_HISTORY_TABLE="price-history-dev"

DOCKER_ENV_FLAGS="-e PRODUCTS_TABLE=$PRODUCTS_TABLE -e PRICE_HISTORY_TABLE=$PRICE_HISTORY_TABLE"

# load aws credentials from ../.env
if [ -f ../.env ]; then
    echo "Loading environment variables from ../.env"
    export $(grep -v '^#' ../.env | xargs)
    echo "Environment variables loaded successfully."
    DOCKER_ENV_FLAGS="$DOCKER_ENV_FLAGS -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_REGION"
else
    echo "No .env file found in the parent directory. Using default environment variables."
    exit 1
fi

docker run --rm -it \
    $DOCKER_ENV_FLAGS \
    priceco-scraper scrapy crawl exito