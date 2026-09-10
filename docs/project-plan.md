# CampusHub Project Plan

This document summarizes the chronological development phases of the Campus Event & Volunteer Management System as tracked natively in the repository via `PROGRESS.md`.

The project follows a standard Software Development Lifecycle (SDLC) tailored for an academic semester project, transitioning from initial design to deep implementation, testing, and documentation.

## Phase 1: Planning and Architecture
- Analyzed `MASTER.md` to solidify core requirements.
- Finalized technology stack: Python, Django, Django REST Framework, and Oracle Database.

## Phase 2: Project Initialization
- Configured isolated virtual environments and installed requirements.
- Bootstrapped the Django app (`CampusHub`).
- Configured connection string and verified local Oracle XE Database connectivity.

## Phase 3: Authentication & User Profiles
- Implemented Django's native authentication flow (Sign Up, Login, Logout).
- Created the `Student` model with a One-to-One relationship to the base `User` entity to segregate auth details from domain details.

## Phase 4: Core Domain Modeling
- Developed the `Event`, `Registration`, and `VolunteerTask` models mapping directly to Oracle schema definitions.
- Enforced table constraints at the ORM layer, explicitly setting table names and referential ON CASCADE policies.

## Phase 5: Service Layer & Business Logic
- Abstracted heavy algorithmic logic away from views.
- Implemented `register_for_event()` with capacity constraints.
- Integrated row-level locking via `select_for_update()` to manage concurrent modifications on Oracle.

## Phase 6: API and DTO Layer
- Engineered DRF serializers (Data Transfer Objects).
- Exposed the `RegistrationViewSet` and `EventViewSet` to handle JSON I/O safely.
- Added strict field validations.

## Phase 7: Advanced Data Queries
- Drafted SQL deliverables (`schema.sql`, `seed.sql`, `queries.sql`).
- Handled Oracle-specific complex queries merging at least 3 distinct tables for analytical reporting.

## Phase 8: Background Tasks & Asynchronous Queues
- Developed `process_registrations()` as a daemonized Python background thread.
- Enabled administrators to trigger waitlist resolutions synchronously without freezing the user interface, incorporating strict database connection release safeguards (`connections.close_all()`).

## Phase 9: Web User Interface
- Configured Django Templates (`base.html`, `admin.html`, `student.html`).
- Mapped Role-Based UI visibility rules natively via context variables (`is_staff`).
- Constructed full interactive CRUD panels for Events and Volunteer Tasks.

## Phase 10: Security Hardening & QA Testing
- Conducted extensive negative testing and fuzzing on CSRF mechanisms.
- Validated auto-escaping templates for XSS defense.
- Remediated Insecure Direct Object Reference (IDOR) vulnerabilities by tightly coupling querysets to the authenticated user's session state.
- Automated tests via `django.test.Client` validated a 100% Security PASS score.

## Phase 11: Final Documentation & Database Scripts (Current Phase)
- Extracting the raw Oracle SQL structure matching the actual application state.
- Generating relational diagrams (ERD, UML) and User Manuals.
- Verifying traceability against core academic constraints.

## Phase 12: Final Delivery (Upcoming)
- Code cleanup.
- ZIP packaging.
- Submission release.
