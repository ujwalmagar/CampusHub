-- CampusHub Oracle Database Seed Script
-- Note: This script assumes that Django migrations have already populated the 
-- auth_user table with user_ids 1 through 10, or that foreign key constraints 
-- to auth_user are disabled for standalone testing.

-- Clear existing data if necessary (handled by schema.sql drop normally)

-- ==========================================
-- SEED EVENTS (5+ Events)
-- ==========================================
INSERT INTO events (title, description, event_date, location, capacity, status) 
VALUES ('Tech Symposium 2026', 'Annual technology gathering for all students.', TO_TIMESTAMP('2026-10-15 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Main Auditorium', 200, 'OPEN');

INSERT INTO events (title, description, event_date, location, capacity, status) 
VALUES ('Career Fair Fall', 'Meet top employers and startups.', TO_TIMESTAMP('2026-11-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Sports Hall', 500, 'OPEN');

INSERT INTO events (title, description, event_date, location, capacity, status) 
VALUES ('Web Dev Workshop', 'Hands-on React and Django workshop.', TO_TIMESTAMP('2026-09-20 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Lab 3', 30, 'CLOSED');

INSERT INTO events (title, description, event_date, location, capacity, status) 
VALUES ('Alumni Networking Night', 'Connect with graduated peers.', TO_TIMESTAMP('2026-08-10 18:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Campus Cafe', 100, 'COMPLETED');

INSERT INTO events (title, description, event_date, location, capacity, status) 
VALUES ('Winter Hackathon', '48-hour coding marathon.', TO_TIMESTAMP('2026-12-15 17:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Library 2nd Floor', 150, 'OPEN');


-- ==========================================
-- SEED STUDENTS (10+ Students)
-- ==========================================
INSERT INTO students (user_id, name, email, phone, course) VALUES (1, 'Alice Smith', 'alice@campus.edu', '555-0101', 'Computer Science');
INSERT INTO students (user_id, name, email, phone, course) VALUES (2, 'Bob Johnson', 'bob@campus.edu', '555-0102', 'Information Technology');
INSERT INTO students (user_id, name, email, phone, course) VALUES (3, 'Charlie Davis', 'charlie@campus.edu', '555-0103', 'Software Engineering');
INSERT INTO students (user_id, name, email, phone, course) VALUES (4, 'Diana Prince', 'diana@campus.edu', '555-0104', 'Cyber Security');
INSERT INTO students (user_id, name, email, phone, course) VALUES (5, 'Evan Wright', 'evan@campus.edu', '555-0105', 'Data Science');
INSERT INTO students (user_id, name, email, phone, course) VALUES (6, 'Fiona Clark', 'fiona@campus.edu', '555-0106', 'Computer Science');
INSERT INTO students (user_id, name, email, phone, course) VALUES (7, 'George Harris', 'george@campus.edu', '555-0107', 'Information Technology');
INSERT INTO students (user_id, name, email, phone, course) VALUES (8, 'Hannah Lee', 'hannah@campus.edu', '555-0108', 'Software Engineering');
INSERT INTO students (user_id, name, email, phone, course) VALUES (9, 'Ian Miller', 'ian@campus.edu', '555-0109', 'Cyber Security');
INSERT INTO students (user_id, name, email, phone, course) VALUES (10, 'Julia Moore', 'julia@campus.edu', '555-0110', 'Data Science');


-- ==========================================
-- SEED REGISTRATIONS (15+ Registrations)
-- ==========================================
-- Tech Symposium Registrations
INSERT INTO registrations (student_id, event_id, status) VALUES (1, 1, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (2, 1, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (3, 1, 'PENDING');
INSERT INTO registrations (student_id, event_id, status) VALUES (4, 1, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (5, 1, 'CANCELLED');

-- Career Fair Fall Registrations
INSERT INTO registrations (student_id, event_id, status) VALUES (1, 2, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (6, 2, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (7, 2, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (8, 2, 'PENDING');

-- Web Dev Workshop Registrations
INSERT INTO registrations (student_id, event_id, status) VALUES (2, 3, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (9, 3, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (10, 3, 'CONFIRMED');

-- Alumni Networking Night
INSERT INTO registrations (student_id, event_id, status) VALUES (3, 4, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (4, 4, 'CONFIRMED');

-- Winter Hackathon Registrations
INSERT INTO registrations (student_id, event_id, status) VALUES (5, 5, 'PENDING');
INSERT INTO registrations (student_id, event_id, status) VALUES (6, 5, 'CONFIRMED');
INSERT INTO registrations (student_id, event_id, status) VALUES (1, 5, 'PENDING');


-- ==========================================
-- SEED VOLUNTEER TASKS (8+ Tasks)
-- ==========================================
-- Tech Symposium Volunteers
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (1, 1, 'Registration Desk Setup', 'COMPLETED');
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (1, 2, 'Guest Speaker Escort', 'ASSIGNED');
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (1, 4, 'Lunch Catering Coordination', 'IN_PROGRESS');

-- Career Fair Fall Volunteers
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (2, 6, 'Company Booth Setup', 'IN_PROGRESS');
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (2, 7, 'Welcome Banner Placement', 'COMPLETED');

-- Web Dev Workshop Volunteers
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (3, 9, 'Network Cabling', 'COMPLETED');

-- Winter Hackathon Volunteers
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (5, 6, 'Midnight Snack Distribution', 'ASSIGNED');
INSERT INTO volunteer_tasks (event_id, student_id, task_name, task_status) VALUES (5, 1, 'Wi-Fi Troubleshooting Support', 'ASSIGNED');

COMMIT;
