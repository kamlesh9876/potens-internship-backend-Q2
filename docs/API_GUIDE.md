# API Guide

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints (except `/register` and `/login`) require JWT authentication.

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string"
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Using the Token
```http
Authorization: Bearer <access_token>
```

## Endpoints

### Health
```http
GET /api/v1/health
GET /api/v1/health/db
GET /api/v1/metrics
```

### Users
```http
GET /api/v1/users/me
PUT /api/v1/users/me
GET /api/v1/users/users (Admin only)
GET /api/v1/users/{id} (Admin only)
POST /api/v1/users/{id}/deactivate (Admin only)
POST /api/v1/users/{id}/activate (Admin only)
POST /api/v1/users/{id}/make-admin (Admin only)
POST /api/v1/users/{id}/revoke-admin (Admin only)
```

### Items
```http
GET /api/v1/items (Admin only)
POST /api/v1/items (Admin only)
GET /api/v1/items/{id} (Admin only)
PUT /api/v1/items/{id} (Admin only)
DELETE /api/v1/items/{id} (Admin only)
```

### Recommendations
```http
POST /api/v1/recommend
```

Request:
```json
{
  "age": 25,
  "budget": 200,
  "experience_level": "Beginner",
  "goal": "Career Change",
  "location": "Online",
  "preferred_pace": "Self-paced"
}
```

### Query Parameters (Items)
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `category`: Filter by category
- `location`: Filter by location
- `goal`: Filter by goal
- `skill_level`: Filter by skill level
- `price_min`: Minimum price
- `price_max`: Maximum price
- `search`: Search in name, description, category
- `sort_by`: Sort field (price, name, created_at)
- `order`: Sort order (asc, desc)

## Response Format

Success:
```json
{
  "success": true,
  "message": "string",
  "data": {}
}
```

Error:
```json
{
  "success": false,
  "message": "string",
  "data": null
}
```

## Pagination Response
```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "limit": 20,
  "total_pages": 5,
  "has_next": true,
  "has_previous": false
}
```

## Error Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

## Rate Limiting
- 100 requests per minute per IP
- Health endpoints are exempt
