# ptrack Backend

## Overview

**ptrack** is a price tracking backend for Colombian e-commerce sites, built on AWS using a serverless architecture. It scrapes product prices from multiple marketplaces, stores product and price history in DynamoDB, and exposes APIs for prices history.

---

## Architecture

### Main Components

- **AWS Lambda Functions**
  - **ApiFunction**: Handles API requests.

  - **ScrapingScheduler**: Schedules scraping jobs and sends messages to SQS.
  - **ScrapingTaskLauncher**: Listens to SQS, launches ECS scraping tasks.

- **Amazon ECS (Fargate)**
  - Runs the Scrapy-based scraper in containers.

- **Amazon SQS**
  - Decouples scheduling from task launching.

- **Amazon DynamoDB**
  - `products-*`: Stores product metadata.
  - `price-history-*`: Stores price history.
  - `targets-*`: Stores scraping targets.

- **Amazon S3**
  - Stores static configuration files (YAML) for each site.

- **CloudWatch Logs**
  - Centralized logging for ECS tasks and Lambda functions.

---

## Function Descriptions

### 1. ApiFunction

- **Path:** `/src/api/app.py`
- **Purpose:** Exposes API endpoints for prices and product info.
- **Endpoints:**
  - `GET /products/{product_url}`: Get product historical prices

### 2. ScrapingScheduler

- **Path:** `/src/scheduler/app.py`
- **Purpose:** Reads `targets.json` and sends jobs to the SQS queue for processing.
- **How it works:** Loads job definitions, sends each as a message to SQS.

### 3. ScrapingTaskLauncher

- **Path:** `/src/task_launcher/app.py`
- **Purpose:** Triggered by SQS messages, launches ECS Fargate tasks to run the scraper.
- **How it works:** Reads job details, sets environment variables, and starts a container task.

---

## Deployment Guide

### 1. Build and Push Docker Image

Build and push the Scrapy Docker image to ECR:

```sh
cd backend/scripts
[build-and-push.sh](http://_vscodecontentref_/0)