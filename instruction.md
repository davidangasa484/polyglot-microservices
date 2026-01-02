# Write Comprehensive Polyglot Microservices README

Your task is to create a comprehensive `README.md` file for the polyglot microservices repository located at `/workspace`.

## Context

The repository contains a microservices architecture with three services written in different languages:
- **User Service** (Python/Flask) - Port 5000
- **Order Service** (Node.js/Express) - Port 3000
- **Inventory Service** (Go) - Port 4000

The services communicate with each other and can be orchestrated using Docker Compose. A CI/CD workflow exists in `.github/workflows/ci.yml`.

## Requirements

Your README.md must include the following sections in this order:

### 1. Title and Badges
- Project title: "Polyglot Microservices Platform"
- Badges for:
  - CI/CD status (GitHub Actions)
  - Code coverage (Codecov)
  - License (MIT)

### 2. Architecture Overview
- Brief description of the microservices architecture
- Mention of the three services and their purposes
- Reference to an architecture diagram (assume `architecture.png` exists)

### 3. Architecture Diagram
- Include the architecture diagram image
- Use markdown image syntax: `![Architecture](./architecture.png)`

### 4. Services Overview
A table listing all services with:
- Service name
- Technology stack
- Port number
- Description

### 5. Prerequisites
List all required tools:
- Docker and Docker Compose (with minimum versions)
- Programming language runtimes for local development
- Git

### 6. Quick Start
Step-by-step instructions to:
1. Clone the repository
2. Start all services with Docker Compose
3. Verify services are running
4. Access health check endpoints

### 7. Per-Service Setup Instructions

For each service, provide:
- **Local Development Setup** (without Docker)
  - How to install dependencies
  - How to run the service
  - How to run tests
- **Environment Variables**
  - List and describe all environment variables
  - Provide example values

### 8. API Documentation

For each service, document:
- Base URL
- Available endpoints with:
  - HTTP method
  - Endpoint path
  - Description
  - Request body example (for POST/PUT)
  - Response example

Provide at least 2 example curl commands showing:
- Creating a user
- Creating an order

### 9. Docker Compose Usage

Document:
- How to build all services: `docker-compose build`
- How to start all services: `docker-compose up -d`
- How to view logs: `docker-compose logs -f [service-name]`
- How to stop services: `docker-compose down`
- How to rebuild a single service

### 10. Testing

Explain how to:
- Run tests for each service individually
- Run all tests
- View test coverage

### 11. CI/CD Pipeline

Describe:
- The GitHub Actions workflow
- What jobs run on each push
- How to view CI/CD status

### 12. Contributing

Include:
- How to submit issues
- How to create pull requests
- Code style guidelines
- Commit message conventions (e.g., Conventional Commits)

### 13. License

State that the project is under MIT License.

## Constraints

- The README.md must be created at `/workspace/README.md`
- Use proper markdown formatting throughout
- Code blocks must specify the language for syntax highlighting
- All URLs and file paths must be accurate
- Badge URLs should follow this format:
  - CI: `https://github.com/JoramWells/polygot-microservices/workflows/CI/badge.svg`
  - Coverage: `https://codecov.io/gh/JoramWells/polygot-microservices/branch/main/graph/badge.svg`
  - License: `https://img.shields.io/badge/License-MIT-blue.svg`
- Curl examples must use `localhost` and the correct ports
- Do not modify any existing code or configuration files

## Information Gathering

You should examine the following files to gather information:
- Service code files (`app.py`, `index.js`, `main.go`)
- Dockerfile for each service
- `docker-compose.yml`
- `.github/workflows/ci.yml`
- `package.json`, `requirements.txt`, `go.mod`

Use commands like `cat`, `grep`, `tree`, and `ls` to explore the repository structure and understand the services.

## Success Criteria

Your README.md will be evaluated based on:
1. Completeness - All required sections are present
2. Accuracy - Information matches the actual code and configuration
3. Clarity - Instructions are clear and well-organized
4. Markdown Quality - Proper formatting, headers, code blocks
5. Usability - Someone new to the project can follow the instructions successfully

## Files

- **Input**: All files in `/workspace` directory
- **Output**: `/workspace/README.md`