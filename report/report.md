---
title: "CampusHub - Campus Event & Volunteer Management System"
author: "Ujwal Magar"
date: "2026-09-11"
subject: "Enterprise Application Development / DBMS Project"
---

# COVER PAGE

**Project Name:** CampusHub - Campus Event & Volunteer Management System
**Course:** Enterprise Application Development / DBMS Project
**Technology Stack:** Python, Django, Oracle Database, Bootstrap

---

# TABLE OF CONTENTS
1. [Overview](#overview)
2. [System Proposal](#system-proposal)
3. [Technologies and Web Components](#technologies-and-web-components)
4. [Project Plan](#project-plan)
5. [UML Diagrams](#uml-diagrams)
6. [System Architecture](#system-architecture)
7. [Application Layers](#application-layers)
8. [Database Design](#database-design)
9. [ER Diagram](#er-diagram)
10. [API and Business Logic](#api-and-business-logic)
11. [Testing](#testing)
12. [User Manual](#user-manual)
13. [Application Installation Manual](#application-installation-manual)
14. [Application Screenshots](#application-screenshots)
15. [Assignment Requirement Traceability](#assignment-requirement-traceability)
16. [Conclusion](#conclusion)

---

## 1. Overview <a name="overview"></a>
CampusHub is a comprehensive university management web application that streamlines event registration and volunteer coordination. It replaces manual spreadsheet-based tracking with an automated, role-based system. Core features include student registration, event capacity management, background waitlist processing, and administrative reporting.

## 2. System Proposal <a name="system-proposal"></a>
**Problem:** Managing campus events manually leads to overbooking, miscommunication with volunteers, and administrative overhead.
**Proposed Solution:** CampusHub provides a centralized platform. Students can browse events, register instantly, and track assigned volunteer tasks. Administrators can manage the entire lifecycle of an event, including automated waitlist processing when capacity opens up.

## 3. Technologies and Web Components <a name="technologies-and-web-components"></a>
- **Frontend:** Django Templates, HTML5, CSS3, Bootstrap 5. Used to construct the Light UI design system.
- **Backend:** Python 3, Django, Django REST Framework (DRF). Handles HTTP requests, view logic, and RESTful API endpoints.
- **Database:** Oracle Database, interfaced via the Django ORM for secure data persistence.

## 4. Project Plan <a name="project-plan"></a>
1. **Requirement Analysis:** Defined user roles (Student, Admin) and entity relationships.
2. **Database Design:** Created schema for Students, Events, Registrations, and Volunteer Tasks.
3. **Backend Development:** Implemented Django models, views, and DRF endpoints.
4. **Frontend Development:** Built the Light UI and dashboard interfaces using Bootstrap.
5. **Background Processing:** Implemented the async registration processor.
6. **Testing & Polish:** Final QA and UI consistency audits.

## 5. UML Diagrams <a name="uml-diagrams"></a>
*(Refer to `docs/class-diagram.md` for full Mermaid diagrams)*
The system implements a Class Diagram modeling the `Student`, `Event`, `Registration`, and `VolunteerTask` entities. A Sequence Diagram illustrates the HTTP POST request flow during event registration, routing through the Presentation, Service, and Data Access layers.

## 6. System Architecture <a name="system-architecture"></a>
*(Refer to `docs/architecture.md`)*
The application utilizes a classic 3-tier web architecture. The presentation layer handles templating; the API/Business layer handles capacity rules; the Data Access layer manages transactions with the Oracle Database.

## 7. Application Layers <a name="application-layers"></a>
- **Presentation Layer:** Contains Django HTML templates utilizing CSS variables for styling.
- **API / View Layer:** Django views authenticate users and route actions (e.g., `event_list`, `manage_volunteers`).
- **Business / Service Layer:** Contains core rules (e.g., if total confirmed >= capacity, assign PENDING status).
- **Data Access Layer:** Uses Django's `QuerySet` API to interface securely with Oracle, preventing SQL injection.

## 8. Database Design <a name="database-design"></a>
*(Refer to `docs/database-design.md`)*
Key tables:
- `api_student`: Extends user auth.
- `api_event`: Core event details and capacity.
- `api_registration`: Links students to events with `status`.
- `api_volunteertask`: Assigns roles to students.

## 9. ER Diagram <a name="er-diagram"></a>
*(Refer to `docs/er-diagram.md`)*
Students have a one-to-many relationship with Registrations and Tasks. Events have a one-to-many relationship with Registrations and Tasks.

## 10. API and Business Logic <a name="api-and-business-logic"></a>
**CRUD Operations:** Fully implemented for Events, Registrations, and Tasks via standard HTTP verbs mapped to Django views.
**Background Processing:** The `Process Pending Registrations` tool calculates remaining capacity (`total_capacity - confirmed_count`) and automatically promotes `PENDING` waitlisted students to `CONFIRMED` in chronological order.

## 11. Testing <a name="testing"></a>
Manual E2E and visual regression testing was prioritized due to environmental constraints with headless browser agents. The application passes all core UI/UX consistency checks.

## 12. User Manual <a name="user-manual"></a>
1. **Signup/Login:** Navigate to `/accounts/login/` to authenticate.
2. **Dashboard:** View registration counts and upcoming events.
3. **Event Registration:** Browse `/events/`, click an event, and confirm registration.
4. **My Registrations:** Check waitlist status under the Registrations tab.

## 13. Application Installation Manual <a name="application-installation-manual"></a>
1. Extract `CampusHub_Final_Submission.zip`.
2. Ensure Python 3.13 and Oracle Database are installed.
3. Create a virtual environment: `python -m venv venv` and activate it.
4. Install dependencies: `pip install -r requirements.txt`.
5. Execute `database/schema.sql` in Oracle to build tables.
6. Configure Oracle connection in `CampusHub/settings.py` or `.env`.
7. Run `python manage.py runserver`.

## 14. Application Screenshots <a name="application-screenshots"></a>
*(Screenshots captured via automated Playwright pipeline)*
- Figure 14.1: Student Login (`screenshots/01_student_login.png`)
- Figure 14.2: Student Dashboard (`screenshots/03_student_dashboard.png`)
- Figure 14.3: Admin Dashboard (`screenshots/12_admin_dashboard.png`)
- Figure 14.4: Registration Processing (`screenshots/17_process_pending_registrations.png`)

## 15. Assignment Requirement Traceability <a name="assignment-requirement-traceability"></a>
| Requirement | Implementation | Evidence |
|---|---|---|
| Python Web App | Django | Source code |
| Oracle Database | Django ORM + Oracle schema | `database/schema.sql` |
| 3 Linked Tables | Students, Events, Registrations | ER Diagram |
| ORM / API | Django Models | `api/models.py` |
| Background Task | Registration Queue Processor | Admin Dashboard UI |
| Complex Queries | Participation Report | `docs/database-design.md` |

## 16. Conclusion <a name="conclusion"></a>
CampusHub successfully fulfills the requirements of an enterprise-grade university event management system, leveraging Python, Django, and Oracle.
