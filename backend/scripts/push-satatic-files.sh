#!/bin/bash
set -e

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
STATIC_FILES_BUCKET="static-files-${AWS_ACCOUNT_ID}-dev"
BUCKET_URI="s3://${STATIC_FILES_BUCKET}"


# S3 Bucket URI
cd "$(dirname "$0")/../"

# copy static files to S3 bucket
echo "======== Pushing static files to S3 bucket ========"
echo "AWS Region: ${AWS_REGION}"
echo "S3 Bucket: ${STATIC_FILES_BUCKET}"
echo "====================================================" 


# Sync static files to S3 bucket
echo "Syncing static files to S3 bucket..."
aws s3 sync ./config s3://${STATIC_FILES_BUCKET}/config 
echo "Static files pushed to S3 bucket successfully."