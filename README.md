# Campus Event & Volunteer Management System

## Overview
This is a full-stack academic project built using Python, Django, Django REST Framework, and Oracle Database. It provides an automated, secure platform for students to browse and register for university events, while allowing administrators to manage capacities, allocate volunteer tasks, and resolve waitlists through background asynchronous processes.

## Documentation
- **Architecture & Design:** See the `docs/` folder for ER diagrams, class diagrams, and database structures.
- **Academic Report:** The final submission report is located at `report/report.md`.
- **Manuals:** 
  - `report/docs/user-manual.md` (Workflow Guide)
  - `report/docs/installation-manual.md` (Deployment & Setup)

## Setup
To launch this project:
1. Initialize a Python virtual environment (`python -m venv venv`).
2. Install dependencies (`pip install -r requirements.txt`).
3. Set up the `c##campus_admin` Oracle database and execute the SQL scripts in the `database/` directory (`schema.sql` then `seed.sql`).
4. Run the development server (`python manage.py runserver`).

*For full instructions, refer to the Installation Manual.*
