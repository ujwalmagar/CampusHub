# Campus Event & Volunteer Management System: Implementation Roadmap

This roadmap translates the requirements from `MASTER.md` (and its linked `/docs/` specifications) into a practical, step-by-step development plan. It covers the full lifecycle from environment setup through final verification.

## Important Rules for Development
- **No skipping:** Complete all tasks in a phase before moving to the next.
- **Security by default:** Implement input validation, role checks, and error handling *during* feature creation, not at the end.
- **Verification:** Run tests and check the UI/API at the end of every major phase.

---

## Phase 0: Environment & Preparation
**Goal:** Ensure the local development environment is ready to connect to Oracle Database.

- [x] Verify Python 3.x installation and pip functionality.
- [x] Verify Oracle Database is installed, running, and accessible.
- [x] Verify Oracle SQL Developer is installed and connects to the database.
- [x] Verify the Oracle listener and services are active.
- [x] Create a dedicated Oracle user/schema for the application (e.g., `campushub_user`).
- [x] Grant necessary privileges to the Oracle user.
- [x] Verify Python can connect to Oracle (e.g., using `oracledb` or `cx_Oracle` via a test script).
- [x] **Checkpoint:** Database connectivity confirmed.

## Phase 1: Specification & Design
**Goal:** Ensure all documentation is final and understood.

- [x] Verify `MASTER.md` and all files in `docs/` are finalized.
- [x] Review ER diagram (`docs/database.md`).
- [x] Review UML Class diagram (`docs/architecture.md`).
- [x] Review Navigation diagram (`docs/product.md`).
- [x] Review API contracts (`docs/api.md`).
- [x] Review `AGENTS.md` for core engineering and security principles.

## Phase 2: Django Foundation
**Goal:** Initialize the project and configure core settings.

- [x] Create a Python virtual environment.
- [x] Install Django, Django REST Framework, and Oracle database adapter.
- [x] Create the Django project (`config`).
- [x] Create Django apps: `accounts`, `students`, `events`, `registrations`, `volunteers`, `reports`.
- [x] Configure `settings.py` for Oracle Database connection.
- [x] Verify Django can connect to Oracle (`python manage.py inspectdb` or similar).
- [x] Configure static files and template directories.
- [x] Run initial Django migrations for built-in apps (admin, auth, contenttypes, sessions).
- [x] **Checkpoint:** Blank Django project runs successfully (`python manage.py runserver`).

## Phase 3: Authentication & Authorization
**Goal:** Secure the application and manage user identities.

- [x] Configure Django's built-in User model for authentication.
- [x] Create `accounts` views and templates for Signup.
- [x] Create `accounts` views and templates for Login.
- [x] Create `accounts` views and templates for Logout.
- [x] Implement role-based access control (differentiating Student and Admin).
- [x] Secure routes so only authenticated users can access the dashboard.
- [x] Prevent Admin routes from being accessed by Students.
- [x] Write security tests for Signup, Login, and Authorization logic.
- [x] **Checkpoint:** Authentication flow tested and secured.

## Phase 4: Core Data Models & Database
**Goal:** Map business requirements to Django ORM and Oracle database.

- [x] Implement `Student` model (linked to Auth User, Name, Email, Phone, Course).
- [x] Implement `Event` model (Title, Description, Date, Location, Capacity, Status).
- [x] Implement `Registration` model (Foreign keys to Student and Event, Status, Timestamp).
- [x] Implement `VolunteerTask` model (Foreign keys to Event and Student, Task Name, Status, Timestamp).
- [x] Add unique constraints (e.g., a student cannot register for the same event twice).
- [x] Create Django migrations for the core models.
- [x] Apply migrations to Oracle database.
- [x] Verify the schema in Oracle SQL Developer.
- [x] **Checkpoint:** Core models exist and data integrity rules (constraints) are applied.

## Phase 5: Backend / Core Services (Business Logic)
**Goal:** Encapsulate business rules away from views and serializers.

- [x] Create `students/services.py` (CRUD operations for students).
- [x] Create `events/services.py` (CRUD operations for events).
- [x] Create `registrations/services.py` (Registration logic: capacity checks, duplicate checks, status updates).
- [x] Create `volunteers/services.py` (Task assignment and management).
- [x] Write unit tests for service layer operations to ensure business rules are enforced.

## Phase 6: API Development (REST Framework)
**Goal:** Expose business logic via REST endpoints with validation.

- [x] Create DTO serializers for `Student`, `Event`, `Registration`, and `VolunteerTask`.
- [x] Implement input validation in serializers (e.g., required fields, capacity > 0).
- [x] Implement error handling for consistent API responses.
- [x] Build `Student` API endpoints.
- [x] Build `Event` API endpoints.
- [x] Build `Registration` API endpoints.
- [x] Build `VolunteerTask` API endpoints.
- [x] Write API tests ensuring endpoints validate input and return correct HTTP status codes.

## Phase 7: Business Queries & Reports
**Goal:** Implement complex queries mapping related entities.

- [x] Implement logic/API for "Student → Events" (Show all events registered by a student).
- [x] Implement logic/API for "Event → Students" (Show all students registered for an event).
- [x] Implement logic/API for "Event → Volunteer Tasks" (Show assignments for an event).
- [x] Create `reports/services.py` and implement Complex Query 1: Event Participation Report.
- [x] Create `reports/services.py` and implement Complex Query 2: Student Participation Report.
- [x] Expose complex queries via Report API endpoints.
- [x] Test all queries against seed data to verify accuracy.

## Phase 8: Background / Asynchronous Processing
**Goal:** Process pending registrations safely.

- [x] Implement a Django background processing mechanism (e.g., a custom management command or a simple async worker loop).
- [x] Build the logic to find pending registrations.
- [x] Check event capacity and confirm registrations where capacity allows.
- [x] Leave or handle registrations where capacity is unavailable.
- [x] Build the `POST /api/registrations/process/` endpoint for Admin to trigger processing.
- [x] Write tests to verify race conditions are avoided and capacity is respected.

## Phase 9: Frontend / Web GUI
**Goal:** Provide an intuitive UI using Django Templates.

- [x] Create a base layout template (`base.html`) with navigation.
- [x] Build Student Dashboard (Welcome, registered events, upcoming events, volunteer tasks).
- [x] Build Admin Dashboard (Totals, pending registrations, quick actions).
- [x] Build Event pages (List, Detail, Create, Edit).
- [x] Build Registration pages (Student: Register, Cancel; Admin: Manage).
- [x] Build Volunteer task pages (Admin: Assign, update status).
- [x] Build Report viewing pages for Admin.
- [x] Implement UI validation and error message display (using Django messages).
- [x] **Checkpoint:** Complete UI journey tested from the browser.

## Phase 10: Security Hardening & Testing
**Goal:** Perform a final security sweep and run full end-to-end tests.

- [ ] Verify CSRF protection is active on all forms and state-changing APIs.
- [ ] Verify XSS protections (Django template auto-escaping).
- [ ] Verify SQL injection prevention (Ensure ORM is used safely everywhere).
- [ ] Check IDOR (Ensure students can only view/cancel their own registrations).
- [ ] Review error handling to ensure internal stack traces are never exposed.
- [ ] Ensure no secrets are hardcoded in the source code.
- [ ] Run full test suite (Unit, API, Auth, E2E).
- [ ] **Checkpoint:** No critical security vulnerabilities found.

## Phase 11: Final Documentation & Database Scripts
**Goal:** Prepare deliverables for submission.

- [ ] Extract `schema.sql` (Oracle schema creation script).
- [ ] Create `seed.sql` with realistic demo data (10+ students, 5+ events, 15+ registrations, 8+ volunteer tasks).
- [ ] Extract `queries.sql` containing the required relationship and complex SQL queries.
- [ ] Update `docs/` with any minor architectural or API changes made during implementation.
- [ ] Write User Manual.
- [ ] Write Installation Manual.
- [ ] Generate final `report.md`.

## Phase 12: Final Review & Delivery
**Goal:** Verify everything works from a clean slate.

- [ ] Spin up a clean environment (fresh virtual environment).
- [ ] Run Oracle schema script and verify tables.
- [ ] Run Oracle seed script and verify data.
- [ ] Run `python manage.py runserver` and navigate through all roles (Student, Admin).
- [ ] Verify all 14 Success Criteria from `MASTER.md` are met.
- [ ] Rehearse demonstration flow.
- [ ] Create final ZIP archive for submission.
