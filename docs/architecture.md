# System Architecture

The Campus Event & Volunteer Management System follows a classic layered architecture utilizing the Django web framework for backend logic and Django Templates for server-side rendering of the web client.

## High-Level Data Flow

```text
Browser (End User)
   ↓
Django Templates / Web Client
   ↓
Django Views / REST API (Presentation Layer)
   ↓
Service / Business Layer (Business Logic)
   ↓
Django ORM (Data Access Layer)
   ↓
Oracle Database (Persistence)
```

## Architecture Layers

### 1. Web Client Layer (`client/` and Django Templates)
The web interface is built using standard HTML/CSS/JS, driven dynamically by Django Templates. The `client/` conceptual layer uses Bootstrap for styling and handles user interaction. Note that this is NOT a separate Single Page Application (like React or Node.js), but a natively integrated server-rendered GUI that interacts with the backend routes.

### 2. Presentation / API Layer (`api/`, `events/views.py`, etc.)
This layer captures HTTP requests from the browser. 
- **HTML Views:** Standard Class-Based Views (CBV) and function-based views in Django return rendered HTML.
- **REST API:** Django REST Framework (DRF) is utilized to serialize models into JSON data for dynamic async tasks (like background processing queues and API-driven registration workflows).

### 3. Service / Business Logic Layer (`services.py`)
Complex business logic is deliberately decoupled from the views and models into dedicated Service modules (e.g., `registrations/services.py`).
- **Capacity Management:** Validates if an event has available seats before confirming a registration.
- **Background Processing:** Features like `process_registrations` execute in a detached daemon thread, processing waiting lists in the background asynchronously without blocking the user interface.

### 4. Data Access Layer (Django ORM)
The Django Object-Relational Mapper (ORM) abstracts raw SQL. Models defined in `models.py` strictly map to the underlying Oracle relational tables.

### 5. Persistence Layer (Oracle Database)
An Oracle SQL Database serves as the persistent data store, enforcing referential integrity, constraints, and data relations.

## Cross-Cutting Concerns

### Authentication & Authorization
- Django's built-in Authentication system secures the application via session-based cookies.
- **Role-Based Access:** Standard users are linked to `Student` profiles and can only access student-centric pages. Users with the `is_staff` flag are Admins, possessing privileges to manage events and volunteer tasks. Access is enforced using decorators like `@login_required` and mixins like `UserPassesTestMixin`.

### Security Hardening
- **CSRF Protection:** Django's `CsrfViewMiddleware` enforces token validation on all state-changing `POST` requests.
- **XSS Protection:** Django templates automatically escape variable output, safely rendering user input.
- **IDOR Prevention:** Insecure Direct Object Reference vulnerabilities are mitigated by overriding view querysets, ensuring students can only view and modify records that are linked to their authenticated session (`request.user.student_profile`).

### Concurrency Control
For sensitive operations like decrementing available seats on event registration, the application utilizes `select_for_update()` to apply robust database row-level locking, mitigating race conditions during concurrent requests. Background tasks employ atomic transactions and strictly close database connections to prevent pool exhaustion.