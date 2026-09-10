# Testing Documentation

# 44. Testing Strategy

Testing must cover both individual components and complete journeys.

## Unit/Service Tests

Test:

- Student creation
- Event creation
- Registration rules
- Duplicate registration
- Full event
- Volunteer task creation
- Registration processing
- Report calculations

## API Tests

Test:

- GET
- POST
- PUT/PATCH
- DELETE
- Authentication
- Authorization
- Invalid payloads
- Not-found cases

## End-to-End Journey

At minimum test:

```text
Signup
  ↓
Login
  ↓
Browse Event
  ↓
Register
  ↓
Admin Login
  ↓
View Registration
  ↓
Assign Volunteer Task
  ↓
Process Registration
  ↓
View Report
```

---

---

# 50. Final Demonstration Script

The lecturer demonstration should follow one coherent story.

## Step 1

Show login page.

## Step 2

Create a student account.

## Step 3

Log in as student.

## Step 4

Show student dashboard.

## Step 5

Browse events.

## Step 6

Open an event.

## Step 7

Register for the event.

## Step 8

Show registration in "My Events".

## Step 9

Log out.

## Step 10

Log in as admin.

## Step 11

Show admin dashboard.

## Step 12

Create/edit an event.

## Step 13

Open event registrations.

## Step 14

Assign a volunteer task.

## Step 15

Trigger registration processing.

## Step 16

Show database-backed status update.

## Step 17

Open reports.

## Step 18

Explain the ER diagram and relationships.

## Step 19

Explain the architecture:

```text
UI
 ↓
API
 ↓
Service
 ↓
ORM
 ↓
Oracle
```

## Step 20

Show SQL scripts and project structure.

---