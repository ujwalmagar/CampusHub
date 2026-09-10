# API Documentation

# 14. API Design

Base URL:

```text
/api/
```

All API endpoints return JSON.

---

---

# 15. Authentication API

## Signup

```http
POST /api/auth/signup/
```

Request:

```json
{
  "name": "Ram Sharma",
  "email": "ram@example.com",
  "phone": "9800000000",
  "course": "BSc CSIT",
  "password": "SecurePassword123",
  "password_confirm": "SecurePassword123"
}
```

Success:

```http
201 Created
```

Response:

```json
{
  "message": "Account created successfully",
  "user": {
    "id": 1,
    "email": "ram@example.com"
  },
  "student": {
    "id": 1,
    "name": "Ram Sharma",
    "course": "BSc CSIT"
  }
}
```

## Login

```http
POST /api/auth/login/
```

Request:

```json
{
  "email": "ram@example.com",
  "password": "SecurePassword123"
}
```

Success:

```http
200 OK
```

Response:

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "ram@example.com",
    "role": "STUDENT"
  }
}
```

Authentication may use Django session authentication for the web client.

---

---

# 16. Student API

## List Students

```http
GET /api/students/
```

## Retrieve Student

```http
GET /api/students/{id}/
```

## Create Student

```http
POST /api/students/
```

Request:

```json
{
  "name": "Ram Sharma",
  "email": "ram@example.com",
  "phone": "9800000000",
  "course": "BSc CSIT"
}
```

## Update Student

```http
PUT /api/students/{id}/
```

## Partial Update

```http
PATCH /api/students/{id}/
```

## Delete Student

```http
DELETE /api/students/{id}/
```

## Student Events

```http
GET /api/students/{id}/events/
```

Response:

```json
{
  "student": {
    "id": 1,
    "name": "Ram Sharma"
  },
  "events": [
    {
      "id": 4,
      "title": "Blood Donation Camp",
      "event_date": "2026-09-15T10:00:00",
      "location": "College Hall",
      "registration_status": "CONFIRMED"
    }
  ]
}
```

---

---

# 17. Event API

## List Events

```http
GET /api/events/
```

## Retrieve Event

```http
GET /api/events/{id}/
```

## Create Event

```http
POST /api/events/
```

Request:

```json
{
  "title": "Blood Donation Camp",
  "description": "Annual campus blood donation program",
  "event_date": "2026-09-15T10:00:00",
  "location": "College Hall",
  "capacity": 50,
  "status": "OPEN"
}
```

## Update Event

```http
PUT /api/events/{id}/
```

## Partial Update

```http
PATCH /api/events/{id}/
```

## Delete Event

```http
DELETE /api/events/{id}/
```

## Event Registrations

```http
GET /api/events/{id}/registrations/
```

## Event Volunteer Tasks

```http
GET /api/events/{id}/volunteer-tasks/
```

---

---

# 18. Registration API

## List Registrations

```http
GET /api/registrations/
```

## Retrieve Registration

```http
GET /api/registrations/{id}/
```

## Create Registration

```http
POST /api/registrations/
```

Request:

```json
{
  "student_id": 1,
  "event_id": 4
}
```

Response:

```json
{
  "id": 10,
  "student_id": 1,
  "event_id": 4,
  "status": "PENDING",
  "registered_at": "2026-09-05T20:00:00"
}
```

## Update Registration

```http
PATCH /api/registrations/{id}/
```

## Delete/Cancel Registration

```http
DELETE /api/registrations/{id}/
```

Business rules MUST be enforced through the service layer.

---

---

# 19. Volunteer Task API

## List Tasks

```http
GET /api/volunteer-tasks/
```

## Retrieve Task

```http
GET /api/volunteer-tasks/{id}/
```

## Create Task

```http
POST /api/volunteer-tasks/
```

Request:

```json
{
  "event_id": 4,
  "student_id": 1,
  "task_name": "Registration Desk",
  "task_status": "ASSIGNED"
}
```

## Update Task

```http
PUT /api/volunteer-tasks/{id}/
```

## Partial Update

```http
PATCH /api/volunteer-tasks/{id}/
```

## Delete Task

```http
DELETE /api/volunteer-tasks/{id}/
```

---

---

# 20. API Status Codes

Use appropriate HTTP responses.

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
500 Internal Server Error
```

Use `409 Conflict` for cases such as:

- duplicate registration
- event capacity conflict

---