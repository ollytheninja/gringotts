from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin as UpstreamLoginRequiredMixin


class LoginRequiredMixin(UpstreamLoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.authz_was_checked = "LoginRequired"
        return response


def mark_checked(view_func, module):
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response.authz_was_checked = module
        return response

    return wrapped_view


def superuser_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    check_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    return mark_checked(check_decorator(function), "superuser_required")


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    check_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    return mark_checked(check_decorator(function), "login_required")


def require_no_authz(view_func):
    """
    Mark a view function as excluded from Authz Enforcement.
    """
    return mark_checked(view_func, "requite_no_authz")
