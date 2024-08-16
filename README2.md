
# Region Pricing API

## Overview
The Region Pricing API is a Django-based application designed to handle requests for retrieving average prices between ports and regions. The project is containerized using Docker and Docker Compose, making it easy to set up and run in any environment.

## Features
- Retrieve average prices between ports or regions.
- Handle requests for prices between specific dates.
- Uses PostgreSQL as the database.

## Project Structure
```
region-pricing-api/
│
├── project/
│   ├── Dockerfile # Dockerfile for the backend service
│   ├── manage.py # Django management script
│   ├── settings.py # Django settings file
│   ├── urls.py # URL configurations
│   ├── wsgi.py # WSGI entry point
│   ├── requirements.txt # Python dependencies
│   └── rates/
│       ├── migrations/ # Django migrations
│       ├── models.py # Database models
│       ├── views.py # API views
│       ├── serializers.py # Data serializers
│       ├── test_runner.py # Unit tests settings prevent drop db
│       ├── tests.py # Unit tests
│       └── urls.py # App-specific URLs
│
├── db/
│   ├── Dockerfile # Dockerfile for the PostgreSQL service
│   └── rates.sql # SQL file to initialize the database
│
└── docker-compose.yml # Docker Compose configuration file
```

## Prerequisites
- Docker
- Docker Compose

## Setup and Installation

### 1. Clone the repository
```bash
git clone <repository_url>
cd region-pricing-api
```

### 2. Build and run the Docker containers
```bash
docker-compose up --build
```

### 3. Access the API
The API will be available at http://localhost:8000/.

### 4. Running Tests
To run the test cases, use the following command:
```bash
docker-compose run web python manage.py test --keepdb
```


## API Endpoints

### 1. Get Average Prices
Retrieve average prices between ports or regions.

**URL:** /rates/  
**Method:** GET  
**Params:**  
- `date_from`: The start date for the price range.
- `date_to`: The end date for the price range.
- `origin`: The origin port code or region slug.
- `destination`: The destination port code or region slug.

**Example:**
  ```bash
  curl "http://localhost:8000/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=BEZEE"
  ```
```bash
curl "http://localhost:8000/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=north_europe_main"
```
```bash
curl "http://localhost:8000/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```

## Docker Configuration

### Backend Service (web)
- Build Context: `project/`
- Exposed Port: `8000`
- Command: `python manage.py runserver 0.0.0.0:8000`

### Database Service (db)
- Image: `postgres:13`
- Build Context: `db/`
- Exposed Port: `5432`
- Environment:
  - `POSTGRES_DB`: `postgres`
  - `POSTGRES_USER`: `postgres`
  - `POSTGRES_PASSWORD`: `ratestask`
- Volumes:
  - `postgres_data:/var/lib/postgresql/data`

## Notes
- Ensure that the database service is up and running before accessing the API.
- The API should handle most common requests, including handling of slugs for regions and codes for ports.
- Ensure that while using test use --keepdb command otherwise db will be deleted.
- Db docker file postgres version changed to 13 because of version issues.

## License
This project is licensed under the MIT License.
