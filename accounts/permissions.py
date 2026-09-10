from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None, redirect_field_name='next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is a staff member,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def student_required(function=None, redirect_field_name='next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is a standard user (student),
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
