# MyCurrency Project

## Overview
MyCurrency is a Django-based web application that facilitates the management of currencies, fetching exchange rates from various providers, and converting currency amounts. It is built to be extensible and scalable, making it easy to add new features or integrate additional exchange rate providers. The project exposes a REST API that can be used by frontend applications or other services to interact with the system.

## Setup Instructions

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.11 or later
- Redis (for Celery task queue)
- Git

## Clone the Repository

`git clone https://github.com/sanidhya3340/mycurrency`
`cd mycurrency`


## Create and Activate a Virtual Environment

#### On Windows:
- `python -m venv venv`
- `venv\Scripts\activate`
#### On macOS/Linux:
- `python3 -m venv venv`
- `source venv/bin/activate`

## Setup Project
- `python setup_project.py`
- Script will create superuser with username: `admin` password: `admin`

## Postman Collection
- postman collection `mycurrency.postman_collection.json` is in root of the git repo
- you can visit http://localhost:8000/api/admin/currency-converter/ for converter page built by django

## Impovement and Future Enhancements
- Scalability: The system can be scaled by adding support for more exchange rate providers. Implementing caching mechanisms (e.g., with Redis) for frequently accessed rates could greatly improve performance.
- Docker Support: adding Docker support to simplify the setup process for developers and deploy the application consistently across different environments.
- Validation of User on every API.
- Enhanced Error Handling: Current error handling is sufficient, but there is room for improvements, such as more specific error codes and more detailed logging.
- Security Enhancements: Implement rate limiting on certain API endpoints to prevent abuse. Also, make sure all sensitive data is handled securely.
- Asynchronous Historical Data Loading: The current script loads data synchronously; converting it to a fully asynchronous process would improve performance, especially when dealing with large datasets.
- API Versioning: Add support for API versioning to ensure backward compatibility as the application grows.