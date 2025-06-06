# ptrack - Price Tracking App

**ptrack** is a price tracking backend for Colombian e-commerce sites, built on AWS using a serverless architecture. It scrapes product prices from multiple marketplaces, stores product and price history in DynamoDB, and exposes APIs for prices history.

## Project Overview

- **Frontend**: Google Chrome extension for user interaction and product tracking.
- **Backend**: Python-based services, including Scrapy spiders, running on AWS ECS for scalable scraping and data processing.
- **Infrastructure**: Fully serverless deployment on AWS, leveraging services like Lambda, DynamoDB, and API Gateway, managed via the Serverless Framework.
- **Scraping**: Automated price extraction using Scrapy for Colombian e-commerce sites.

## Features
- Daily price scraping from multiple e-commerce websites (exito, falabella, alkosto)
- Price history tracking
- Periodically save html content to s3 for debugging 
- Best offers display: To be implemented
- Price alerts : To be implemented
- Users: To be implemented

## Project Structure
- **backend/**: Contains the backend code and infrastructure configuration.
  - **src/**: Source code for the backend services.
    - **api/**: API service for product price history.
    - **scheduler/**: Service to schedule scraping jobs.
    - **task_launcher/**: Service to launch scraping tasks in ECS.
  - **scripts/**: Utility scripts for building and deploying the backend.
    - **template.yaml**: AWS SAM template for the backend services.
    - **config/**: Configuration for scraping targets one file for each website.
    - **scraper/**: Scrapy project for scraping product prices.
- **frontend/**: Contains the frontend code (Google Chrome extension).

# Disclaimer
This project is for educational purposes only. It is not intended for production use and should not be used to scrape websites without permission. Always check the terms of service of the websites you scrape.