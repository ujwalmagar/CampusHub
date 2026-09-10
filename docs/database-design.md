# Database Design

This document details the Oracle relational database design that acts as the persistence layer for the Campus Event & Volunteer Management System.

The application manages data through four primary domain tables mapped identically to Django models: `students`, `events`, `registrations`, and `volunteer_tasks`.

## 1. STUDENTS Table
Stores the profile and contact details of users registered as students.

- **Purpose:** Tracks student participants.
- **Primary Key:** `student_id` (Number/Identity)
- **Foreign Keys:** `user_id` (References the Django internal `auth_user` table)
- **Important Columns:**
  - `name`: Full string name.
  - `email`: Must be unique constraint.
  - `phone`, `course`: String data.
- **Relationships:**
  - 1-to-N with `registrations` (A student can register for multiple events).
  - 1-to-N with `volunteer_tasks` (A student can volunteer for multiple tasks).

## 2. EVENTS Table
Stores the institutional events that are open for registration.

- **Purpose:** Acts as the central anchor for scheduling, capacities, and task delegation.
- **Primary Key:** `event_id` (Number/Identity)
- **Important Columns:**
  - `title`, `description`, `location`: String details.
  - `event_date`: Timestamp for scheduling.
  - `capacity`: Numeric maximum capacity.
  - `status`: String state.
- **Constraints:**
  - Check Constraint: `capacity > 0`
  - Check Constraint: `status IN ('OPEN', 'CLOSED', 'COMPLETED', 'CANCELLED')`
- **Relationships:**
  - 1-to-N with `registrations` (An event hosts multiple registrations).
  - 1-to-N with `volunteer_tasks` (An event requires multiple volunteer assignments).

## 3. REGISTRATIONS Table
Associative entity (join table) resolving the Many-to-Many relationship between Students and Events.

- **Purpose:** Tracks the enrollment status of a specific student in a specific event.
- **Primary Key:** `registration_id` (Number/Identity)
- **Foreign Keys:**
  - `student_id` (References `students.student_id`, ON DELETE CASCADE)
  - `event_id` (References `events.event_id`, ON DELETE CASCADE)
- **Important Columns:**
  - `status`: Enrollment state.
- **Constraints:**
  - Unique Constraint: `(student_id, event_id)` — A student can only register for a given event once.
  - Check Constraint: `status IN ('PENDING', 'CONFIRMED', 'CANCELLED')`

## 4. VOLUNTEER_TASKS Table
Associative entity tracking operational responsibilities assigned to students during events.

- **Purpose:** Allows Admins to assign specific logistical tasks to students on a per-event basis.
- **Primary Key:** `task_id` (Number/Identity)
- **Foreign Keys:**
  - `student_id` (References `students.student_id`, ON DELETE CASCADE)
  - `event_id` (References `events.event_id`, ON DELETE CASCADE)
- **Important Columns:**
  - `task_name`: Title of the duty.
  - `task_status`: Progress marker.
- **Constraints:**
  - Check Constraint: `task_status IN ('ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')`
