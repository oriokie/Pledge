# API Documentation

## Authentication

All API endpoints (except `/auth/login` and `/auth/register`) require authentication using JWT tokens.

### Getting a Token

```bash
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### Using the Token

Include the token in the Authorization header:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## API Endpoints

### Members

#### List Members
```bash
GET /api/v1/members
```

Query Parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `search`: Search term for name/phone/code

#### Create Member
```bash
POST /api/v1/members
Content-Type: application/json

{
    "name": "John Doe",
    "phone_number": "+254712345678",
    "email": "john@example.com"
}
```

#### Get Member
```bash
GET /api/v1/members/{member_id}
```

#### Update Member
```bash
PUT /api/v1/members/{member_id}
Content-Type: application/json

{
    "name": "John Doe Updated",
    "phone_number": "+254712345678",
    "email": "john@example.com"
}
```

#### Delete Member
```bash
DELETE /api/v1/members/{member_id}
```

### Groups

#### List Groups
```bash
GET /api/v1/groups
```

#### Create Group
```bash
POST /api/v1/groups
Content-Type: application/json

{
    "name": "Test Group",
    "description": "Test Description",
    "members": [1, 2, 3]
}
```

#### Get Group
```bash
GET /api/v1/groups/{group_id}
```

#### Update Group
```bash
PUT /api/v1/groups/{group_id}
Content-Type: application/json

{
    "name": "Updated Group",
    "description": "Updated Description",
    "members": [1, 2, 3, 4]
}
```

#### Delete Group
```bash
DELETE /api/v1/groups/{group_id}
```

### Projects

#### List Projects
```bash
GET /api/v1/projects
```

#### Create Project
```bash
POST /api/v1/projects
Content-Type: application/json

{
    "name": "Test Project",
    "description": "Test Description",
    "target_amount": 100000,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
}
```

#### Get Project
```bash
GET /api/v1/projects/{project_id}
```

#### Update Project
```bash
PUT /api/v1/projects/{project_id}
Content-Type: application/json

{
    "name": "Updated Project",
    "description": "Updated Description",
    "target_amount": 150000
}
```

#### Delete Project
```bash
DELETE /api/v1/projects/{project_id}
```

### Contributions

#### List Contributions
```bash
GET /api/v1/contributions
```

Query Parameters:
- `member_id`: Filter by member
- `project_id`: Filter by project
- `start_date`: Filter by date range start
- `end_date`: Filter by date range end

#### Create Contribution
```bash
POST /api/v1/contributions
Content-Type: application/json

{
    "member_id": 1,
    "project_id": 1,
    "amount": 1000,
    "payment_method": "MPESA",
    "transaction_id": "QWERTY123"
}
```

#### Get Contribution
```bash
GET /api/v1/contributions/{contribution_id}
```

#### Update Contribution
```bash
PUT /api/v1/contributions/{contribution_id}
Content-Type: application/json

{
    "amount": 1500,
    "payment_method": "MPESA",
    "transaction_id": "QWERTY123"
}
```

#### Delete Contribution
```bash
DELETE /api/v1/contributions/{contribution_id}
```

### Reports

#### Generate Report
```bash
POST /api/v1/reports
Content-Type: application/json

{
    "report_type": "contributions",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "format": "pdf"
}
```

### SMS

#### Send SMS
```bash
POST /api/v1/sms
Content-Type: application/json

{
    "phone_number": "+254712345678",
    "message": "Test message"
}
```

#### Send Bulk SMS
```bash
POST /api/v1/sms/bulk
Content-Type: application/json

{
    "group_id": 1,
    "message": "Test message"
}
```

## Error Handling

The API uses standard HTTP status codes and returns error responses in the following format:

```json
{
    "detail": {
        "message": "Error message",
        "code": "ERROR_CODE",
        "params": {}
    }
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

## Rate Limiting

API endpoints are rate-limited to prevent abuse. The current limits are:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in the response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1624987543
``` 