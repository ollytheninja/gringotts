import logging

from django.http import HttpRequest, HttpResponseServerError

from project import settings

logger = logging.getLogger(getattr(settings, 'LOG_NAME', 'django'))
logger.setLevel(logging.DEBUG)

PATH_ALLOWLIST = [
    '/media',
    '/static',
    '/admin',
]


class RequireAuthzMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path = request.path
        response = self.get_response(request)

        path_allowlisted = False
        for prefix in PATH_ALLOWLIST:
            if path.startswith(prefix):
                path_allowlisted = True

        if not path_allowlisted:
            if hasattr(response, "authz_was_checked"):
                if settings.DEBUG:
                    if type(response.authz_was_checked) == str:
                        logger.info(f"Authz was checked on {path} by {response.authz_was_checked}")
                    else:
                        logger.info(f"Authz was checked on {path}")
            else:
                if settings.DEBUG:
                    logger.warning(f"Authz was not checked for {path}")
                else:
                    return AuthzNotCheckedResponse()

        return response


class AuthzNotCheckedResponse(HttpResponseServerError):
    pass
