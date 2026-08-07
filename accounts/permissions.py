from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(check_func, message='You are not authorized to perform this action.'):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            try:
                allowed = check_func(user)
            except Exception:
                allowed = False
            if allowed:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied(message)

        return _wrapped

    return decorator


student_required = role_required(lambda u: getattr(u, 'is_student', False), 'Students only.')

teacher_required = role_required(lambda u: getattr(u, 'is_teacher', False) or getattr(u, 'is_superuser', False), 'Teachers only.')

# Librarians are modeled as staff members in this project (is_staff_member)
librarian_required = role_required(lambda u: getattr(u, 'is_staff_member', False) or getattr(u, 'is_staff', False) or getattr(u, 'is_superuser', False), 'Librarians only.')

# Combined decorator: teachers or librarians (admins allowed)
teacher_or_librarian_required = role_required(
    lambda u: bool(getattr(u, 'is_teacher', False) or getattr(u, 'is_staff_member', False) or getattr(u, 'is_staff', False) or getattr(u, 'is_superuser', False)),
    'You must be a teacher or librarian to perform this action.'
)
