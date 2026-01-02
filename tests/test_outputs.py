"""
Unit tests for polyglot microservices README generation task.

This test suite verifies that the README.md contains all required sections,
accurate information, proper formatting, and follows best practices for
technical documentation.

Each test checks a specific aspect of the README to ensure completeness
and quality.
"""

import pytest
import os
import re


def test_readme_file_exists():
    """
    Check that README.md was created in the correct location.
    
    The agent must create the file at /workspace/README.md.
    This is the most basic requirement - without this file, the task fails.
    """
    assert os.path.exists('/workspace/README.md'), \
        "README.md file not found at /workspace/README.md"


def test_readme_not_empty():
    """
    Verify that README.md has substantial content.
    
    A comprehensive README for a polyglot microservices project should
    be at least 2000 characters. This prevents agents from creating
    minimal or placeholder documentation.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert len(content) > 2000, \
        f"README.md is too short ({len(content)} chars). Expected at least 2000 characters."


def test_title_and_badges_section():
    """
    Verify the title and CI/CD badges are present.
    
    Checks for:
    - Main project title containing 'Microservices'
    - CI/CD badge (GitHub Actions)
    - Code coverage badge (Codecov)
    - License badge (MIT)
    
    These badges are standard in modern open-source projects.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    # Check for main title (must be H1 with 'Microservices')
    assert re.search(r'^#\s+.*Microservices', content, re.MULTILINE | re.IGNORECASE), \
        "Main title with 'Microservices' not found"
    
    # Check for CI badge
    assert 'workflows/CI/badge.svg' in content or 'github.com' in content, \
        "CI badge not found"
    
    # Check for coverage badge
    assert 'codecov.io' in content or 'coverage' in content.lower(), \
        "Coverage badge not found"
    
    # Check for license badge
    assert 'License' in content and 'MIT' in content, \
        "MIT License badge not found"


def test_architecture_overview_section():
    """
    Check that an architecture overview section exists.
    
    The overview should describe the microservices architecture and
    mention all three services (User, Order, Inventory).
    This gives readers a high-level understanding of the system.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    # Check for architecture section header
    assert re.search(r'##\s+Architecture', content, re.IGNORECASE), \
        "Architecture Overview section not found"
    
    # Should mention the three services
    arch_section = content.lower()
    assert 'user' in arch_section and 'service' in arch_section, \
        "User Service not mentioned in architecture"
    assert 'order' in arch_section, \
        "Order Service not mentioned"
    assert 'inventory' in arch_section, \
        "Inventory Service not mentioned"


def test_architecture_diagram_included():
    """
    Verify that the architecture diagram is referenced.
    
    Should include markdown image syntax for architecture.png.
    Visual diagrams are crucial for understanding system architecture.
    
    Example: ![Architecture](./architecture.png)
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert '![' in content and 'architecture.png' in content, \
        "Architecture diagram image not included in README"



def test_prerequisites_section():
    """
    Verify prerequisites section lists required tools.
    
    Should mention:
    - Docker (for containerization)
    - Docker Compose (for orchestration)
    - Development tools (optional but helpful)
    
    Clear prerequisites help users set up their environment correctly.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+Prerequisites', content, re.IGNORECASE), \
        "Prerequisites section not found"
    
    prereq_section = content.lower()
    assert 'docker' in prereq_section, "Docker not listed in prerequisites"
    assert 'compose' in prereq_section, "Docker Compose not mentioned"


def test_quick_start_section():
    """
    Check for Quick Start section with setup instructions.
    
    Should include:
    - Clone command
    - docker-compose up command
    - Health check verification steps
    
    Quick Start lets users try the system immediately without
    reading the entire documentation.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+Quick\s+Start', content, re.IGNORECASE), \
        "Quick Start section not found"
    
    # Should include docker-compose commands
    assert 'docker-compose up' in content or 'docker compose up' in content, \
        "docker-compose up command not found in Quick Start"
    
    # Should include health check instructions
    assert 'health' in content.lower() and 'curl' in content.lower(), \
        "Health check verification not included"


def test_per_service_setup_instructions():
    """
    Verify that setup instructions exist for each service.
    
    Each service (User, Order, Inventory) should have:
    - Local development setup instructions
    - Dependency installation commands
    - How to run the service locally
    - How to run tests
    
    This enables developers to work on individual services.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    # Check for service-specific sections
    assert re.search(r'User\s+Service', content, re.IGNORECASE), \
        "User Service section not found"
    assert re.search(r'Order\s+Service', content, re.IGNORECASE), \
        "Order Service section not found"
    assert re.search(r'Inventory\s+Service', content, re.IGNORECASE), \
        "Inventory Service section not found"
    
    # Check for setup instructions for each language
    content_lower = content.lower()
    assert 'pip install' in content_lower or 'requirements.txt' in content_lower, \
        "Python dependency installation not documented"
    assert 'npm install' in content_lower, \
        "Node.js dependency installation not documented"
    assert 'go mod' in content_lower or 'go build' in content_lower, \
        "Go build instructions not documented"


def test_environment_variables_documented():
    """
    Check that environment variables are documented for services.
    
    Should list important variables like:
    - PORT (for all services)
    - USER_SERVICE_URL (for Order Service)
    - INVENTORY_SERVICE_URL (for Order Service)
    
    Environment variable documentation is critical for deployment.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert 'Environment' in content and 'Variable' in content, \
        "Environment variables section not found"
    
    assert 'PORT' in content, "PORT environment variable not documented"


def test_api_documentation_section():
    """
    Verify comprehensive API documentation exists.
    
    Should document:
    - Base URLs for each service
    - HTTP methods (GET, POST, etc.)
    - Endpoint paths (/api/v1/users, /api/v1/orders, etc.)
    - Request/response examples
    
    API documentation is essential for service integration.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+API', content, re.IGNORECASE), \
        "API Documentation section not found"
    
    # Check for endpoint documentation
    assert '/health' in content, "Health endpoint not documented"
    assert '/api/v1/users' in content, "User API endpoints not documented"
    assert '/api/v1/orders' in content, "Order API endpoints not documented"
    assert '/api/v1/inventory' in content, "Inventory API endpoints not documented"


def test_curl_examples_present():
    """
    Check that curl command examples are provided.
    
    Should include at least 2 curl examples demonstrating:
    - How to create a user
    - How to create an order
    - How to query inventory
    
    Practical examples help developers understand API usage immediately.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    curl_count = content.lower().count('curl')
    assert curl_count >= 2, \
        f"Not enough curl examples found. Expected at least 2, found {curl_count}"
    
    # Check for localhost usage (correct for local development)
    assert 'localhost:5000' in content or 'localhost:3000' in content, \
        "Curl examples don't use correct localhost URLs"


def test_docker_compose_usage_section():
    """
    Verify Docker Compose usage documentation.
    
    Should explain how to:
    - Build services: docker-compose build
    - Start services: docker-compose up
    - View logs: docker-compose logs
    - Stop services: docker-compose down
    
    Docker Compose is the primary way to run the entire system.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+Docker\s+Compose', content, re.IGNORECASE), \
        "Docker Compose Usage section not found"
    
    content_lower = content.lower()
    assert 'docker-compose build' in content_lower or 'docker compose build' in content_lower, \
        "docker-compose build command not documented"
    assert 'docker-compose logs' in content_lower or 'docker compose logs' in content_lower, \
        "docker-compose logs command not documented"
    assert 'docker-compose down' in content_lower or 'docker compose down' in content_lower, \
        "docker-compose down command not documented"


def test_testing_section():
    """
    Check for testing documentation.
    
    Should explain how to run tests for:
    - Python service (pytest)
    - Node.js service (npm test)
    - Go service (go test)
    
    Testing documentation ensures code quality and reliability.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+Test', content, re.IGNORECASE), \
        "Testing section not found"
    
    content_lower = content.lower()
    assert 'pytest' in content_lower, "pytest command not documented"
    assert 'npm test' in content_lower, "npm test command not documented"
    assert 'go test' in content_lower, "go test command not documented"


def test_ci_cd_pipeline_section():
    """
    Verify CI/CD pipeline documentation.
    
    Should describe:
    - The GitHub Actions workflow
    - What jobs run on each push
    - How to view CI/CD status
    
    CI/CD documentation helps contributors understand the
    automated testing and deployment process.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+CI', content, re.IGNORECASE), \
        "CI/CD section not found"
    
    content_lower = content.lower()
    assert 'github actions' in content_lower or 'workflow' in content_lower, \
        "GitHub Actions not mentioned in CI/CD section"


def test_contributing_section():
    """
    Check for contributing guidelines.
    
    Should explain:
    - How to submit issues
    - How to create pull requests
    - Code style guidelines
    - Commit message conventions
    
    Contributing guidelines help maintain code quality and
    project consistency as the team grows.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+Contributing', content, re.IGNORECASE), \
        "Contributing section not found"
    
    content_lower = content.lower()
    assert 'pull request' in content_lower or 'pr' in content_lower, \
        "Pull request guidelines not found"
    assert 'issue' in content_lower, "Issue submission guidelines not found"
    assert 'commit' in content_lower, "Commit guidelines not found"


def test_license_section():
    """
    Verify that license information is included.
    
    Should mention MIT License, which is common for open-source projects.
    License information is legally important for any public repository.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    assert re.search(r'##\s+License', content, re.IGNORECASE), \
        "License section not found"
    
    assert 'MIT' in content, "MIT License not mentioned"




def test_readme_structure_logical():
    """
    Verify that README sections appear in a logical order.
    
    Expected flow:
    1. Title and badges
    2. Architecture overview
    3. Quick start
    4. Detailed setup
    5. API documentation
    6. Contributing
    
    Logical structure makes documentation easier to navigate.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    # Get positions of key sections
    title_pos = content.find('# ')
    arch_pos = content.lower().find('## architecture')
    quick_start_pos = content.lower().find('## quick start')
    
    assert title_pos >= 0, "Main title not found"
    assert arch_pos > title_pos, "Architecture section should come after title"
    
    if quick_start_pos > 0 and arch_pos > 0:
        assert quick_start_pos > arch_pos, \
            "Quick Start should come after Architecture"


def test_no_placeholder_text():
    """
    Ensure there are no placeholder texts left in the README.
    
    Common placeholders to avoid:
    - TODO
    - FIXME
    - [placeholder]
    - TBD
    - XXX
    
    Placeholders indicate incomplete documentation.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    placeholders = ['TODO', 'FIXME', '[placeholder]', 'TBD', 'XXX']
    for placeholder in placeholders:
        assert placeholder not in content, \
            f"Placeholder text '{placeholder}' found in README"


def test_accurate_port_numbers():
    """
    Verify that port numbers in examples match actual service ports.
    
    Expected ports:
    - User Service: 5000
    - Order Service: 3000
    - Inventory Service: 4000
    
    Accurate port numbers prevent confusion and connection errors.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    # If examples mention specific services with ports, verify correctness
    if 'localhost:5000' in content:
        # User service endpoints should be associated with port 5000
        assert '/api/v1/users' in content or 'user' in content.lower(), \
            "Port 5000 should be associated with user service"
    
    if 'localhost:3000' in content:
        # Order service endpoints should be associated with port 3000
        assert '/api/v1/orders' in content or 'order' in content.lower(), \
            "Port 3000 should be associated with order service"



def test_service_interaction_explained():
    """
    Verify that service interactions are documented.
    
    The README should explain that:
    - Order Service calls User Service
    - Order Service calls Inventory Service
    - Services communicate via REST APIs
    
    Understanding service interactions is crucial for debugging
    and system maintenance.
    """
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    content_lower = content.lower()
    
    # Check for mentions of inter-service communication
    assert 'communicate' in content_lower or 'call' in content_lower or 'api' in content_lower, \
        "Service communication not explained"
