# SkillPath Recommendation API

## Overview
A production-grade FastAPI backend for a skill path recommendation system with JWT authentication, CRUD operations, personalized recommendations, caching, and comprehensive testing.

## Features
- **Recommendation Engine**: Personalized skill path recommendations based on user profile
- **JWT Authentication**: Secure token-based authentication with role-based access control
- **CRUD Operations**: Full Create, Read, Update, Delete for catalogue items
- **Advanced Filtering**: Filter by category, location, goal, skill level, price range
- **Search**: Full-text search across items
- **Pagination**: Efficient pagination with metadata
- **Caching**: In-memory caching with TTL for performance
- **Rate Limiting**: 100 requests/minute per IP
- **Metrics**: Request tracking and performance monitoring
- **API Versioning**: Versioned endpoints under `/api/v1/`
- **Background Tasks**: Email sending, analytics, history logging
- **Security Headers**: Comprehensive security headers
- **Request Logging**: Detailed request/response logging

## Tech Stack
- **FastAPI**: Modern, fast web framework with automatic OpenAPI docs
- **SQLAlchemy**: ORM for database operations with type safety
- **Alembic**: Database migration management
- **Pydantic**: Data validation and serialization
- **JWT**: Stateless authentication
- **Python 3.11+**: Runtime environment
- **SQLite**: Lightweight database (can be upgraded to PostgreSQL)
- **pytest**: Testing framework
- **uvicorn**: ASGI server

## Architecture

### Layered Architecture
```
app/
├── api/v1/              # API endpoints (versioned)
├── services/            # Business logic layer
├── repositories/        # Data access layer
├── models/              # SQLAlchemy ORM models
├── schemas/             # Pydantic validation schemas
├── core/                # Core utilities (config, security, JWT)
├── middleware/          # Custom middleware
├── cache/               # Caching layer
├── metrics/             # Metrics collection
└── background/          # Background tasks
```

### Folder Structure
```
potens-internship-backend-Q2/
├── app/
│   ├── api/             # API endpoints
│   │   └── v1/         # Versioned API
│   ├── background/      # Background tasks
│   ├── cache/           # Caching implementation
│   ├── core/            # Core utilities
│   ├── db/              # Database configuration
│   ├── metrics/         # Metrics collection
│   ├── middleware/      # Custom middleware
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── utils/           # Utilities
├── alembic/             # Database migrations
├── tests/               # Test suite
├── scripts/             # Utility scripts
├── docs/                # Documentation
├── data/                # Database files (gitignored)
├── logs/                # Log files (gitignored)
├── .github/workflows/   # CI/CD pipeline
├── README.md
├── requirements.txt
├── alembic.ini
├── .env.example
└── .gitignore
```

### Database Design
**Users Table**
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- full_name
- is_active
- is_admin
- created_at
- updated_at

**Items Table**
- id (Primary Key)
- name
- category
- price
- skill_level
- goal
- location
- pace
- description
- created_at
- updated_at

**Indexes**
- Single-column: category, goal, location, skill_level, price, created_at
- Composite: (category, goal), (location, skill_level), (price, category)

### Recommendation Logic
The recommendation engine uses a weighted scoring system based on user profile attributes:

1. **Goal Match** (+4 points): Item goal must match user goal
2. **Skill Level Match** (+3 points): Exact skill level match
3. **Beginner-Friendly** (+2 points): Beginner users can access beginner/intermediate items
4. **Budget Fit** (+2 points): User budget >= item price
5. **Near-Budget Fit** (+1 point): User budget >= 80% of item price
6. **Location Fit** (+2 points): Location matches or item is remote
7. **Pace Fit** (+1 point): Preferred pace matches item pace

**Minimum Score**: 8 points required for recommendation
**Tie Breaker**: Higher score wins, then by creation date (newest first)
**Output**: Top 3 ranked recommendations with human-readable explanations

### Design Decisions
- **FastAPI**: Modern, fast web framework with automatic OpenAPI docs
- **SQLAlchemy**: ORM for database operations with type safety
- **Alembic**: Database migration management
- **Pydantic**: Data validation and serialization
- **JWT**: Stateless authentication
- **In-memory Cache**: Simple caching with TTL (can be upgraded to Redis)
- **SQLite**: Lightweight database (can be upgraded to PostgreSQL)

## Setup Instructions

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
# Clone repository
git clone https://github.com/kamlesh9876/potens-internship-backend-Q2.git
cd potens-internship-backend-Q2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Required variables:
```env
DATABASE_URL=sqlite:///data/app.db
APP_NAME=SkillPath Recommendation API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here
ADMIN_TOKEN=your-admin-token-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

## Database Setup

### Run Migrations
```bash
# Initialize Alembic (first time only)
alembic init alembic

# Run migrations
alembic upgrade head
```

### Seed Database
```bash
# Run seed script (if available)
python scripts/seed_database.py
```

## Run Instructions

### Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## API Documentation

### Swagger UI
Open http://localhost:8000/docs in your browser

### ReDoc
Open http://localhost:8000/redoc in your browser

### Key Endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/recommend` - Get personalized recommendations
- `GET /api/v1/items` - List items (admin only)
- `POST /api/v1/items` - Create item (admin only)
- `GET /api/v1/items/{id}` - Get item by ID (admin only)
- `PUT /api/v1/items/{id}` - Update item (admin only)
- `DELETE /api/v1/items/{id}` - Delete item (admin only)
- `GET /api/v1/explain/{item_id}` - Get explanation for item
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Application metrics

## Example Requests

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "user@example.com",
    "password": "SecurePass123",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Get Recommendations
```bash
curl -X POST http://localhost:8000/api/v1/recommend \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "age": 25,
    "budget": 200,
    "experience_level": "Beginner",
    "goal": "Career Change",
    "location": "Online",
    "preferred_pace": "Self-paced"
  }'
```

### Create Item (Admin)
```bash
curl -X POST http://localhost:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{
    "name": "Python Bootcamp",
    "category": "Programming",
    "price": 99.99,
    "skill_level": "Beginner",
    "goal": "Career Change",
    "location": "Online",
    "pace": "Self-paced",
    "description": "Learn Python from scratch"
  }'
```

### List Items with Filters
```bash
curl -X GET "http://localhost:8000/api/v1/items?category=Programming&price_min=50&price_max=150&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Get Item Explanation
```bash
curl -X GET http://localhost:8000/api/v1/explain/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Current Coverage
- **116 tests passing**
- **69% code coverage**
- Tests for authentication, CRUD, services, repositories, cache, and security

## Assumptions
- SQLite database for development (PostgreSQL recommended for production)
- In-memory cache (Redis recommended for production scale)
- Single server deployment (can be scaled horizontally)
- Email service is mocked (requires SMTP configuration for production)

## Limitations
- In-memory cache is not distributed
- No real-time notifications
- Background tasks are synchronous in test environment
- Rate limiting is in-memory (not distributed)

## Future Improvements
- Migrate to PostgreSQL for production
- Implement Redis for distributed caching
- Add WebSocket support for real-time updates
- Implement webhook subscriptions
- Add comprehensive API contract testing
- Implement load testing with Locust
- Add performance benchmarks
- Implement refresh token rotation
- Add OAuth2 social login support

## AI Use Log

### Tool Used: Cascade (AI Coding Assistant)
- **Approximate Usage**: 50+ hours across multiple sessions
- **Purpose**: 
  - Implementing core CRUD operations
  - Building recommendation engine
  - Adding authentication and authorization
  - Implementing middleware (logging, rate limiting, security)
  - Creating comprehensive test suite
  - Writing documentation
  - Debugging and fixing issues
- **Honest Assessment**: Cascade was used extensively for code generation, debugging, and architectural decisions. All code was reviewed and understood before committing. The AI accelerated development significantly while maintaining code quality.

## Phase Completion

### Phase 1: Core Requirements ✅
- Recommendation API with structured profile
- 15+ catalogue items in database
- Full CRUD operations
- Admin protection with JWT
- Explain endpoint

### Phase 2: API Quality ✅
- RESTful endpoints
- Proper HTTP methods and status codes
- Consistent response format
- Clean OpenAPI docs

### Phase 3: Recommendation Engine ✅
- Clear eligibility rules
- Weighted scoring system
- Tie breaker logic
- Deterministic output
- Explainability

### Phase 4: Production Features ✅
- Layered architecture
- Database with migrations
- Security (password hashing, JWT, rate limiting)
- Structured logging
- Caching with TTL
- API versioning
- Background tasks
- Metrics and monitoring
- Docker support
- CI/CD pipeline

### Phase 5: Testing & QA ✅
- 116 tests passing
- 69% code coverage
- Security tests
- Repository tests
- Service tests
- Cache tests
- Comprehensive documentation

## License
MIT License
