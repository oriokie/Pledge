# Pledge - Contribution Management System

A FastAPI-based backend for managing contributions and pledges.

## Features

- User authentication with JWT tokens
- Role-based access control (Admin, Staff, Member)
- Contribution management
- Pledge tracking
- Email notifications
- Redis caching
- PostgreSQL database

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pledge.git
cd pledge
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Database Setup

1. Make sure PostgreSQL is running and accessible

2. Initialize the databases:
```bash
cd backend
./init_db.sh
```

This will:
- Create the production database named "pledge"
- Create the test database named "test_pledge"
- Create all necessary tables
- Create the initial admin user in both databases

Default admin credentials:
- Email: admin@pledge.com
- Phone: +254700000000
- Password: admin123

**Important**: Change the admin password in production!

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite:
```bash
cd backend
pytest
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 