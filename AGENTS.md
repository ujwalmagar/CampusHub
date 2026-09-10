# 1. Core Engineering Principle

This project must be developed with a production-quality, security-first, reliability-first mindset.

Do NOT optimize primarily for speed of implementation or a quick MVP.

Priorities, in order:

1. Security
2. Correctness
3. Data integrity
4. Reliability
5. Maintainability
6. Testability
7. Performance
8. Development speed

A fast implementation is not considered successful if it introduces security vulnerabilities, incorrect behavior, data loss, architectural problems, or significant technical debt.

Never intentionally use an insecure shortcut merely to make implementation faster.

---

# 2. Do Not Guess Requirements

Before implementing a feature:

* Read master.md and the relevant documentation in docs/.
* Inspect the existing code and architecture.
* Do not invent business requirements.
* Do not silently make assumptions when requirements are ambiguous.
* If an important requirement is unclear, ask for clarification or explicitly mark it as TBD.
* Do not implement behavior simply because it is convenient.

The documented requirements are the source of truth.

---

# 3. Production-Quality Implementation

Implement features as they should reasonably exist in a real production application, while keeping the scope appropriate for this project.

Avoid:

* throwaway implementations
* hardcoded business logic that should be configurable
* duplicated logic
* unnecessary shortcuts
* insecure temporary solutions
* fake/mock implementations presented as production functionality
* excessive technical complexity without a reason

Do not introduce production-hostile code simply because it is easier to write.

---

# 4. Security by Default

Treat all external input as untrusted.

Security must be considered for every feature and every API.

Always consider:

* authentication
* authorization
* input validation
* output handling
* access control
* data exposure
* injection attacks
* session security
* CSRF where applicable
* XSS
* SQL/NoSQL injection
* command injection
* path traversal
* SSRF where applicable
* insecure file uploads
* rate limiting
* abuse prevention
* sensitive information disclosure
* privilege escalation
* IDOR/BOLA
* race conditions
* replay attacks where relevant

Do not assume the frontend is trusted.

All security-sensitive decisions must be enforced on the server.

---

# 5. Authentication and Authorization

Authentication and authorization are separate concerns.

For every protected resource:

* Verify the user’s identity.
* Verify that the authenticated user has permission to perform the requested action.
* Never rely solely on frontend restrictions.
* Never trust role information supplied by the client.
* Apply least-privilege principles.
* Prevent users from accessing resources belonging to other users unless explicitly authorized.

Every new endpoint must explicitly consider:

* Is authentication required?
* Which roles can access it?
* Which specific resource-level permissions are required?

---

# 6. Input Validation

Validate all untrusted input at the appropriate boundary.

This includes:

* request bodies
* query parameters
* URL/path parameters
* headers where relevant
* uploaded files
* external API responses
* user-generated content

Validation must happen server-side even if the frontend already validates the same data.

Reject malformed, unexpected, or unauthorized input safely.

Do not trust client-provided:

* user IDs
* roles
* permissions
* ownership information
* prices
* status values
* security-sensitive flags

---

# 7. Database Security and Integrity

Database operations must preserve data integrity.

Use:

* appropriate constraints
* foreign keys where appropriate
* unique constraints
* transactions where required
* parameterized queries or safe ORM mechanisms
* appropriate indexes
* migrations
* appropriate data types

Never construct database queries using unsafe string concatenation with user input.

Do not delete, migrate, or modify production data destructively without explicit authorization.

Database schema changes must be reflected in docs/database.md.

---

# 8. API Security and Design

Every API endpoint must have clearly defined:

* authentication requirements
* authorization requirements
* input validation
* expected responses
* error behavior
* resource ownership rules
* rate-limiting considerations where appropriate

Do not expose:

* passwords
* password hashes
* tokens
* API keys
* internal secrets
* unnecessary personal information
* internal stack traces
* database errors
* internal implementation details

Use consistent and safe error responses.

Do not leak information through error messages unnecessarily.

API changes must be reflected in docs/api.md.

---

# 9. Secrets and Configuration

Never hardcode:

* passwords
* API keys
* tokens
* private keys
* database credentials
* encryption keys
* other secrets

Use environment variables or an appropriate secret-management mechanism.

Never commit real secrets to version control.

Do not expose server-side secrets to client-side code.

---

# 10. Error Handling

Handle errors deliberately.

Do not:

* silently swallow important errors
* expose stack traces to users
* return raw database errors
* return internal implementation details
* assume operations succeeded without verification

Errors should be:

* safe
* predictable
* useful for debugging through appropriate server-side logging
* appropriate for the API/client

---

# 11. Frontend Security

Never treat frontend code as a security boundary.

Frontend validation improves user experience but does not replace server-side validation.

Do not place secrets in frontend code.

Do not rely on hiding UI elements as authorization.

When rendering user-generated content, use appropriate escaping/sanitization mechanisms.

Avoid dangerous browser APIs unless there is a justified and safe implementation.

---

# 12. Dependencies

Before adding a dependency:

* Determine whether an existing dependency already solves the problem.
* Prefer mature and well-maintained packages.
* Avoid unnecessary dependencies.
* Use versions compatible with the project.
* Consider security and maintenance implications.

Do not add libraries simply because they make a small task slightly easier.

---

# 13. Testing

Testing is part of implementation, not an optional final step.

For important functionality, test:

* normal behavior
* invalid input
* unauthorized access
* forbidden access
* ownership boundaries
* edge cases
* failure conditions
* important business rules

Security-sensitive functionality must include appropriate security and authorization tests.

Do not only test the happy path.

---

# 14. Code Changes

Before modifying existing code:

1. Understand the existing implementation.
2. Identify dependencies and side effects.
3. Check whether the functionality already exists.
4. Determine whether the change affects the API, database, authentication, authorization, or architecture.
5. Make the smallest appropriate change.

Do not rewrite working systems unnecessarily.

Do not introduce unrelated changes while implementing a feature.

---

# 15. Documentation Synchronization

Documentation must remain consistent with the implementation.

When a change affects:

* requirements → update the relevant requirements documentation
* architecture → update docs/architecture.md
* database → update docs/database.md
* API → update docs/api.md
* security behavior → update docs/security.md
* major architectural decisions → update docs/decisions.md

Do not allow documentation to describe behavior that the application no longer implements.

---

# 16. Security Review Before Completion

Before considering a security-sensitive feature complete, review:

* authentication
* authorization
* input validation
* data exposure
* ownership checks
* injection risks
* error handling
* rate limiting where appropriate
* secret handling
* logging
* abuse scenarios
* race conditions where relevant

Ask:

“How could a malicious or unauthorized user misuse this feature?”

Do not only verify that the intended user can use the feature.

---

# 17. Never Claim Security Guarantees

No implementation should be described as:

* “100% secure”
* “vulnerability-free”
* “impossible to hack”
* “guaranteed secure”

Security is an ongoing process.

When appropriate, explicitly identify remaining risks, assumptions, limitations, and areas requiring further review.

---

# 18. No Blind Execution

Do not make large architectural, database, authentication, authorization, or security changes without first explaining the intended approach.

For significant changes:

1. Analyze the requirement.
2. Identify affected components.
3. Explain the implementation approach.
4. Identify security considerations.
5. Identify database/API/architecture implications.
6. Then implement after the approach is clear.

---

# 19. Production Over MVP

Unless explicitly instructed otherwise, do NOT choose an implementation merely because it is the fastest way to produce a working demo.

If there are multiple approaches:

* prefer the safer approach
* prefer the maintainable approach
* prefer the testable approach
* prefer the approach that preserves data integrity
* prefer established patterns over ad-hoc solutions

If a production-quality implementation is significantly more complex, explain the trade-off rather than silently implementing an insecure shortcut.

---

# 20. Final Verification

Before declaring a task complete:

* Review the changed code.
* Check for obvious security issues.
* Check authorization boundaries.
* Check input validation.
* Check error handling.
* Run relevant tests.
* Check for regressions.
* Verify documentation is synchronized.
* Clearly report anything that could not be verified.

Never claim that tests, security checks, builds, or other verification steps were performed if they were not actually performed.
