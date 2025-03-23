# Pledge Backend Documentation

## Overview
The Pledge backend is a FastAPI-based REST API that provides functionality for managing church members, contributions, projects, and fundraising activities. The application follows a clean architecture pattern with clear separation of concerns.

## Project Structure
```
backend/
├── app/
│   ├── api/           # API endpoints and route handlers
│   ├── core/          # Core functionality and configurations
│   ├── crud/          # Database CRUD operations
│   ├── db/            # Database models and migrations
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic models for request/response
│   └── services/      # Business logic and external services
├── tests/             # Test files
│   ├── api/          # API endpoint tests
│   ├── crud/         # CRUD operation tests
│   └── conftest.py   # Test configurations and fixtures
└── alembic/          # Database migrations
```

## Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Staff, User)
- Token refresh mechanism
- Password hashing and verification

### Member Management
- Member registration with unique codes
- Member profile management
- Member search and filtering
- Member status tracking

### Project Management
- Project creation and tracking
- Project status management
- Project contribution tracking
- Project reporting

### Contribution Management
- Individual contributions
- Group contributions
- Pledge management
- Contribution history

### Group Management
- Group creation and management
- Member assignment to groups
- Group contribution tracking
- Group reporting

### Fundraising
- Fundraising campaign management
- Fundraising goals and targets
- Progress tracking
- Contribution tracking

### Reporting
- Project reports
- Member reports
- Group reports
- Dashboard analytics
- Export functionality

## API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/login`: User login
- `POST /api/v1/auth/refresh`: Refresh access token
- `POST /api/v1/auth/test-token`: Validate token

### User Management
- `POST /api/v1/users/`: Create new user
- `GET /api/v1/users/`: List all users
- `GET /api/v1/users/me`: Get current user
- `GET /api/v1/users/{id}`: Get user by ID
- `PUT /api/v1/users/{id}`: Update user
- `DELETE /api/v1/users/{id}`: Delete user

### Member Management
- `POST /api/v1/members/`: Create new member
- `GET /api/v1/members/`: List all members
- `GET /api/v1/members/{id}`: Get member by ID
- `GET /api/v1/members/code/{code}`: Get member by code
- `PUT /api/v1/members/{id}`: Update member
- `DELETE /api/v1/members/{id}`: Delete member

### Project Management
- `POST /api/v1/projects/`: Create new project
- `GET /api/v1/projects/`: List all projects
- `GET /api/v1/projects/{id}`: Get project by ID
- `PUT /api/v1/projects/{id}`: Update project
- `DELETE /api/v1/projects/{id}`: Delete project

### Contribution Management
- `POST /api/v1/contributions/`: Create new contribution
- `GET /api/v1/contributions/`: List all contributions
- `GET /api/v1/contributions/{id}`: Get contribution by ID
- `PUT /api/v1/contributions/{id}`: Update contribution
- `DELETE /api/v1/contributions/{id}`: Delete contribution

### Group Management
- `POST /api/v1/groups/`: Create new group
- `GET /api/v1/groups/`: List all groups
- `GET /api/v1/groups/{id}`: Get group by ID
- `PUT /api/v1/groups/{id}`: Update group
- `DELETE /api/v1/groups/{id}`: Delete group
- `POST /api/v1/groups/{id}/members/{member_id}`: Add member to group
- `DELETE /api/v1/groups/{id}/members/{member_id}`: Remove member from group

### Reporting
- `GET /api/v1/reports/projects/{id}`: Get project report
- `GET /api/v1/reports/members/{id}`: Get member report
- `GET /api/v1/reports/groups/{id}`: Get group report
- `GET /api/v1/reports/dashboard`: Get dashboard data

## Testing

### Test Structure
The test suite is organized into two main categories:

1. **API Tests** (`tests/api/`)
   - Endpoint testing
   - Request/response validation
   - Authentication testing
   - Authorization testing

2. **CRUD Tests** (`tests/crud/`)
   - Database operation testing
   - Model validation
   - Business logic testing

### Test Coverage
The test suite covers:
- Authentication and authorization
- User management
- Member management
- Project management
- Contribution management
- Group management
- Reporting functionality

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/api/test_auth.py

# Run with coverage report
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Test Fixtures
The test suite includes fixtures for:
- Database session
- Test client
- Test users (admin, staff, regular)
- Authentication tokens
- Test data (members, projects, contributions, groups)

## Database

### Models
The application uses SQLAlchemy ORM with the following main models:
- User
- Member
- Project
- Contribution
- Group
- Fundraising
- FundraisingGoal
- FundraisingContribution
- FundraisingGoalContribution
- FundraisingGoalProgress
- FundraisingGoalMember
- FundraisingGoalGroup
- FundraisingGoalGroupMember

### Migrations
Database migrations are managed using Alembic:
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Security

### Authentication
- JWT tokens with refresh mechanism
- Password hashing using bcrypt
- Token expiration and refresh
- Role-based access control

### Data Protection
- Input validation using Pydantic
- SQL injection prevention
- XSS protection
- CORS configuration

## Error Handling
The application implements comprehensive error handling:
- HTTP status codes
- Detailed error messages
- Validation errors
- Database errors
- Authentication errors
- Authorization errors

## Logging
The application uses structured logging:
- Request/response logging
- Error logging
- Authentication logging
- Database operation logging

## Configuration
Configuration is managed through environment variables:
- Database connection
- JWT settings
- API settings
- Logging settings
- External service credentials

## Dependencies
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- JWT
- pytest
- python-jose
- passlib
- python-multipart
- uvicorn

## Development Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize database:
```bash
alembic upgrade head
```

5. Run development server:
```bash
uvicorn app.main:app --reload
```

## Deployment

### Requirements
- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)

### Deployment Steps
1. Set up production environment variables
2. Run database migrations
3. Build and run with production server
4. Configure reverse proxy (nginx)
5. Set up SSL certificates
6. Configure monitoring and logging

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 