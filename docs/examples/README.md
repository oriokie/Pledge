# Examples

## Authentication

### Login and Get Token

```bash
# Login and save token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}' \
  | jq -r '.access_token')

# Use token in subsequent requests
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/members
```

## Member Management

### Create and Update Member

```bash
# Create member
MEMBER_ID=$(curl -s -X POST http://localhost:8000/api/v1/members \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone_number": "+254712345678",
    "email": "john@example.com"
  }' | jq -r '.id')

# Update member
curl -X PUT http://localhost:8000/api/v1/members/$MEMBER_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe Updated"
  }'
```

### Search Members

```bash
# Search by name
curl "http://localhost:8000/api/v1/members?search=John" \
  -H "Authorization: Bearer $TOKEN"

# Search by phone
curl "http://localhost:8000/api/v1/members?search=+254712345678" \
  -H "Authorization: Bearer $TOKEN"

# Search with pagination
curl "http://localhost:8000/api/v1/members?page=1&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## Group Management

### Create Group with Members

```bash
# Create group
GROUP_ID=$(curl -s -X POST http://localhost:8000/api/v1/groups \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Group",
    "description": "Test Description",
    "members": [1, 2, 3]
  }' | jq -r '.id')

# Add members to group
curl -X PUT http://localhost:8000/api/v1/groups/$GROUP_ID/members \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "members": [4, 5, 6]
  }'
```

## Project Management

### Create and Track Project

```bash
# Create project
PROJECT_ID=$(curl -s -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "description": "Test Description",
    "target_amount": 100000,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }' | jq -r '.id')

# Get project progress
curl http://localhost:8000/api/v1/projects/$PROJECT_ID/progress \
  -H "Authorization: Bearer $TOKEN"
```

## Contribution Management

### Record Contributions

```bash
# Record single contribution
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

# Get member contributions
curl "http://localhost:8000/api/v1/contributions?member_id=1" \
  -H "Authorization: Bearer $TOKEN"

# Get project contributions
curl "http://localhost:8000/api/v1/contributions?project_id=1" \
  -H "Authorization: Bearer $TOKEN"
```

## Report Generation

### Generate Reports

```bash
# Generate contribution report
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "contributions",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "format": "pdf"
  }' --output report.pdf

# Generate member report
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "members",
    "group_id": 1,
    "format": "excel"
  }' --output report.xlsx
```

## SMS Service

### Send Messages

```bash
# Send single SMS
curl -X POST http://localhost:8000/api/v1/sms \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+254712345678",
    "message": "Test message"
  }'

# Send bulk SMS to group
curl -X POST http://localhost:8000/api/v1/sms/bulk \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": 1,
    "message": "Test message"
  }'
```

## Python Client Examples

### Using the API with Python Requests

```python
import requests

class PledgeClient:
    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.login(email, password)
    
    def login(self, email, password):
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password}
        )
        token = response.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def create_member(self, name, phone_number, email):
        return self.session.post(
            f"{self.base_url}/api/v1/members",
            json={
                "name": name,
                "phone_number": phone_number,
                "email": email
            }
        ).json()
    
    def create_contribution(self, member_id, project_id, amount):
        return self.session.post(
            f"{self.base_url}/api/v1/contributions",
            json={
                "member_id": member_id,
                "project_id": project_id,
                "amount": amount,
                "payment_method": "MPESA",
                "transaction_id": "QWERTY123"
            }
        ).json()

# Usage example
client = PledgeClient(
    "http://localhost:8000",
    "user@example.com",
    "password123"
)

# Create member
member = client.create_member(
    "John Doe",
    "+254712345678",
    "john@example.com"
)

# Create contribution
contribution = client.create_contribution(
    member["id"],
    1,
    1000
)
```

### Using FastAPI Test Client

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_member():
    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "password123"
        }
    )
    token = response.json()["access_token"]
    
    # Create member
    response = client.post(
        "/api/v1/members",
        headers={"Authorization": f"Bearer {token}"},
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