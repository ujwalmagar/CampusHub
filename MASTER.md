# MASTER.md
# Campus Event & Volunteer Management System
## Master Product & Engineering Specification

> **Status:** Source of truth for implementation
> **Project Type:** Enterprise Web Application
> **Academic Context:** Semester 4 Enterprise Application Development / DBMS Assignment
> **Backend:** Python + Django
> **Database:** Oracle
> **Client:** Django Templates + HTML/CSS/Bootstrap
> **API:** Django REST Framework
> **ORM:** Django ORM
> **Primary Goal:** Build a small, realistic, complete enterprise application that satisfies every assignment requirement without unnecessary complexity.

---

# Documentation Index

- [Product & Requirements](docs/product.md)
- [Architecture](docs/architecture.md)
- [Database & Queries](docs/database.md)
- [API Contracts](docs/api.md)
- [Security & Auth](docs/security.md)
- [Testing & Verification](docs/testing.md)
- [Development Workflow](docs/development.md)

---

# 1. Source of Truth

This document is the authoritative specification for the project.

The coding agent MUST:

1. Read this file before implementing features.
2. Follow the architecture, database design, API contracts, business rules, and page flows defined here.
3. Not invent major features, tables, endpoints, relationships, or technologies without approval.
4. Not replace Oracle with SQLite, PostgreSQL, MySQL, or another database.
5. Keep business logic in the service layer rather than putting business rules directly in views.
6. Keep API contracts stable unless the specification is explicitly updated.
7. Keep documentation synchronized with implementation.
8. Keep the application simple enough for a Semester 4 academic project.
9. Prefer clear, understandable code over unnecessary abstractions.
10. Never mark a requirement complete unless it is implemented and tested.

If implementation reveals a conflict or ambiguity, stop and document the issue rather than silently changing the design.

---

---

# 7. Technology Stack

## Required

- Python 3.x
- Django
- Django REST Framework
- Oracle Database
- Oracle SQL Developer
- Django ORM
- HTML
- CSS
- Bootstrap
- Git

The academic specification requires Python, Django or Flask, Oracle Database, Oracle SQL Developer, and a development IDE. This project uses Django.

## Do Not Introduce Without Approval

- React
- Next.js
- Node.js backend
- PostgreSQL
- MongoDB
- Firebase
- Supabase
- Docker
- Redis
- Celery
- Kubernetes

Unless a later implementation decision specifically requires one of these, keep the stack simple.

---

---

# 49. Assignment Requirement Traceability

| Assignment Requirement | Project Implementation | Evidence |
|---|---|---|
| Python web application | Django application | Source code |
| Oracle backend | Oracle Database | SQL scripts + demo |
| 3+ linked tables | 4 core tables | ER diagram |
| ORM classes | Django models | Source code |
| DTO/API serializers | DRF serializers | Source code |
| Business service layer | Service modules | Source code |
| CRUD each table | All 4 core tables | UI/API demo |
| 3 related queries | Student Events, Event Students, Event Tasks | SQL/API |
| 2 complex queries | Event Participation, Student Participation | SQL/API |
| Background task | Registration processing | Demo/source |
| Web GUI | Django templates | Screenshots/demo |
| Table descriptions | Report | report.md |
| ER diagram | Mermaid/documentation | docs |
| Class diagram | UML/Mermaid | docs |
| Screenshots | Report | report.md |
| Markdown report | report/report.md | Submission |
| SQL scripts | database/*.sql | Submission |
| User manual | Report/documentation | Submission |
| Installation manual | Report/documentation | Submission |

---

---

# 53. Success Criteria

The project is successful when:

1. A student can create an account and log in.
2. A student can browse events and register.
3. An admin can manage events.
4. Registrations are stored in Oracle.
5. Volunteer tasks are stored in Oracle.
6. CRUD works for all four core tables.
7. Related queries work.
8. Complex reports work.
9. Background processing updates registration data.
10. The web GUI uses the backend functionality.
11. The architecture clearly separates presentation, business, and data access.
12. The project can be demonstrated from beginning to end.
13. The required report and diagrams are complete.
14. The application can be installed and run from a clean environment.

---

---

# 54. Guiding Principle

This is an academic enterprise application, not a startup.

The goal is:

```text
Simple
   +
Correct
   +
Understandable
   +
Complete
   +
Demonstrable
```

A small feature that is fully implemented, tested, documented, and understood is better than a large feature that is half finished.

**Build the complete journey, not just isolated technical features.**