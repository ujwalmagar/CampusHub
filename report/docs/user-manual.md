# User Manual

Welcome to the Campus Event & Volunteer Management System. This platform allows students to seamlessly discover and register for university events, while empowering staff members to effortlessly coordinate volunteers and manage capacities.

---

## 1. Student Guide

### 1.1 Account Creation & Signup
1. Navigate to the application root URL (e.g. `http://localhost:8000/`).
2. Click **Sign Up** from the navigation bar or welcome page.
3. Provide your Username, Password, Full Name, Email, Phone, and Course.
4. Submit to create your Student profile.

### 1.2 Login & Dashboard
1. Use the **Login** link to authenticate with your Username and Password.
2. Upon successful login, you will land on the **Student Dashboard**.
3. Here, you will see a personalized overview of your total registrations, confirmed attendances, and any volunteer tasks assigned to you.

### 1.3 Browse and Register for Events
1. From the navigation bar or dashboard, click **Browse Events**.
2. Click **View Details** on any event card to see description, location, date, capacity, and current status.
3. Click the **Register** button. 
4. *Note:* If the event is full, you will be placed in a `PENDING` waitlist state.

### 1.4 Manage Your Registrations
1. Click **My Registrations** in the navigation bar to see a list of all your event enrollments.
2. If you can no longer attend an event, click the **Cancel** button next to the registration to free up a seat for others.

### 1.5 Manage Volunteer Tasks
1. If an Administrator assigns you a task, it will appear under the **Volunteer Tasks** section of your dashboard.
2. Click **Update Task**.
3. Use the dropdown to update the status to `IN_PROGRESS` when you begin, and `COMPLETED` when you finish.

### 1.6 Profile & Logout
1. Click **Profile** in the top navigation to view your immutable academic contact data.
2. Click **Logout** at any time to securely end your session.

---

## 2. Administrator Guide

### 2.1 Login
1. Administrators utilize the standard **Login** form.
2. Ensure your account is flagged with `is_staff` privileges (typically created via `python manage.py createsuperuser`).

### 2.2 Admin Dashboard
1. The **Admin Dashboard** displays high-level system aggregates: Total Students, Total Events, Total Registrations, and Total Volunteer Tasks.
2. The central panel displays all Waitlisted (`PENDING`) registrations across all events.

### 2.3 Manage Students
1. Currently handled seamlessly through native integration; user data is viewable through the core Reports section.

### 2.4 Manage Events
1. In the Quick Actions panel, click **Manage Events**.
2. **Create:** Click `Add New Event`, fill out the title, description, time, location, and total seat capacity.
3. **Edit/Cancel:** Click an existing event to update its details or completely Cancel it (soft delete).

### 2.5 Manage Volunteer Tasks
1. In the Quick Actions panel, click **Manage Volunteer Tasks**.
2. **Assign:** Select a Student, select an Event, and describe the logistical duty (e.g., "Set up banners").
3. Admins can manually override and edit a task's progress status if a student forgets to mark it complete.

### 2.6 Process Pending Registrations
1. If users canceled their attendance, seats open up. 
2. On the Admin Dashboard, locate the "Pending Registrations" panel and click **Process Queue**.
3. A background process will safely resolve the waitlist, upgrading `PENDING` students to `CONFIRMED` in chronological order until the newly opened capacity is filled.

### 2.7 View Reports
1. Click **View Reports** in the dashboard header.
2. The reports page outputs aggregated cross-table data, demonstrating Event Participation loads and overarching Student volunteer engagement metrics.
