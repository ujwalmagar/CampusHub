# Final Academic Report: Campus Event & Volunteer Management System

## 1. Project Title
Campus Event & Volunteer Management System

## 2. Introduction
The Campus Event & Volunteer Management System is a centralized digital platform designed to bridge the gap between event organizers and students within a university ecosystem. It streamlines the lifecycle of campus events by automating enrollments, waiting lists, and the assignment of logistical volunteer duties.

## 3. Problem Statement
Many educational institutions currently rely on disjointed, manual, or paper-based systems to manage campus events. This leads to chaotic registration queues, overbooked venues, untracked volunteer efforts, and a high administrative burden for staff attempting to synthesize data into meaningful reports.

## 4. Objectives
- To deliver an automated, web-accessible interface for students to browse and securely register for campus events.
- To provide university administrators with a comprehensive dashboard to enforce capacities, assign volunteer roles, and view aggregated participation reports.
- To design a secure, transactional backend that strictly prevents over-booking and manages unauthorized access through robust authorization protocols.

## 5. Scope
The scope encompasses a full-stack web application encompassing Student profiles, Event directories, Waitlisted Registration queues, and Volunteer Task assignments. The system includes Role-Based Access Control distinguishing standard students from administrative staff. Financial transactions and external email notifications are explicitly outside the scope of this project.

## 6. Technologies Used
- **Backend Framework:** Python (Django)
- **API/Serialization:** Django REST Framework (DRF)
- **Database Management:** Oracle Database (via `oracledb` adapter)
- **Frontend GUI:** Django Server-Side Templates, HTML5, CSS3, JavaScript, Bootstrap
- **Security:** CSRF Middleware, Session-based Authentication

## 7. System Architecture
The application utilizes a classic MVT (Model-View-Template) layered architecture tailored for Django, integrating REST APIs for background asynchronous operations.
- **Client Layer:** Renders HTML from Django Templates.
- **Presentation Layer:** Views and ViewSets handling HTTP requests.
- **Service Layer:** Houses the `process_registrations` capacity algorithms.
- **Data Access Layer:** The Django ORM translating Python objects to SQL.
- **Persistence Layer:** Oracle Database.

*(Please refer to `docs/architecture.md` for extended architectural details).*

## 8. Database Design
The relational database strictly normalizes data into four distinct domain domains ensuring ACID compliance and referential integrity via Foreign Key Constraints cascading on deletion.

*(Please refer to `docs/database-design.md` for detailed structure mappings).*

## 9. Table Descriptions
- **`students`**: Maintains the academic profile and demographic data of standard users.
- **`events`**: Defines the institutional occurrences, including strict numeric capacities and scheduled timestamps.
- **`registrations`**: An associative bridge tracking unique Many-to-Many enrollments between Students and Events, handling `PENDING` vs `CONFIRMED` states.
- **`volunteer_tasks`**: Defines operational duties assigned to students per event, tracking lifecycle states from `ASSIGNED` to `COMPLETED`.

## 10. ER Diagram
The system encompasses a normalized entity structure natively linked via Oracle Foreign Keys.

*(Please refer to `docs/er-diagram.md` for the Mermaid Visual Diagram).*

## 11. Class Diagram
The software models encapsulate domain constraints natively (e.g. `clean()` overriding for capacity assertions).

*(Please refer to `docs/class-diagram.md` for the Mermaid Object Relational Diagram).*

## 12. API / DTO / Service Architecture
Data entering the system through the `/api/` routing prefix is explicitly passed through Data Transfer Objects (DTOs), defined as DRF Serializers (e.g., `RegistrationSerializer`). These serializers abstract away internal model constraints and sanitize JSON payloads before they are delegated to the underlying Business Service layer (`registrations/services.py`).

## 13. Authentication and Authorization
Django's native session-based authentication secures all routes. Access controls are rigorously split:
- **Students:** Can only access basic Views and modify records strictly tied to their own internal `student_profile` object.
- **Admins:** Authorized via the `is_staff` database flag, utilizing Django's `UserPassesTestMixin` to gate access to the `/events/manage/` and reporting dashboards.

## 14. CRUD Functionality
Complete **C**reate, **R**ead, **U**pdate, and **D**elete functionalities are provided through native Web GUIs. Admins can seamlessly manipulate Events and Volunteer Tasks through intuitive forms, while Soft Deletes (`CANCELLED` status overrides) ensure historical records remain intact after deletion commands.

## 15. Required Relationship Queries
All required Oracle SQL relationship aggregations successfully extract multidimensional data bridging primary tables (e.g., matching a Student to their corresponding Events).

*(Please refer to `database/queries.sql` for raw syntax).*

## 16. Complex Queries & Reports
The platform natively handles multi-table JOINs and aggregation techniques (e.g., `COUNT`, `COALESCE`) to construct rich dashboards:
- **Event Participation Report:** Compares declared capacity against grouped confirmed registrations and allocated volunteers.
- **Student Engagement Report:** Quantifies overall student activity dynamically.

## 17. Background / Asynchronous Processing
Handling waitlist promotions is abstracted into an asynchronous background daemon thread (`process_registrations()`). This daemon relies on Oracle row-level locking (`select_for_update()`) enveloped in an `atomic` transaction, safely processing registrations sequentially without blocking or freezing the Administrative UI.

## 18. Web GUI
The web layer utilizes Django HTML Templates coupled with dynamic Context dictionaries to render a responsive, role-aware interface.

## 19. Security Measures
Security hardening actively prevents industry-standard attack vectors:
- **CSRF:** Token enforcement mitigates Cross-Site Request Forgeries on form submissions.
- **XSS:** Template auto-escaping neutralizes injected payload executions.
- **IDOR:** By explicitly ignoring client-provided primary keys (e.g., hidden `student_id` fields) and relying wholly on the authenticated server session, malicious payload tampering is completely mitigated.

## 20. Testing
Comprehensive QA was conducted to verify security, routing, and workflows.

**Final Test Results:**
- CSRF verification: PASS
- XSS verification: PASS
- IDOR - view own registration: PASS
- IDOR - view another registration: PASS (Denied as expected)
- IDOR - cancel own registration: PASS
- IDOR - cancel another registration: PASS (Denied as expected)
- Registration tampering: PASS (Denied as expected)
- Student E2E workflow: PASS
- Admin E2E workflow: PASS
- Role authorization: PASS
- Live regression/E2E verification: PASS

*Note on Automated Tooling:* While standard `manage.py test` attempts were executed, local Oracle XE limitations (`DPY-1001: not connected to database` / `ORA-01031: insufficient privileges`) prevented the automatic generation of a mirror test database. To bypass this, a dedicated E2E Verification script (`run_e2e_live.py`) successfully tested all security assertions against the live development database.

## 21. Screenshots
**TODO: The following screens must be captured manually and inserted here prior to final submission:**

### Student View
- [ ] 1. Signup Form
- [ ] 2. Login Gateway
- [ ] 3. Student Dashboard
- [ ] 4. Event Listing (`/events/`)
- [ ] 5. Event Details (`/events/<id>/`)
- [ ] 6. Waitlisted Registration Screen
- [ ] 7. My Registrations 
- [ ] 8. Volunteer Tasks Panel
- [ ] 9. Profile

### Admin View
- [ ] 10. Admin Dashboard
- [ ] 11. Student Management
- [ ] 12. Event Management CRUD
- [ ] 13. Registration Management Panel
- [ ] 14. Volunteer Task Assignment Interface
- [ ] 15. Process Pending Registrations (Waitlist Execution)
- [ ] 16. Reports Dashboard

## 22. User Manual Reference
For detailed instructions on navigating workflows, please refer to the `report/docs/user-manual.md`.

## 23. Installation Manual Reference
For technical deployment guidelines, environment configuration, and database seeding procedures, please refer to the `report/docs/installation-manual.md`.

## 24. Conclusion
The Campus Event & Volunteer Management System successfully implements a sophisticated, Oracle-backed platform catering to both operational staff and student users. By combining resilient asynchronous transaction management with rigorous security validations, it fulfills the overarching academic mandate of translating raw relational database principles into a scalable, working web application.

## 25. Assignment Requirement Traceability

| Requirement | Implementation | Evidence |
| :--- | :--- | :--- |
| Python web application | Django Framework | Project source codebase |
| Oracle database | Oracle DB + Django ORM | `database/` folder + `config/settings.py` |
| 3+ related tables | 4 Core Tables (Students, Events, Registrations, Volunteer Tasks) | ER diagram (`docs/er-diagram.md`) |
| ORM classes | Django Models | `models.py` files in server apps |
| DTO/API serializers | DRF Serializers | `api/serializers.py` |
| Service layer | Abstracted Service Functions | `registrations/services.py` |
| CRUD | Native Django Forms & Generic Class-Based Views | UI and Application Views |
| Related queries | Evaluated Relationship SQL | `database/queries.sql` |
| Complex queries | Participation Aggregation SQL | `database/queries.sql` + `/reports/` |
| Background task | Daemonized pending registration waitlist processor | `services.py` threading implementation |
| Web GUI | Dynamic Django Templates + Bootstrap | `templates/` structure |
| Security | Form-level CSRF, IDOR Request Overrides, Template XSS Escaping | `run_e2e_live.py` Tests |
| Testing | Native E2E Test Suite simulating Network calls | `run_e2e_live.py` Python Script |
| Documentation | Extensive Markdown Reporting | `docs/` and `report/` repository directories |
