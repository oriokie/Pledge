# Pledge API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@example.com&password=admin123
```

**Response**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Users

### Create User
```http
POST /users/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false
}
```

**Response**
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### List Users
```http
GET /users/
Authorization: Bearer {access_token}
```

**Query Parameters**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)
- `search`: Search term for filtering users

**Response**
```json
{
    "total": 10,
    "items": [
        {
            "id": 1,
            "email": "user@example.com",
            "full_name": "John Doe",
            "is_active": true,
            "is_admin": false,
            "created_at": "2024-03-20T10:00:00",
            "updated_at": "2024-03-20T10:00:00"
        }
    ]
}
```

## Members

### Create Member
```http
POST /members/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "John Doe",
    "phone_number": "1234567890",
    "alias": "JD",
    "is_active": true,
    "email": "john@example.com",
    "address": "123 Main St"
}
```

**Response**
```json
{
    "id": 1,
    "name": "John Doe",
    "phone_number": "1234567890",
    "alias": "JD",
    "unique_code": "MEM001",
    "is_active": true,
    "email": "john@example.com",
    "address": "123 Main St",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### Get Member by Code
```http
GET /members/code/{code}
Authorization: Bearer {access_token}
```

**Response**
```json
{
    "id": 1,
    "name": "John Doe",
    "phone_number": "1234567890",
    "alias": "JD",
    "unique_code": "MEM001",
    "is_active": true,
    "email": "john@example.com",
    "address": "123 Main St",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

## Projects

### Create Project
```http
POST /projects/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "Church Building Fund",
    "description": "Fundraising for new church building",
    "target_amount": 100000.00,
    "start_date": "2024-03-20",
    "end_date": "2024-12-31",
    "status": "active"
}
```

**Response**
```json
{
    "id": 1,
    "name": "Church Building Fund",
    "description": "Fundraising for new church building",
    "target_amount": 100000.00,
    "start_date": "2024-03-20",
    "end_date": "2024-12-31",
    "status": "active",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### Get Project Report
```http
GET /reports/projects/{id}
Authorization: Bearer {access_token}
```

**Response**
```json
{
    "project": {
        "id": 1,
        "name": "Church Building Fund",
        "description": "Fundraising for new church building",
        "target_amount": 100000.00,
        "start_date": "2024-03-20",
        "end_date": "2024-12-31",
        "status": "active"
    },
    "summary": {
        "total_contributed": 50000.00,
        "total_pledged": 30000.00,
        "remaining_amount": 20000.00,
        "progress_percentage": 50.0
    },
    "contributions": [
        {
            "id": 1,
            "member_name": "John Doe",
            "amount": 1000.00,
            "type": "contribution",
            "date": "2024-03-20T10:00:00"
        }
    ]
}
```

## Contributions

### Create Contribution
```http
POST /contributions/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "member_id": 1,
    "project_id": 1,
    "amount": 1000.00,
    "type": "contribution",
    "payment_method": "cash",
    "reference_number": "REF001"
}
```

**Response**
```json
{
    "id": 1,
    "member_id": 1,
    "project_id": 1,
    "amount": 1000.00,
    "type": "contribution",
    "payment_method": "cash",
    "reference_number": "REF001",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### List Contributions
```http
GET /contributions/
Authorization: Bearer {access_token}
```

**Query Parameters**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)
- `member_id`: Filter by member ID
- `project_id`: Filter by project ID
- `type`: Filter by contribution type (contribution/pledge)
- `start_date`: Filter by start date
- `end_date`: Filter by end date

**Response**
```json
{
    "total": 10,
    "items": [
        {
            "id": 1,
            "member_id": 1,
            "project_id": 1,
            "amount": 1000.00,
            "type": "contribution",
            "payment_method": "cash",
            "reference_number": "REF001",
            "created_at": "2024-03-20T10:00:00",
            "updated_at": "2024-03-20T10:00:00"
        }
    ]
}
```

## Groups

### Create Group
```http
POST /groups/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "Youth Group",
    "description": "Church youth group",
    "leader_id": 1
}
```

**Response**
```json
{
    "id": 1,
    "name": "Youth Group",
    "description": "Church youth group",
    "leader_id": 1,
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### Add Member to Group
```http
POST /groups/{id}/members/{member_id}
Authorization: Bearer {access_token}
```

**Response**
```json
{
    "id": 1,
    "group_id": 1,
    "member_id": 1,
    "created_at": "2024-03-20T10:00:00"
}
```

## Fundraising

### Create Fundraising Goal
```http
POST /fundraising/goals/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "New Church Building",
    "description": "Fundraising for new church building",
    "target_amount": 1000000.00,
    "start_date": "2024-03-20",
    "end_date": "2024-12-31",
    "status": "active"
}
```

**Response**
```json
{
    "id": 1,
    "name": "New Church Building",
    "description": "Fundraising for new church building",
    "target_amount": 1000000.00,
    "start_date": "2024-03-20",
    "end_date": "2024-12-31",
    "status": "active",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

### Get Fundraising Progress
```http
GET /fundraising/goals/{id}/progress
Authorization: Bearer {access_token}
```

**Response**
```json
{
    "goal": {
        "id": 1,
        "name": "New Church Building",
        "target_amount": 1000000.00
    },
    "progress": {
        "current_amount": 500000.00,
        "target_amount": 1000000.00,
        "progress_percentage": 50.0,
        "remaining_amount": 500000.00
    },
    "contributions": [
        {
            "id": 1,
            "member_name": "John Doe",
            "amount": 10000.00,
            "date": "2024-03-20T10:00:00"
        }
    ]
}
```

## Error Responses

### Authentication Error
```json
{
    "detail": "Could not validate credentials",
    "status_code": 401
}
```

### Validation Error
```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "Invalid email format",
            "type": "value_error"
        }
    ]
}
```

### Not Found Error
```json
{
    "detail": "Resource not found",
    "status_code": 404
}
```

### Permission Error
```json
{
    "detail": "Not enough permissions",
    "status_code": 403
}
```

## Rate Limiting
- 100 requests per minute per IP address
- 1000 requests per hour per user

## Pagination
All list endpoints support pagination with the following parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

## Filtering
Most list endpoints support filtering with the following parameters:
- `search`: Search term for text fields
- `start_date`: Filter by start date
- `end_date`: Filter by end date
- `status`: Filter by status
- `type`: Filter by type

## Sorting
All list endpoints support sorting with the following parameter:
- `sort_by`: Field to sort by (e.g., "created_at", "name")
- `order`: Sort order ("asc" or "desc", default: "asc") 