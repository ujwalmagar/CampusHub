# Security Documentation

# 13. Authentication

Authentication is a core application feature.

## Pages

```text
/login/
/signup/
/logout/
/profile/
```

## Signup

Fields:

```text
name
email
phone
course
password
password confirmation
```

Signup flow:

```text
Signup form
  ↓
Validate input
  ↓
Create Django User
  ↓
Create Student profile
  ↓
Login / redirect
```

## Login

Fields:

```text
email or username
password
```

After login:

```text
Student → Student Dashboard
Admin → Admin Dashboard
```

## Authorization

Students must not access admin management pages.

Admins can access administrative features.

Use Django authentication and permissions rather than manually checking passwords.

---

---

# 38. Security

Minimum security:

- Django password hashing
- CSRF protection
- Authentication checks
- Authorization checks
- Server-side validation
- ORM parameterization
- No plaintext passwords
- No hardcoded production secrets
- Environment variables for sensitive configuration
- Admin-only access to management functions

---