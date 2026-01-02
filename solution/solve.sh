#!/bin/bash
set -e


cat > README.md << 'EOF'
# Polyglot Microservices Platform

![CI](https://github.com/JoramWells/polygot-microservices/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/JoramWells/polygot-microservices/branch/main/graph/badge.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A modern microservices architecture demonstrating polyglot development with services written in Python, Node.js, and Go. This platform showcases inter-service communication, containerization, and automated CI/CD pipelines.

## Architecture Overview

This repository contains a microservices-based e-commerce platform with three core services:

- **User Service**: Handles user authentication and profile management
- **Order Service**: Manages customer orders and orchestrates transactions
- **Inventory Service**: Tracks product inventory and availability

The services communicate via REST APIs and are orchestrated using Docker Compose for local development and testing.

## Architecture Diagram

![Architecture](../environment/workspace/architecture.png)

## Services Overview

| Service | Technology | Port | Description |
|---------|-----------|------|-------------|
| User Service | Python 3.10 + Flask | 5000 | User account management and authentication |
| Order Service | Node.js 18 + Express | 3000 | Order processing and workflow orchestration |
| Inventory Service | Go 1.18 | 4000 | Product inventory tracking |

## Prerequisites

Before running this project, ensure you have the following installed:

- **Docker**: >= 20.10.0
- **Docker Compose**: >= 2.0.0
- **Git**: >= 2.30.0

For local development without Docker:
- **Python**: >= 3.10
- **Node.js**: >= 18.0.0
- **Go**: >= 1.18

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/JoramWells/polygot-microservices
cd microservices
```

### 2. Start All Services with Docker Compose
```bash
docker-compose up -d
```

### 3. Verify Services are Running

Check that all services are healthy:
```bash
# User Service
curl http://localhost:5000/health

# Order Service
curl http://localhost:3000/health

# Inventory Service
curl http://localhost:4000/health
```

Expected response from each service:
```json
{
  "status": "healthy",
  "service": "<service-name>"
}
```

## Per-Service Setup Instructions

### User Service (Python/Flask)

#### Local Development Setup
```bash
cd services/user-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

#### Run Tests
```bash
pytest tests/
```

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port number for the service | 5000 |

### Order Service (Node.js/Express)

#### Local Development Setup
```bash
cd services/order-service

# Install dependencies
npm install

# Run the service
npm start
```

#### Run Tests
```bash
npm test
```

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port number for the service | 3000 |
| `USER_SERVICE_URL` | URL of the User Service | http://user-service:5000 |
| `INVENTORY_SERVICE_URL` | URL of the Inventory Service | http://inventory-service:4000 |

### Inventory Service (Go)

#### Local Development Setup
```bash
cd services/inventory-service

# Download dependencies
go mod download

# Build the service
go build -o inventory-service .

# Run the service
./inventory-service
```

#### Run Tests
```bash
go test -v
```

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port number for the service | 4000 |

## API Documentation

### User Service API

**Base URL**: `http://localhost:5000`

#### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/users` | Get all users |
| GET | `/api/v1/users/:id` | Get user by ID |
| POST | `/api/v1/users` | Create a new user |

#### Example: Create a User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user-123",
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

Response:
```json
{
  "id": "user-123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Order Service API

**Base URL**: `http://localhost:3000`

#### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/orders` | Get all orders |
| GET | `/api/v1/orders/:id` | Get order by ID |
| POST | `/api/v1/orders` | Create a new order |

#### Example: Create an Order
```bash
curl -X POST http://localhost:3000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user-123",
    "items": [
      {"productId": "prod-1", "quantity": 2}
    ]
  }'
```

Response:
```json
{
  "id": "1234567890",
  "userId": "user-123",
  "items": [
    {"productId": "prod-1", "quantity": 2}
  ],
  "status": "pending"
}
```

### Inventory Service API

**Base URL**: `http://localhost:4000`

#### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/inventory` | Get all products |
| GET | `/api/v1/inventory/:id` | Get product by ID |

#### Example: Get Product
```bash
curl http://localhost:4000/api/v1/inventory/prod-1
```

Response:
```json
{
  "id": "prod-1",
  "name": "Widget",
  "quantity": 100,
  "price": 29.99
}
```

## Docker Compose Usage

### Build All Services
```bash
docker-compose build
```

### Start All Services
```bash
docker-compose up -d
```

### View Logs

View logs from all services:
```bash
docker-compose logs -f
```

View logs from a specific service:
```bash
docker-compose logs -f user-service
```

### Stop All Services
```bash
docker-compose down
```

### Rebuild a Single Service
```bash
docker-compose up -d --build user-service
```

## Testing

### Run Tests for Individual Services

**User Service:**
```bash
cd services/user-service
pytest tests/
```

**Order Service:**
```bash
cd services/order-service
npm test
```

**Inventory Service:**
```bash
cd services/inventory-service
go test -v
```

### Run All Tests
```bash
# User Service
(cd services/user-service && pytest tests/)

# Order Service
(cd services/order-service && npm test)

# Inventory Service
(cd services/inventory-service && go test -v)
```

### View Test Coverage

**Python:**
```bash
cd services/user-service
pytest --cov=. tests/
```

**Node.js:**
```bash
cd services/order-service
npm test -- --coverage
```

**Go:**
```bash
cd services/inventory-service
go test -cover
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### Workflow

The CI pipeline (`.github/workflows/ci.yml`) runs on:
- Push to `main` or `develop` branches
- Pull requests to `main`

### Jobs

1. **test-user-service**: Runs Python tests
2. **test-order-service**: Runs Node.js tests
3. **test-inventory-service**: Runs Go tests

Each job runs independently and reports its status. All jobs must pass before a pull request can be merged.

### Viewing CI/CD Status

- View workflow runs in the GitHub Actions tab
- Check badge status in this README
- View detailed logs for each job in the Actions interface

## Contributing

We welcome contributions to this project! Here's how you can help:

### Submitting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template
3. Provide clear reproduction steps for bugs
4. Include relevant logs and screenshots

### Creating Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write/update tests
5. Ensure all tests pass locally
6. Commit using conventional commits (see below)
7. Push to your fork
8. Open a pull request with a clear description

### Code Style Guidelines

- **Python**: Follow PEP 8, use `black` for formatting
- **Node.js**: Follow Airbnb style guide, use `prettier`
- **Go**: Follow standard Go conventions, use `gofmt`

### Commit Message Conventions

Use Conventional Commits format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(user-service): add email validation

Added email format validation to user creation endpoint.
Prevents invalid email addresses from being stored.

Closes #123
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
EOF

echo "README.md created successfully"
ls -lh /workspace/README.md