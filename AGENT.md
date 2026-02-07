# AGENT.md — Project Instructions

## Project Overview
**Project Name:** Community Learning Platform for Tech Beginners
**Type:** Side Project - Educational Platform
**Current Phase:** Backend API Development (Phase 1)
**Tech Stack:** FastAPI (Python) → Frontend (Phase 2, TBD)

### Mission Statement
Build a welcoming, accessible platform that helps beginners break into tech through community-driven learning, mentorship, and practical resources.

---

## Project Goals

### Phase 1: Backend API (Current Focus)
- Build a robust REST API service using FastAPI
- Implement user authentication and authorization
- Create learning resource management system
- Enable community features (discussions, mentorship matching)
- Write comprehensive tests and documentation
- Set up CI/CD pipeline for automated testing and deployment

### Phase 2: Frontend (Future)
- Create intuitive, accessible user interface
- Implement responsive design for all devices
- Build interactive learning experience
- Integrate with backend API

---

## Architecture & Design Principles

### Backend Architecture
```
project-root/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # Dependency injection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── auth.py     # Authentication endpoints
│   │   │   │   ├── users.py    # User management
│   │   │   │   ├── courses.py  # Learning resources
│   │   │   │   ├── community.py # Community features
│   │   │   │   └── mentorship.py
│   │   │   └── endpoints.py    # Route aggregator
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # Auth & security utilities
│   │   ├── config.py           # App configuration
│   │   └── exceptions.py       # Custom exceptions
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # Database session
│   │   ├── models.py           # SQLAlchemy models
│   │   └── migrations/         # Alembic migrations
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Pydantic schemas
│   │   ├── course.py
│   │   └── community.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py     # Business logic
│   │   ├── course_service.py
│   │   └── auth_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repo.py        # Database operations
│   │   └── course_repo.py
│   └── utils/
│       ├── __init__.py
│       ├── email.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── seed_db.py
│   └── create_admin.py
|-- frontend/
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml              # Python project config
├── pytest.ini
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### Design Principles
1. **Separation of Concerns**: Clear boundaries between routes, services, repositories
2. **Dependency Injection**: Use FastAPI's dependency system for testability
3. **Repository Pattern**: Abstract database operations from business logic
4. **Service Layer**: Encapsulate business logic separate from API routes
5. **Schema Validation**: Use Pydantic models for request/response validation
6. **Error Handling**: Consistent error responses across all endpoints
7. **Security First**: Authentication, authorization, input validation on all endpoints
8. **API Versioning**: Support multiple API versions (start with v1)

---

## Coding Standards

### Python Style Guide
- **Style**: Follow PEP 8 guidelines strictly
- **Linting**: Use `ruff` for fast linting and formatting
- **Type Hints**: Use type hints for all function signatures
- **Docstrings**: Google-style docstrings for all classes and functions
- **Max Line Length**: 88 characters (Black default)
- **Import Order**: Use `isort` for consistent import ordering

### Code Quality Tools
```toml
# pyproject.toml configuration
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.black]
line-length = 88

[tool.isort]
profile = "black"
```

### FastAPI Best Practices
- **Async/Await**: Use async functions for I/O operations
- **Dependency Injection**: Leverage FastAPI dependencies for database sessions, auth
- **Response Models**: Always define Pydantic response models
- **Status Codes**: Use appropriate HTTP status codes (201 for creation, 204 for deletion)
- **Error Responses**: Use HTTPException with consistent error structure
- **Documentation**: Write clear OpenAPI descriptions and examples
- **Background Tasks**: Use BackgroundTasks for email sending, notifications

### Database Standards
- **ORM**: Use SQLAlchemy 2.0 with async support
- **Migrations**: Alembic for all schema changes (never manual SQL)
- **Naming**: snake_case for tables and columns
- **Indexes**: Add indexes for frequently queried columns
- **Relationships**: Define explicit relationships with lazy loading strategy
- **Connection Pooling**: Configure appropriate pool size for production

### Authentication & Security
- **Password Hashing**: Use bcrypt via passlib
- **JWT Tokens**: Access tokens (15min) + Refresh tokens (7 days)
- **OAuth2**: Implement OAuth2 with Password flow
- **CORS**: Configure CORS for frontend domain only
- **Rate Limiting**: Implement rate limiting on auth endpoints
- **Input Validation**: Sanitize all user inputs
- **SQL Injection**: Use ORM parameterized queries (no raw SQL)

---

## Testing Standards

### Testing Philosophy
- **Test Coverage**: Minimum 80% code coverage
- **Test Pyramid**: More unit tests, fewer integration tests, minimal E2E
- **Fast Tests**: Unit tests should run in milliseconds
- **Isolated Tests**: Each test should be independent and idempotent
- **Clear Naming**: Test names should describe what they test and expected behavior

### Test Structure
```python
# test_user_service.py
import pytest
from app.services.user_service import UserService

class TestUserService:
    """Test suite for UserService class."""
    
    def test_create_user_with_valid_data_succeeds(self, db_session):
        """Should create user when provided valid data."""
        # Arrange
        user_data = {"email": "test@example.com", "password": "SecurePass123"}
        service = UserService(db_session)
        
        # Act
        result = service.create_user(user_data)
        
        # Assert
        assert result.email == "test@example.com"
        assert result.id is not None
```

### Testing Tools
- **Framework**: pytest with pytest-asyncio
- **Fixtures**: Use conftest.py for shared fixtures
- **Mocking**: Use pytest-mock for external dependencies
- **Database**: Use SQLite in-memory for tests
- **Coverage**: pytest-cov for coverage reports
- **Factories**: Use factory_boy for test data generation

### Test Categories
1. **Unit Tests** (`tests/unit/`): Test individual functions/methods
2. **Integration Tests** (`tests/integration/`): Test API endpoints with database
3. **E2E Tests** (`tests/e2e/`): Test complete user workflows

### Required Tests for Each Endpoint
- Happy path with valid data
- Invalid input validation
- Authentication/authorization checks
- Error handling (404, 409, etc.)
- Edge cases (empty lists, null values)

---

## API Documentation Standards

### OpenAPI/Swagger
- **Descriptions**: Write clear, user-friendly endpoint descriptions
- **Examples**: Provide request/response examples for all endpoints
- **Tags**: Organize endpoints with logical tags (Auth, Users, Courses)
- **Error Codes**: Document all possible error responses
- **Schemas**: Include detailed schema descriptions

### Example Endpoint Documentation
```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user account",
    description="Register a new user with email and password. Email must be unique.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already registered"},
    },
    tags=["Users"]
)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Create a new user account.
    
    Args:
        user_data: User registration data including email and password
        db: Database session
        
    Returns:
        UserResponse: Created user data
        
    Raises:
        HTTPException: 409 if email already exists
        HTTPException: 400 if validation fails
    """
    pass
```

### README Documentation
- **Quick Start**: Getting started in 5 minutes
- **Installation**: Step-by-step setup instructions
- **Environment Variables**: All required and optional env vars
- **API Endpoints**: High-level overview with examples
- **Development**: How to run tests, lint, format code
- **Deployment**: Production deployment guide

---

## Version Control & Git Workflow

### Branch Strategy
- **main**: Production-ready code only
- **develop**: Integration branch for features
- **feature/**: Feature branches (e.g., `feature/user-authentication`)
- **bugfix/**: Bug fix branches (e.g., `bugfix/login-error`)
- **hotfix/**: Critical production fixes

### Commit Message Format
Follow Conventional Commits specification:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): implement JWT token refresh endpoint

Add endpoint to refresh access tokens using refresh token.
Tokens expire after 15 minutes and can be refreshed up to 7 days.

Closes #42
```

### Semantic Versioning
Follow SemVer (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Current version: `0.1.0` (pre-release development)

---

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt -r requirements-dev.txt
      - name: Lint with ruff
        run: ruff check .
      - name: Format check with black
        run: black --check .
      - name: Type check with mypy
        run: mypy app/
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## Development Workflow Commands

### Backend Development (Current Phase)

#### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Copy environment variables
cp .env.example .env
# Edit .env with your local settings

# Initialize database
alembic upgrade head

# Seed database (optional)
python scripts/seed_db.py
```

#### Running the Application
```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server (with workers)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With Docker
docker-compose up -d

# View logs
docker-compose logs -f api
```

#### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_user_service.py

# Run tests matching pattern
pytest -k "test_create_user"

# Run with verbose output
pytest -v

# Run only unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Watch mode (requires pytest-watch)
ptw
```

#### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Sort imports
isort .

# Type checking
mypy app/

# Run all quality checks
black . && isort . && ruff check . && mypy app/
```

#### Database Management
```bash
# Create new migration
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Seed database
python scripts/seed_db.py

# Create admin user
python scripts/create_admin.py
```

#### API Documentation
```bash
# Access Swagger UI
# Navigate to: http://localhost:8000/docs

# Access ReDoc
# Navigate to: http://localhost:8000/redoc

# Export OpenAPI schema
curl http://localhost:8000/openapi.json > openapi.json
```

### Frontend Development (Phase 2 - Future)
*To be added when frontend development begins*

```bash
# Placeholder commands for future frontend work
# npm install
# npm run dev
# npm run build
# npm run test
```

---

## Environment Variables

### Required Environment Variables
```bash
# .env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/learning_platform
DATABASE_TEST_URL=sqlite:///./test.db

# Security
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Email (for user verification, password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@yourplatform.com

# Application
APP_NAME=Community Learning Platform
ENVIRONMENT=development  # development, staging, production
DEBUG=True
LOG_LEVEL=INFO

# Redis (for caching and rate limiting)
REDIS_URL=redis://localhost:6379/0

# File Storage (for user uploads)
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=10
```

---

## Key Features to Implement

### Phase 1: MVP Backend (Priority Order)

#### 1. User Authentication & Authorization ✓ Priority: HIGH
- [ ] User registration with email verification
- [ ] Login with JWT tokens (access + refresh)
- [ ] Password reset flow
- [ ] OAuth2 integration (Google, GitHub)
- [ ] Role-based access control (Admin, Mentor, Learner)
- [ ] User profile management

#### 2. Learning Resources ✓ Priority: HIGH
- [ ] Course/tutorial CRUD operations
- [ ] Resource categorization (tags, difficulty levels)
- [ ] Search and filtering
- [ ] Resource recommendations
- [ ] Progress tracking
- [ ] Bookmarking system

#### 3. Community Features ✓ Priority: MEDIUM
- [ ] Discussion forums
- [ ] Question & Answer system
- [ ] User comments and replies
- [ ] Upvoting/downvoting
- [ ] Moderation tools
- [ ] Reporting system

#### 4. Mentorship System ✓ Priority: MEDIUM
- [ ] Mentor profiles and availability
- [ ] Mentorship request system
- [ ] Session scheduling
- [ ] Feedback and ratings
- [ ] Mentor-mentee matching algorithm

#### 5. User Progress & Analytics ✓ Priority: LOW
- [ ] Learning path tracking
- [ ] Achievement badges
- [ ] Progress statistics
- [ ] Activity feed
- [ ] Leaderboards (optional)

#### 6. Administrative Features ✓ Priority: MEDIUM
- [ ] User management dashboard
- [ ] Content moderation
- [ ] Analytics and reporting
- [ ] System configuration
- [ ] Bulk operations

---

## Database Schema (Initial)

### Core Tables
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    bio TEXT,
    role VARCHAR(20) DEFAULT 'learner',  -- admin, mentor, learner
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses/Resources table
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT,
    difficulty VARCHAR(20),  -- beginner, intermediate, advanced
    category VARCHAR(100),
    tags TEXT[],
    created_by UUID REFERENCES users(id),
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Progress table
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    progress_percentage INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, course_id)
);
```

---

## API Endpoints (Planned)

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `POST /api/v1/auth/verify-email` - Verify email address
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/reset-password` - Reset password

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users` - List users (admin only)

### Courses
- `POST /api/v1/courses` - Create course (mentor/admin)
- `GET /api/v1/courses` - List courses (with filters)
- `GET /api/v1/courses/{course_id}` - Get course details
- `PUT /api/v1/courses/{course_id}` - Update course
- `DELETE /api/v1/courses/{course_id}` - Delete course
- `POST /api/v1/courses/{course_id}/enroll` - Enroll in course
- `GET /api/v1/courses/{course_id}/progress` - Get user progress

### Community
- `POST /api/v1/discussions` - Create discussion
- `GET /api/v1/discussions` - List discussions
- `GET /api/v1/discussions/{discussion_id}` - Get discussion
- `POST /api/v1/discussions/{discussion_id}/comments` - Add comment
- `POST /api/v1/discussions/{discussion_id}/upvote` - Upvote discussion

---

## Dependencies

### Core Dependencies (requirements.txt)
```txt
fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.3
pydantic-settings==2.1.0
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
aiofiles==23.2.1
python-dotenv==1.0.0
redis==5.0.1
celery==5.3.4
```

### Development Dependencies (requirements-dev.txt)
```txt
pytest==7.4.3
pytest-asyncio==0.23.2
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.26.0
factory-boy==3.3.0
faker==22.0.0
black==23.12.1
ruff==0.1.9
isort==5.13.2
mypy==1.8.0
pre-commit==3.6.0
```

---

## Performance Considerations

### Caching Strategy
- Use Redis for session management
- Cache frequently accessed resources (courses, user profiles)
- Implement cache invalidation on updates
- Use ETags for conditional requests

### Database Optimization
- Add indexes on frequently queried columns
- Use database connection pooling
- Implement pagination for list endpoints
- Use select_related/joinedload for relationships
- Consider read replicas for scaling

### Rate Limiting
- Implement rate limiting on auth endpoints (5 req/min)
- API rate limits: 100 requests per minute per user
- Use Redis for distributed rate limiting

---

## Security Checklist

- [ ] All passwords hashed with bcrypt
- [ ] JWT tokens with short expiration
- [ ] HTTPS only in production
- [ ] CORS configured properly
- [ ] SQL injection protection (use ORM)
- [ ] XSS protection (sanitize inputs)
- [ ] CSRF protection for state-changing operations
- [ ] Rate limiting on sensitive endpoints
- [ ] Input validation on all endpoints
- [ ] Sensitive data not logged
- [ ] Environment variables for secrets
- [ ] Regular dependency updates

---

## Monitoring & Logging

### Logging Strategy
- Use Python's logging module
- Log levels: DEBUG (dev), INFO (prod)
- Structured logging (JSON format)
- Log all errors with stack traces
- Log authentication attempts
- Don't log sensitive data (passwords, tokens)

### Metrics to Track
- Request/response times
- Error rates by endpoint
- Database query performance
- Authentication success/failure rates
- User registration trends

---

## Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files served via CDN
- [ ] HTTPS certificate installed
- [ ] Database backups configured
- [ ] Monitoring and alerts set up
- [ ] Rate limiting enabled
- [ ] CORS configured for production domain
- [ ] Error tracking configured (Sentry)
- [ ] Load testing completed

### Deployment Options
1. **Docker + Docker Compose** (recommended for initial deployment)
2. **Kubernetes** (for scaling)
3. **Heroku/Railway** (for quick deployment)
4. **AWS/GCP/Azure** (for production)

---

## Communication & Collaboration

### Code Review Guidelines
- All code changes require review before merging
- Review for: functionality, tests, code style, security
- Be constructive and respectful in feedback
- Approve only when all comments addressed

### Documentation Standards
- Update README for any new features
- Document all API changes
- Keep this AGENT.md file updated
- Write clear commit messages
- Comment complex logic

---

## Future Enhancements (Backlog)

### Phase 2 Ideas
- Real-time chat between mentors and learners
- Video integration for tutorials
- Interactive code playground
- Certificate generation
- Gamification (points, badges, levels)
- Mobile app (React Native)
- AI-powered learning recommendations
- Integration with GitHub for code reviews
- Job board for tech positions
- Scholarship/grant information

---

## Questions to Ask When Working

### For New Features
1. What problem does this solve for beginners?
2. Is this accessible to users with disabilities?
3. How will this scale with 10k+ users?
4. What are the security implications?
5. How will we test this?
6. Does this align with our mission?

### For Bug Fixes
1. What caused this bug?
2. How can we prevent similar bugs?
3. Are there other places with the same issue?
4. What tests should we add?

---

## Contact & Resources

### Useful Links
- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLAlchemy Documentation: https://docs.sqlalchemy.org
- Pydantic Documentation: https://docs.pydantic.dev
- Pytest Documentation: https://docs.pytest.org

### Getting Help
- Check existing issues first
- Write clear issue descriptions
- Include error messages and logs
- Provide steps to reproduce

---

## Notes for AI Coding Agents

When working on this project, always:
1. ✅ Write tests for new features
2. ✅ Update API documentation
3. ✅ Follow the project structure
4. ✅ Use type hints and docstrings
5. ✅ Handle errors gracefully
6. ✅ Consider security implications
7. ✅ Keep beginner users in mind
8. ✅ Ask clarifying questions when uncertain
9. ✅ Suggest improvements where appropriate
10. ✅ Maintain consistency with existing code

Remember: This platform is for beginners. Keep things simple, well-documented, and welcoming!

---

**Last Updated:** 2025-02-07
**Version:** 0.1.0-alpha
**Maintainer:** [Bheki]