# Testing Guide

## Overview
This project uses pytest for testing with 69% code coverage across 116 tests.

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/test_auth.py -v
```

### Run specific test
```bash
pytest tests/test_auth.py::test_register_success -v
```

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── fixtures.py              # Helper functions and fixtures
├── test_auth.py             # Authentication tests
├── test_items.py            # Items CRUD tests
├── test_users.py            # User management tests
├── test_repositories.py     # Repository layer tests
├── test_services.py         # Service layer tests
├── test_cache.py            # Cache functionality tests
└── test_security.py         # Security tests
```

## Fixtures

### Database Fixtures
- `db_session`: In-memory SQLite database session
- `client`: Test client with database override

### User Fixtures
- `admin_user`: Admin user for testing
- `normal_user`: Regular user for testing
- `admin_token`: Admin JWT token
- `user_token`: Regular user JWT token

### Data Fixtures
- `sample_items`: Sample items for testing
- `recommendation_data`: Sample recommendation profile

## Test Coverage

Current coverage: **69%** (116 tests passing)

### High Coverage Areas
- Cache: 100%
- Metrics: 96%
- Main app: 90%
- Items API: 89%
- Dependencies: 88%
- Exceptions: 94%
- User schemas: 94%
- Item service: 94%

### Areas for Improvement
- Old API routes (deprecated)
- Cache decorator
- Security middleware
- User service
- Base repository

## Writing New Tests

1. Add fixtures to `conftest.py` if needed
2. Create test file in `tests/` directory
3. Use helper functions from `fixtures.py`
4. Follow naming convention: `test_<functionality>_<scenario>`

## Security Tests

Security tests cover:
- SQL injection attempts
- XSS payloads
- JWT tampering
- Rate limiting
- Password validation
- Authorization checks
- Security headers

## Continuous Integration

Tests run automatically on GitHub Actions:
- Linting (Black, isort, Flake8)
- Unit tests
- Coverage reporting
- Docker build validation
