# Installation Manual

Follow these steps to deploy and run the Campus Event & Volunteer Management System from a clean environment.

## 1. Requirements

Before starting, ensure you have the following installed on your machine:
- **Python**: Version 3.10 or higher.
- **Oracle Database**: Oracle Database 21c Express Edition (XE) or equivalent.
- **Oracle Client**: Suitable Oracle Instant Client and drivers to communicate via Python.
- **pip**: Standard Python package manager.

## 2. Environment Setup

It is highly recommended to run this Django application inside a virtual environment to prevent dependency collisions.

1. Navigate to the project root directory (`C:\College-Assignment\CampusHub` or your cloned path):
   ```bash
   cd path/to/CampusHub
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies from the `requirements.txt` file (includes Django, DRF, and Oracle drivers like `oracledb`):
   ```bash
   pip install -r requirements.txt
   ```

## 3. Oracle Database Setup

The application relies on Oracle to function. You must configure the backend user and schema.

1. Connect to your Oracle database as `SYSDBA` and create the application user (ensure you grant the necessary permissions for connection and tablespace quotas):
   ```sql
   CREATE USER c##campus_admin IDENTIFIED BY password123;
   GRANT CONNECT, RESOURCE TO c##campus_admin;
   ALTER USER c##campus_admin QUOTA UNLIMITED ON USERS;
   ```

2. Open your preferred SQL client (e.g., SQL*Plus or SQL Developer), log in as `c##campus_admin`, and execute the structural schema script:
   ```bash
   @database/schema.sql
   ```

3. (Optional) Run the Django native migrations to generate the internal framework tables (e.g., `auth_user` and `django_session`):
   ```bash
   python manage.py migrate
   ```

4. Execute the seed script to populate realistic dummy data into the business tables:
   ```bash
   @database/seed.sql
   ```

5. Confirm your `config/settings.py` file points to the correct Database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.oracle',
           'NAME': 'localhost:1521/XEPDB1',
           'USER': 'c##campus_admin',
           'PASSWORD': 'password123',
       }
   }
   ```

## 4. Running the Application

To launch the local development server, run the following command in the project root:

```bash
python manage.py runserver
```

The application will be accessible via a web browser at: **http://localhost:8000/**

## 5. Testing

The application ships with a Django automated testing suite covering API logic, authentication, and security.

To run the standard unit tests:
```bash
python manage.py test
```

### Known Oracle Test Limitation
*Note on `manage.py test`:* Django's test runner attempts to dynamically construct an isolated mirror database (`test_CampusHub`) from scratch. Due to restricted `CREATE DATABASE` / `CREATE USER` privileges commonly enforced on local Oracle XE `c##campus_admin` accounts, you may encounter an `ORA-01031: insufficient privileges` or `DPY-1001: not connected to database` failure.

**To successfully execute the comprehensive E2E Security and Regression verifications against the active development database, simply run:**
```bash
python run_e2e_live.py
```
This executes a dedicated regression and E2E script ensuring CSRF, XSS, and IDOR vulnerabilities are safely mitigated in the real environment.
