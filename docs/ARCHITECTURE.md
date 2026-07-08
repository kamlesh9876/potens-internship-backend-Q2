# Architecture Documentation

## Overview
This is a FastAPI-based backend for a skill path recommendation system with JWT authentication, CRUD operations, and personalized recommendations.

## Project Structure

```
potens-internship-backend-Q2/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── v1/             # Versioned API (v1)
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   ├── items.py    # Items CRUD endpoints
│   │   │   └── users.py    # User management endpoints
│   │   ├── routes.py       # Legacy routes (deprecated)
│   │   ├── auth_routes.py  # Legacy auth (deprecated)
│   │   └── user_routes.py # Legacy users (deprecated)
│   ├── background/          # Background tasks
│   │   └── tasks.py        # Email, analytics, history tasks
│   ├── cache/              # Caching layer
│   │   ├── cache.py        # In-memory cache implementation
│   │   └── decorator.py    # Cache decorator
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration management
│   │   ├── database.py     # Database base
│   │   ├── dependencies.py # Dependency injection
│   │   ├── exceptions.py   # Custom exceptions
│   │   ├── jwt.py          # JWT utilities
│   │   ├── logging.py      # Logging configuration
│   │   └── security.py     # Security utilities
│   ├── db/                 # Database
│   │   ├── database.py     # Database configuration
│   │   └── session.py      # Session management
│   ├── metrics/            # Metrics collection
│   │   └── metrics.py      # Application metrics
│   ├── middleware/         # Custom middleware
│   │   ├── logging.py      # Request logging
│   │   ├── rate_limit.py   # Rate limiting
│   │   └── security.py     # Security headers
│   ├── models/             # SQLAlchemy models
│   │   ├── item.py         # Item model
│   │   └── user.py         # User model
│   ├── repositories/       # Data access layer
│   │   ├── base_repository.py
│   │   ├── item_repository.py
│   │   └── user_repository.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── item.py         # Item schemas
│   │   ├── pagination.py   # Pagination schemas
│   │   ├── recommendation.py
│   │   ├── response.py     # Response schemas
│   │   ├── token.py        # Token schemas
│   │   └── user.py         # User schemas
│   ├── services/           # Business logic layer
│   │   ├── auth_service.py
│   │   ├── explain_service.py
│   │   ├── item_service.py
│   │   ├── recommendation_service.py
│   │   └── user_service.py
│   ├── utils/              # Utilities
│   │   └── ranking.py
│   └── main.py             # Application entry point
├── alembic/                # Database migrations
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .env                    # Environment variables
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker orchestration
└── requirements.txt        # Python dependencies
```

## Architecture Layers

### 1. API Layer (`app/api/`)
- Handles HTTP requests/responses
- Route definitions and validation
- Versioned API structure (`/api/v1/`)
- Integrates middleware and dependencies

### 2. Service Layer (`app/services/`)
- Business logic implementation
- Coordinates between repositories
- Handles complex operations
- Example: `RecommendationService` builds recommendations

### 3. Repository Layer (`app/repositories/`)
- Data access abstraction
- Database operations
- CRUD operations
- Query building

### 4. Model Layer (`app/models/`)
- SQLAlchemy ORM models
- Database schema definition
- Relationships between entities

### 5. Schema Layer (`app/schemas/`)
- Pydantic models for validation
- Request/response serialization
- Data validation

## Key Components

### Authentication
- JWT-based authentication
- Role-based access control (Admin/User)
- Password hashing with bcrypt
- Token expiration handling

### Caching
- In-memory cache with TTL
- Cache decorator for easy caching
- Cache invalidation on data changes
- 5-minute default TTL

### Middleware Stack
1. **Request Logging**: Logs all requests with execution time
2. **Security Headers**: Adds security headers to responses
3. **Rate Limiting**: 100 requests/minute per IP

### Background Tasks
- Welcome email sending
- User login logging
- Password change logging
- Recommendation history
- Item analytics

### Metrics
- Request counting
- Response time tracking
- Cache statistics
- Per-endpoint metrics

## Database

### Models
- **User**: id, username, email, hashed_password, full_name, is_active, is_admin
- **Item**: id, name, category, price, skill_level, goal, location, pace, description, timestamps

### Indexes
- Single-column indexes on frequently queried fields
- Composite indexes for common query patterns
- Performance optimization for filtering/sorting

## Configuration

### Environment Profiles
- `.env.dev`: Development configuration
- `.env.test`: Testing configuration
- `.env.prod`: Production configuration

### Key Settings
- Database URL
- JWT secret key
- Admin token
- Token expiration time
- Debug mode

## Deployment

### Docker
- Multi-stage Python 3.11 image
- Health checks
- Volume mounts for data persistence
- Optional PostgreSQL and Redis services

### CI/CD
- GitHub Actions pipeline
- Automated testing
- Linting (Black, isort, Flake8)
- Coverage reporting
- Docker build validation

## Security Features

- Password validation (length, complexity)
- JWT token validation
- SQL injection prevention (ORM)
- XSS protection (input validation)
- Rate limiting
- Security headers
- Request ID tracking

## Performance Optimizations

- Database indexes
- In-memory caching
- Connection pooling
- Efficient queries
- Pagination

## API Versioning

- Versioned routes under `/api/v1/`
- Backward compatibility
- Easy migration to new versions
