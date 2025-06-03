#!/bin/bash
set -e

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPOSITORY="priceco-scraper"
IMAGE_TAG="latest"

# ECR Registry URI
ECR_REGISTRY_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# ECR Repository URI
ECR_REPOSITORY_URI="${ECR_REGISTRY_URI}/${ECR_REPOSITORY}"

cd "$(dirname "$0")/../scraper"

echo "======== Building and delivering the Docker image ========"
# Build the Docker image
echo "AWS Region: ${AWS_REGION}"
echo "ECR Repository: ${ECR_REPOSITORY}"
echo "Image Tag: ${IMAGE_TAG}"
echo "=========================================================="

# Build the Docker image
echo "Building Docker image..."
docker build -t ${ECR_REPOSITORY}:${IMAGE_TAG} .

# Tag the Docker image
echo "Tagging Docker image..."
docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REPOSITORY_URI}:${IMAGE_TAG}
