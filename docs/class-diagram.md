# UML Class Diagram

This diagram represents the actual Django ORM domain models implemented in the core API application.

```mermaid
classDiagram
    class Student {
        +Integer id
        +String user
        +String roll_number
        +String program
        +__str__() String
    }
    class Event {
        +Integer id
        +String title
        +String description
        +Date event_date
        +String location
        +Integer capacity
        +__str__() String
        +get_confirmed_count() Integer
    }
    class Registration {
        +Integer id
        +Student student
        +Event event
        +DateTime registered_at
        +String status
        +__str__() String
    }
    class VolunteerTask {
        +Integer id
        +Event event
        +Student student
        +String task_name
        +String task_status
        +__str__() String
    }

    Student "1" -- "*" Registration : makes
    Student "1" -- "*" VolunteerTask : assigned to
    Event "1" -- "*" Registration : receives
    Event "1" -- "*" VolunteerTask : has
```

# UML Sequence Diagram — Event Registration

This sequence demonstrates how a student successfully registers for an event, interacting with the Presentation, View, Service, and Data Access layers.

```mermaid
sequenceDiagram
    actor Student
    participant Browser as Web UI
    participant View as API View
    participant Service as Registration Service
    participant ORM as Django ORM
    participant DB as Oracle Database

    Student->>Browser: Click "Register" on Event
    Browser->>View: POST /api/registrations/ {event_id}
    View->>Service: handle_registration(student, event_id)
    Service->>ORM: get(Event, id=event_id)
    ORM->>DB: SELECT * FROM events
    DB-->>ORM: Event Data
    ORM-->>Service: Event Object
    
    Service->>ORM: count(Registration, status='CONFIRMED')
    ORM->>DB: SELECT COUNT(*)
    DB-->>ORM: Count
    ORM-->>Service: Current Registrations
    
    alt Under Capacity
        Service->>ORM: create(status='CONFIRMED')
    else Over Capacity
        Service->>ORM: create(status='PENDING')
    end
    
    ORM->>DB: INSERT INTO registrations
    DB-->>ORM: Success
    ORM-->>Service: Registration Object
    Service-->>View: Success Response
    View-->>Browser: Redirect/Update UI
    Browser-->>Student: Display Status Badge
```

# UML Activity Diagram — Background Waitlist Processing

This demonstrates the core asynchronous background operation triggered by administrators to process the waitlist queue.

```mermaid
activityDiagram
    start
    :Admin clicks "Process Queue";
    :POST /api/registrations/process/;
    :Trigger Background Task;
    
    :Retrieve All Future Events;
    while (More Events?) is (yes)
        :Calculate Remaining Capacity\n(Total - Confirmed);
        if (Remaining Capacity > 0) then (yes)
            :Retrieve PENDING Registrations\n(Ordered by registered_at);
            while (Remaining Capacity > 0 && More Pending?) is (yes)
                :Update Registration Status to CONFIRMED;
                :Decrement Remaining Capacity;
            endwhile (no)
        else (no)
            :Skip Event;
        endif
    endwhile (no)
    
    :Commit Transaction to Oracle DB;
    :Return Success;
    stop
```
