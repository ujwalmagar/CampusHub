-- CampusHub Database Queries
-- This script contains required relationship and complex reporting queries.

-- ==========================================
-- RELATIONSHIP QUERY 1: Student -> Events
-- Demonstrates: Finding all events registered for by a specific student
-- Tables Involved: students, registrations, events
-- Output: Student Name, Event Title, Event Date, Registration Status
-- ==========================================
SELECT 
    s.name AS student_name,
    e.title AS event_title,
    e.event_date,
    r.status AS registration_status
FROM 
    students s
JOIN 
    registrations r ON s.student_id = r.student_id
JOIN 
    events e ON r.event_id = e.event_id
WHERE 
    s.student_id = 1
ORDER BY 
    e.event_date DESC;


-- ==========================================
-- RELATIONSHIP QUERY 2: Event -> Students
-- Demonstrates: Finding all students registered for a specific event
-- Tables Involved: events, registrations, students
-- Output: Event Title, Student Name, Student Course, Registration Date
-- ==========================================
SELECT 
    e.title AS event_title,
    s.name AS student_name,
    s.course,
    r.registered_at
FROM 
    events e
JOIN 
    registrations r ON e.event_id = r.event_id
JOIN 
    students s ON r.student_id = s.student_id
WHERE 
    e.event_id = 1
ORDER BY 
    r.registered_at ASC;


-- ==========================================
-- RELATIONSHIP QUERY 3: Event -> Volunteer Tasks
-- Demonstrates: Finding all volunteer tasks and assigned students for an event
-- Tables Involved: events, volunteer_tasks, students
-- Output: Event Title, Task Name, Task Status, Assigned Student
-- ==========================================
SELECT 
    e.title AS event_title,
    v.task_name,
    v.task_status,
    s.name AS assigned_student
FROM 
    events e
JOIN 
    volunteer_tasks v ON e.event_id = v.event_id
JOIN 
    students s ON v.student_id = s.student_id
WHERE 
    e.event_id = 1
ORDER BY 
    v.task_status ASC, v.task_name ASC;


-- ==========================================
-- COMPLEX QUERY 1: Event Participation Report
-- Demonstrates: Aggregated report showing capacity, registration counts, 
--               and volunteer counts per event.
-- Tables Involved: events (1), registrations (2), volunteer_tasks (3)
-- Output: Event Title, Capacity, Confirmed Registrations, Available Seats, Total Volunteers
-- ==========================================
SELECT 
    e.title AS event_title,
    e.capacity,
    COALESCE(r_stats.confirmed_count, 0) AS confirmed_registrations,
    e.capacity - COALESCE(r_stats.confirmed_count, 0) AS available_seats,
    COALESCE(v_stats.volunteer_count, 0) AS total_volunteers
FROM 
    events e
LEFT JOIN (
    SELECT event_id, COUNT(*) AS confirmed_count
    FROM registrations
    WHERE status = 'CONFIRMED'
    GROUP BY event_id
) r_stats ON e.event_id = r_stats.event_id
LEFT JOIN (
    SELECT event_id, COUNT(*) AS volunteer_count
    FROM volunteer_tasks
    GROUP BY event_id
) v_stats ON e.event_id = v_stats.event_id
ORDER BY 
    e.event_date ASC;


-- ==========================================
-- COMPLEX QUERY 2: Student Participation Report
-- Demonstrates: Aggregated report showing each student's total registrations
--               and total completed volunteer tasks.
-- Tables Involved: students (1), registrations (2), volunteer_tasks (3)
-- Output: Student Name, Course, Total Events Registered, Total Completed Tasks
-- ==========================================
SELECT 
    s.name AS student_name,
    s.course,
    COUNT(DISTINCT r.registration_id) AS total_events_registered,
    COUNT(DISTINCT v.task_id) AS completed_volunteer_tasks
FROM 
    students s
LEFT JOIN 
    registrations r ON s.student_id = r.student_id
LEFT JOIN 
    volunteer_tasks v ON s.student_id = v.student_id AND v.task_status = 'COMPLETED'
GROUP BY 
    s.student_id, s.name, s.course
ORDER BY 
    total_events_registered DESC, completed_volunteer_tasks DESC;
