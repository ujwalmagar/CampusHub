# Development Documentation

# 39. Project Structure

```text
campus-event-manager/
│
├── MASTER.md
├── PROGRESS.md
├── README.md
├── requirements.txt
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── students/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── events/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── registrations/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── volunteers/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── reports/
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── templates/
│   ├── base.html
│   ├── registration/
│   ├── dashboard/
│   ├── events/
│   ├── registrations/
│   ├── volunteers/
│   └── reports/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── queries.sql
│
├── docs/
│   ├── architecture.md
│   ├── database-design.md
│   ├── uml.md
│   └── navigation.md
│
└── report/
    └── report.md
```

---

---

# 39.1 What Each Part Does

## `config/`
Contains the main Django project configuration.
Responsible for:
* Django settings
* installed applications
* database configuration
* middleware
* main URL routing
* ASGI/WSGI configuration

It should NOT contain business logic.

## `accounts/`
Responsible for authentication and user accounts.
Examples:
* Signup
* Login
* Logout
* User roles
* Authentication-related logic
Use Django's built-in authentication system where possible.

## `students/`
Responsible for student-related functionality.
Examples:
* Student profile
* Student CRUD
* Student dashboard information
* Student-related queries

## `events/`
Responsible for events.
Examples:
* Create event
* View events
* Update event
* Delete event
* Event details
* Event capacity
* Event status

## `registrations/`
Responsible for students registering for events.
Examples:
* Register for an event
* View registration
* Cancel registration
* Update registration status
* Registration-related queries

## `volunteers/`
Responsible for volunteer tasks.
Examples:
* Create volunteer task
* Assign task to student
* Update task status
* Delete task
* View assigned tasks

## `reports/`
Responsible for the required complex queries and reports.
Examples:
* Event participation report
* Student participation report
* Registration statistics
* Volunteer statistics
The report layer can call the service layer, which performs the required ORM queries.

---

---

# 45. Definition of Done

A feature is complete only when:

```text
[ ] Database model exists
[ ] ORM model works
[ ] Business service exists
[ ] Serializer/DTO exists where applicable
[ ] API endpoint works
[ ] UI works where applicable
[ ] Validation exists
[ ] Error handling exists
[ ] Authorization is correct
[ ] Test exists
[ ] Documentation is updated
```

---

---

# 46. Development Phases

Do not build the whole project in one step.

## Phase 0 — Environment

```text
[ ] Verify Python
[ ] Verify pip
[ ] Verify Oracle Database
[ ] Verify Oracle SQL Developer
[ ] Verify Oracle listener/service
[ ] Create application Oracle user
[ ] Verify Python → Oracle connection
```

## Phase 1 — Specification

```text
[ ] MASTER.md finalized
[ ] ER diagram finalized
[ ] Class diagram finalized
[ ] Navigation finalized
[ ] API contracts finalized
```

## Phase 2 — Django Foundation

```text
[ ] Create virtual environment
[ ] Create Django project
[ ] Configure Oracle
[ ] Install dependencies
[ ] Verify Django → Oracle
[ ] Create Django apps
```

## Phase 3 — Authentication

```text
[ ] Signup
[ ] Login
[ ] Logout
[ ] Student profile
[ ] Admin role
[ ] Authorization
```

## Phase 4 — Core Models

```text
[ ] Student
[ ] Event
[ ] Registration
[ ] VolunteerTask
[ ] Relationships
[ ] Constraints
```

## Phase 5 — CRUD

```text
[ ] Student CRUD
[ ] Event CRUD
[ ] Registration CRUD
[ ] VolunteerTask CRUD
```

## Phase 6 — APIs

```text
[ ] Authentication APIs
[ ] Student APIs
[ ] Event APIs
[ ] Registration APIs
[ ] Volunteer APIs
```

## Phase 7 — Business Queries

```text
[ ] Student → Events
[ ] Event → Students
[ ] Event → Volunteer Tasks
[ ] Event Participation Report
[ ] Student Participation Report
```

## Phase 8 — Background Processing

```text
[ ] Processing endpoint
[ ] Background/asynchronous task
[ ] Database update
[ ] Processing result
```

## Phase 9 — GUI

```text
[ ] Student dashboard
[ ] Admin dashboard
[ ] Event pages
[ ] Registration pages
[ ] Volunteer pages
[ ] Reports
```

## Phase 10 — Testing

```text
[ ] Unit/service tests
[ ] API tests
[ ] Authentication tests
[ ] Authorization tests
[ ] End-to-end testing
```

## Phase 11 — Documentation

```text
[ ] Architecture
[ ] ER diagram
[ ] Class diagram
[ ] Navigation diagram
[ ] Table descriptions
[ ] Screenshots
[ ] User manual
[ ] Installation manual
[ ] Report
```

## Phase 12 — Final Verification

```text
[ ] Clean environment test
[ ] Oracle schema script tested
[ ] Seed script tested
[ ] Project runs from fresh setup
[ ] All assignment requirements verified
[ ] Demonstration flow rehearsed
[ ] ZIP created
```

---

---

# 47. AI Coding Agent Workflow

The coding agent must work incrementally.

Before each task:

```text
1. Read MASTER.md.
2. Read PROGRESS.md.
3. Identify the current phase.
4. Identify dependencies.
5. Implement only the requested/current phase.
6. Run tests/checks.
7. Update PROGRESS.md.
8. Report what was completed.
9. Report what should be built next.
```

The agent must NOT jump randomly between phases.

If Phase 2 is incomplete, do not start building complex reports.

---

---

# 47.1 Development Rule for the AI Coding Agent

Before implementing any feature, identify which layer it belongs to.

Example:
### Feature: Student registers for event
```text
Browser
   ↓
Registration HTML page
   ↓
Django View / API
   ↓
Registration Serializer
   ↓
register_student_for_event()
   ↓
Registration ORM
   ↓
Oracle
```
The agent should not implement all of this inside one giant view function.
Keep responsibilities separated.

---

---

# 48. Progress Tracking

`PROGRESS.md` must always contain:

```text
Current Phase
Completed Work
Current Task
Next Task
Blocked Items
Tests Run
Known Issues
```

Example:

```markdown
# Project Progress

## Current Phase
Phase 2 — Django Foundation

## Completed
- [x] Python verified
- [x] Virtual environment created

## Current Task
Configure Django connection to Oracle.

## Next
- [ ] Verify database connection
- [ ] Create Django apps

## Blocked
None

## Tests
- Python version: PASS
- Oracle connection: PENDING
```

---

---

# 51. What NOT to Do

Do not:

- Build a landing page before core functionality.
- Add AI just to make the project sound advanced.
- Add unnecessary technologies.
- Use SQLite during final implementation.
- Put all logic inside views.
- Hardcode database records in Python.
- Hardcode passwords.
- Create random tables just to increase table count.
- Create APIs that do not correspond to actual business operations.
- Build reports with fake values.
- Skip testing.
- Wait until the final day to discover Oracle connection problems.
- Implement everything before verifying each layer.

---

---

# 52. Current Starting Point

The immediate development order is:

```text
1. Verify Oracle installation
        ↓
2. Create Oracle application user/schema
        ↓
3. Verify Python can connect to Oracle
        ↓
4. Create Django project
        ↓
5. Connect Django ORM to Oracle
        ↓
6. Create authentication
        ↓
7. Create domain models
        ↓
8. Continue through phases
```

Do not move to the next major phase until the current phase is verified.

---