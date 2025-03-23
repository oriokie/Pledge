# Testing Documentation

## Overview

The system uses pytest for testing. Tests are organized into the following categories:
- Unit tests
- Integration tests
- API tests
- Service tests
- Task tests

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest backend/tests/api/test_members.py

# Run specific test function
pytest backend/tests/api/test_members.py::test_create_member

# Run with coverage
pytest --cov=app

# Generate coverage report
pytest --cov=app --cov-report=html
```

## Test Structure

```
backend/tests/
├── api/
│   ├── test_members.py
│   ├── test_groups.py
│   ├── test_projects.py
│   ├── test_contributions.py
│   ├── test_sms.py
│   └── test_reports.py
├── core/
│   ├── test_security.py
│   ├── test_deps.py
│   ├── test_db.py
│   └── test_utils.py
├── services/
│   ├── test_storage_service.py
│   ├── test_email_service.py
│   ├── test_sms_service.py
│   ├── test_file_service.py
│   ├── test_notification_service.py
│   └── test_report_service.py
├── tasks/
│   └── test_tasks.py
└── migrations/
    └── test_migrations.py
```

## API Tests

Example API test:

```python
def test_create_member():
    """Test member creation"""
    response = client.post(
        "/api/v1/members",
        json={
            "name": "John Doe",
            "phone_number": "+254712345678",
            "email": "john@example.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
```

## Service Tests

Example service test:

```python
def test_send_sms(sms_service, mock_sms_provider):
    """Test SMS sending"""
    result = sms_service.send_sms(
        phone_number="+254712345678",
        message="Test message"
    )
    assert result["status"] == "success"
    assert "message_id" in result
```

## Task Tests

Example task test:

```python
def test_send_sms_task(mock_celery, mock_sms_service):
    """Test SMS sending task"""
    result = send_sms.delay(
        phone_number="+254712345678",
        message="Test message"
    )
    assert result.get()["status"] == "success"
```

## Test Fixtures

Common test fixtures:

```python
@pytest.fixture
def test_user():
    """Create test user"""
    return User(
        email="test@example.com",
        full_name="Test User",
        role=UserRole.STAFF,
        is_active=True
    )

@pytest.fixture
def mock_sms_provider():
    """Mock SMS provider"""
    with patch("app.services.sms_service.SMSProvider") as mock:
        mock_instance = MagicMock()
        mock_instance.send_sms.return_value = {
            "status": "success",
            "message_id": "123"
        }
        mock.return_value = mock_instance
        yield mock
```

## API Testing with cURL

### Authentication

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Use token
export TOKEN="your-token-here"
curl -X GET http://localhost:8000/api/v1/members \
  -H "Authorization: Bearer $TOKEN"
```

### Members

```bash
# Create member
curl -X POST http://localhost:8000/api/v1/members \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone_number": "+254712345678",
    "email": "john@example.com"
  }'

# Get member
curl -X GET http://localhost:8000/api/v1/members/1 \
  -H "Authorization: Bearer $TOKEN"

# Update member
curl -X PUT http://localhost:8000/api/v1/members/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe Updated"
  }'

# Delete member
curl -X DELETE http://localhost:8000/api/v1/members/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Contributions

```bash
# Create contribution
curl -X POST http://localhost:8000/api/v1/contributions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": 1,
    "project_id": 1,
    "amount": 1000,
    "payment_method": "MPESA",
    "transaction_id": "QWERTY123"
  }'

# Get contributions
curl -X GET "http://localhost:8000/api/v1/contributions?member_id=1" \
  -H "Authorization: Bearer $TOKEN"
```

### Reports

```bash
# Generate report
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "contributions",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "format": "pdf"
  }'
```

## Postman Collection

Import the [Postman Collection](../postman/pledge_api.json) for a complete set of API requests.

Environment variables:
```json
{
  "base_url": "http://localhost:8000",
  "token": "your-token-here"
}
```

Test scripts:
```javascript
// Test successful response
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response structure
pm.test("Response has required fields", function () {
    const response = pm.response.json();
    pm.expect(response).to.have.property("id");
    pm.expect(response).to.have.property("name");
});

// Save token
if (pm.response.code === 200) {
    pm.environment.set("token", pm.response.json().access_token);
}
```

## Performance Testing

Using [k6](https://k6.io/):

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
    vus: 10,
    duration: "30s",
};

export default function () {
    const res = http.get("http://localhost:8000/api/v1/members");
    check(res, {
        "status is 200": (r) => r.status === 200,
        "response time < 200ms": (r) => r.timings.duration < 200
    });
    sleep(1);
}
```

Run performance test:
```bash
k6 run performance_test.js
``` 