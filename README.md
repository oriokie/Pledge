# Church Pledging Application

A comprehensive church pledging and contribution management system built with FastAPI and Next.js.

## Features

- Phone number-based authentication
- Member management with alias names
- Group contributions tracking
- Project/fundraising campaign management
- SMS notifications via Advanta SMS
- Role-based access control (Admin/Staff)
- Advanced search functionality
- Excel report generation
- Real-time dashboard

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

4. Set up the database:
```bash
# Start PostgreSQL service
# Create database named 'church_pledging'
```

5. Start Redis server:
```bash
# Start Redis service
```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the FastAPI server:
```bash
uvicorn backend.app.main:app --reload
```

8. Start Celery worker (in a separate terminal):
```bash
celery -A backend.app.core.celery_app worker --loglevel=info
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Required environment variables (see `.env.example`):
- Database configuration
- Redis configuration
- JWT settings
- SMS API credentials

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── tests/
└── alembic/
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`

### Users (Admin/Staff)
- `GET /api/v1/users`
- `POST /api/v1/users`
- `PUT /api/v1/users/{user_id}`
- `DELETE /api/v1/users/{user_id}`

### Members
- `GET /api/v1/members`
- `POST /api/v1/members`
- `PUT /api/v1/members/{member_id}`
- `DELETE /api/v1/members/{member_id}`

### Groups
- `GET /api/v1/groups`
- `POST /api/v1/groups`
- `PUT /api/v1/groups/{group_id}`
- `DELETE /api/v1/groups/{group_id}`

### Projects
- `GET /api/v1/projects`
- `POST /api/v1/projects`
- `PUT /api/v1/projects/{project_id}`
- `DELETE /api/v1/projects/{project_id}`

### Contributions
- `GET /api/v1/contributions`
- `POST /api/v1/contributions`
- `PUT /api/v1/contributions/{contribution_id}`
- `DELETE /api/v1/contributions/{contribution_id}`

### Reports
- `GET /api/v1/reports/projects/{project_id}`
- `GET /api/v1/reports/groups/{group_id}`
- `GET /api/v1/reports/download`

### SMS
- `POST /api/v1/sms/send`
- `POST /api/v1/sms/send-bulk`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 