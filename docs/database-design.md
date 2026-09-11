# Database Design

The CampusHub application leverages a robust Oracle Database, mapping directly to our Django ORM models. Below is the detailed structure of the core database schema.

## 1. STUDENTS Table
Stores registered student users, extending the base Django authentication user.
- **id**: Primary Key (Number)
- **user_id**: Foreign Key (One-to-One mapping to `auth_user`)
- **roll_number**: Varchar, Unique constraint (Student ID)
- **program**: Varchar (Academic Program)

## 2. EVENTS Table
Stores university events created by administrators.
- **id**: Primary Key (Number)
- **title**: Varchar
- **description**: Text/CLOB
- **event_date**: Date
- **location**: Varchar
- **capacity**: Integer (Maximum number of confirmed attendees allowed)

## 3. REGISTRATIONS Table
Stores the enrollment relationship between Students and Events.
- **id**: Primary Key (Number)
- **student_id**: Foreign Key (References `STUDENTS(id)`)
- **event_id**: Foreign Key (References `EVENTS(id)`)
- **registered_at**: Timestamp
- **status**: Varchar (`CONFIRMED`, `PENDING`, `CANCELLED`)

## 4. VOLUNTEER_TASKS Table
Stores specific tasks assigned to students for specific events.
- **id**: Primary Key (Number)
- **event_id**: Foreign Key (References `EVENTS(id)`)
- **student_id**: Foreign Key (References `STUDENTS(id)`)
- **task_name**: Varchar
- **task_status**: Varchar (`PENDING`, `IN_PROGRESS`, `COMPLETED`)

---

# Key Relational Queries

These queries correspond to the required queries documented in `database/queries.sql`.

### Query 1: Find all events a specific student is registered for
**Purpose:** Populates the "My Registrations" dashboard view.
**Tables Involved:** STUDENTS, REGISTRATIONS, EVENTS
```sql
SELECT e.title, e.event_date, r.status
FROM api_event e
JOIN api_registration r ON e.id = r.event_id
JOIN api_student s ON r.student_id = s.id
WHERE s.roll_number = 'STU001';
```

### Query 2: Find all confirmed students for an event
**Purpose:** Allows admins to view active participants and print rosters.
**Tables Involved:** STUDENTS, REGISTRATIONS, EVENTS
```sql
SELECT au.first_name, au.last_name, s.roll_number
FROM auth_user au
JOIN api_student s ON au.id = s.user_id
JOIN api_registration r ON s.id = r.student_id
WHERE r.event_id = 1 AND r.status = 'CONFIRMED';
```

### Query 3: Complex Multi-Entity Query (Participation Report)
**Purpose:** Advanced reporting feature showing complete event ecosystem (Event + Registrations + Volunteer Tasks).
**Tables Involved:** EVENTS, REGISTRATIONS, VOLUNTEER_TASKS, STUDENTS
```sql
SELECT e.title,
       COUNT(DISTINCT r.id) as total_registrations,
       COUNT(DISTINCT v.id) as total_volunteers
FROM api_event e
LEFT JOIN api_registration r ON e.id = r.event_id
LEFT JOIN api_volunteertask v ON e.id = v.event_id
GROUP BY e.title;
```
