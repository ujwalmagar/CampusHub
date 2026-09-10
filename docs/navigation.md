# Application Navigation

The Campus Event & Volunteer Management System provides dynamically rendered interfaces utilizing Django Templates. Access is strictly divided between regular Students and Staff/Administrators.

## Student Navigation Flow

```text
Landing Page
 │
 ├─ Signup (Create new account and Student Profile)
 │
 └─ Login (Authenticate via credentials)
     │
     └─ Student Dashboard (`/accounts/dashboard/`)
         │
         ├─ Browse Events (`/events/`)
         │   └─ Event Details (`/events/<id>/`)
         │       └─ Register (`POST /api/registrations/`)
         │
         ├─ My Registrations (`/students/registrations/`)
         │   └─ Cancel Registration (`DELETE /api/registrations/<id>/`)
         │
         ├─ Volunteer Tasks (`/volunteers/student/`)
         │   └─ Update Status (`POST /volunteers/update-task/<id>/`)
         │
         ├─ Profile (`/accounts/profile/`)
         │
         └─ Logout (`/accounts/logout/`)
```

## Administrator Navigation Flow

```text
Login
 │
 └─ Admin Dashboard (`/accounts/dashboard/`)
     │
     ├─ Quick Actions: Manage Students
     │
     ├─ Quick Actions: Manage Events (`/events/manage/`)
     │   ├─ Create Event (`/events/create/`)
     │   ├─ Edit Event (`/events/<id>/edit/`)
     │   └─ Delete/Cancel Event (`/events/<id>/delete/`)
     │
     ├─ Quick Actions: Manage Volunteer Tasks (`/volunteers/manage/`)
     │   ├─ Assign Task (`/volunteers/create/`)
     │   ├─ Update Task (`/volunteers/<id>/edit/`)
     │   └─ Delete Task (`/volunteers/<id>/delete/`)
     │
     ├─ Process Waitlist (`POST /api/registrations/process/` via Background Sync)
     │
     ├─ View Reports (`/reports/`)
     │
     └─ Logout (`/accounts/logout/`)
```
