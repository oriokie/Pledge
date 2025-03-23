# Pledge System Documentation

## Overview
The Pledge System is a comprehensive platform for managing member contributions, projects, and groups. This documentation provides detailed information about the system's architecture, components, and usage.

## Table of Contents

1. [API Documentation](api/README.md)
   - REST API endpoints
   - Authentication
   - Request/Response formats
   - Error handling

2. [Core Components](core/README.md)
   - Security
   - Database
   - Dependencies
   - Utilities

3. [Services](services/README.md)
   - Storage Service
   - Email Service
   - SMS Service
   - File Service
   - Notification Service
   - Report Service

4. [Testing](testing/README.md)
   - Unit Tests
   - Integration Tests
   - API Tests
   - Performance Tests

5. [Examples](examples/README.md)
   - cURL Examples
   - API Usage Examples
   - Code Snippets

6. [Postman Collection](postman/README.md)
   - Environment Setup
   - Request Collections
   - Test Scripts

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture

The system follows a modular architecture with the following main components:

- FastAPI backend
- SQLAlchemy ORM
- Celery for background tasks
- Redis for caching
- PostgreSQL database
- S3/Local storage for files

## Security

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- HTTPS encryption
- Input validation
- Rate limiting

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 