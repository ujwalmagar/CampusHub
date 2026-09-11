# CampusHub - Campus Event & Volunteer Management System

## Project Overview
CampusHub is a full-stack academic project providing an automated, secure platform for universities to manage events and volunteer coordination. It eliminates manual spreadsheet-based tracking by providing a robust role-based system. Students can browse events, register instantly, and track their volunteer assignments. Administrators can manage the entire lifecycle of an event, including automated waitlist processing when capacity opens up.

## Features
- **Role-Based Dashboards:** Separate interfaces for Students and Administrators.
- **Event Management:** Admins can create, update, and monitor university events.
- **Automated Waitlisting:** Background processing evaluates total capacity vs. confirmed attendees to seamlessly promote waitlisted students.
- **Volunteer Coordination:** Admins can create tasks (e.g., "Registration Desk") and assign them to participating students.
- **Comprehensive Reporting:** Integrated tools to generate participation and waitlist reports.

## Technology Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5, Django Templates (Light UI standard)
- **Backend:** Python 3, Django, Django REST Framework (DRF)
- **Database:** Oracle Database, Django ORM

## Architecture & Database
CampusHub employs a clean 3-tier architecture separating the Presentation (Templates), Business (DRF Services), and Data Access (Django ORM) layers. 
The Oracle Database schema maps four core entities: `Students`, `Events`, `Registrations`, and `VolunteerTasks`. 

## Project Structure
```
CampusHub_Final/
├── accounts/         # User auth and profiles
├── api/              # Core business logic and REST endpoints
├── database/         # Oracle SQL initialization scripts
├── docs/             # Technical markdown documentation & UML
├── documentation/    # Final generated PDFs
├── events/           # Event management app
├── registrations/    # Registration processing app
├── report/           # Final academic markdown report
├── screenshots/      # UI captures
├── templates/        # Global HTML layouts (Light UI)
└── volunteers/       # Volunteer management app
```

## Requirements
- Python 3.10+
- Oracle Database 19c+ (or XE)
- Git (for cloning)

## Installation & Oracle Configuration
1. **Clone & Environment:**
   ```bash
   git clone https://github.com/ujwalmagar/CampusHub.git
   cd CampusHub
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Oracle Database Setup:**
   Ensure your Oracle listener is running. Use SQL Developer (or SQL*Plus) as SYSDBA to run `database/schema.sql`. This script initializes the tables and user constraints.
3. **Application Config:**
   Update your environment variables in `.env` or `config/settings.py` to match your local Oracle credentials (never commit real passwords).

## Running the Application
Apply migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`.

## Test Instructions & Demo Accounts
*Note: Demo data can be loaded via `database/seed.sql`.*
- **Admin Access:** Username `admin`, Password `admin123`
- **Student Access:** Username `alice`, Password `password123`

## Documentation Location
- **Academic Report:** `report/report.md`
- **Formatted PDF:** `documentation/CampusHub_Documentation.pdf`
- **System Architecture & Diagrams:** `docs/`
