import pytest
import json
import sys    
from app import app, users


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    users.clear()


@pytest.fixture
def sample_user():
    return {
        "id": "user-1",
        "name": "John Doe",
        "email": "john@example.com"
    }


def test_health_check(client):
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['service'] == 'user-service'


def test_get_users_empty(client):
    response = client.get('/api/v1/users')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['users'] == []


def test_create_user(client, sample_user):
    response = client.post(
        '/api/v1/users',
        data=json.dumps(sample_user),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['id'] == sample_user['id']
    assert data['name'] == sample_user['name']
    assert data['email'] == sample_user['email']


def test_get_users_with_data(client, sample_user):
    client.post(
        '/api/v1/users',
        data=json.dumps(sample_user),
        content_type='application/json'
    )
    
    response = client.get('/api/v1/users')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['users']) == 1
    assert data['users'][0]['id'] == sample_user['id']


def test_get_user_by_id_success(client, sample_user):
    client.post(
        '/api/v1/users',
        data=json.dumps(sample_user),
        content_type='application/json'
    )
    
    response = client.get(f'/api/v1/users/{sample_user["id"]}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['id'] == sample_user['id']
    assert data['name'] == sample_user['name']


def test_get_user_by_id_not_found(client):
    response = client.get('/api/v1/users/nonexistent')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['error'] == 'User not found'


def test_create_multiple_users(client):
    users_data = [
        {"id": "user-1", "name": "Alice", "email": "alice@example.com"},
        {"id": "user-2", "name": "Bob", "email": "bob@example.com"},
        {"id": "user-3", "name": "Charlie", "email": "charlie@example.com"}
    ]
    
    for user in users_data:
        response = client.post(
            '/api/v1/users',
            data=json.dumps(user),
            content_type='application/json'
        )
        assert response.status_code == 201
    
    response = client.get('/api/v1/users')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['users']) == 3


def test_create_user_overwrites_existing(client):
    user_v1 = {"id": "user-1", "name": "John", "email": "john@example.com"}
    user_v2 = {"id": "user-1", "name": "John Updated", "email": "john.new@example.com"}
    
    client.post(
        '/api/v1/users',
        data=json.dumps(user_v1),
        content_type='application/json'
    )
    
    response = client.post(
        '/api/v1/users',
        data=json.dumps(user_v2),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    
    response = client.get('/api/v1/users/user-1')
    data = json.loads(response.data)
    
    assert data['name'] == 'John Updated'
    assert data['email'] == 'john.new@example.com'


def test_create_user_with_additional_fields(client):
    user = {
        "id": "user-1",
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "role": "admin"
    }
    
    response = client.post(
        '/api/v1/users',
        data=json.dumps(user),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['age'] == 30
    assert data['role'] == 'admin'


def test_health_check_content_type(client):
    response = client.get('/health')
    
    assert response.content_type == 'application/json'


def test_get_users_content_type(client):
    response = client.get('/api/v1/users')
    
    assert response.content_type == 'application/json'
