# ptrack Backend

## Overview

**ptrack** is a  price tracking backend system designed specifically for Colombian e-commerce sites. Built on AWS using a serverless architecture, it provides real-time price monitoring and historical price data analysis capabilities. The system automatically scrapes product prices from multiple marketplaces, maintains comprehensive price history in DynamoDB, and exposes RESTful APIs for accessing price data.

### Key Features

- Real-time price monitoring across multiple Colombian e-commerce sites
- Historical price tracking and analysis
- Serverless architecture for cost-effective scaling
- Automated scraping with configurable schedules
- RESTful API for price data access
- Centralized logging and monitoring

---

## Architecture

### Main Components

#### AWS Lambda Functions

- **ApiFunction** (`/src/api/app.py`)
  - Handles all API requests
  - Provides RESTful endpoints for price data access
  - Implements rate limiting and request validation
  - Endpoints:
    - `GET /products/{product_url}`: Retrieve product historical prices
    - `GET /products/{product_url}/stats`: Get price statistics and trends

- **ScrapingScheduler** (`/src/scheduler/app.py`)
  - Manages scraping job scheduling
  - Reads configuration from `targets.json`
  - Sends jobs to SQS queue for processing
  - Implements retry logic and error handling

- **ScrapingTaskLauncher** (`/src/task_launcher/app.py`)
  - Triggered by SQS messages
  - Launches ECS Fargate tasks for scraping
  - Manages container configuration and environment variables
  - Handles task lifecycle and monitoring

#### Data Storage

- **Amazon DynamoDB Tables**
  - `products-*`: Product metadata and current information
  - `price-history-*`: Historical price data with timestamps
  - `targets-*`: Scraping targets and configuration

#### Infrastructure

- **Amazon ECS (Fargate)**
  - Runs containerized Scrapy-based scrapers
  - Auto-scales based on workload

- **Amazon SQS**
  - Message queue for job processing
  - Decouples scheduling from task execution

- **Amazon S3**
  - Stores site-specific configuration files (YAML)
  - Maintains scraping rules and selectors
  - Hosts static assets and templates

- **CloudWatch Logs**
  - Centralized logging for all components
  - Real-time monitoring and alerting
  - Log retention and analysis

---

## Development Setup

### Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed and running
- Python 3.8 or higher
- AWS SAM for infrastructure deployment

### Local Development

1. Clone the repository
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Deployment

1. Build and push the Scrapy Docker image:
   ```sh
   cd backend/scripts
   ./build-and-push.sh
   ```
2. Deploy infrastructure:
   ```sh
   SAM build
   SAM deploy
   ```
3. Sync static files


