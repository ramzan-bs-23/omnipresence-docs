from django.utils.deprecation import MiddlewareMixin


class OrganizationMiddleware(MiddlewareMixin):
    """
    Middleware to attach the current user's organization to the request.
    """

    def process_request(self, request):
        if request.user.is_authenticated:
            request.organization = request.user.organization
        else:
            request.organization = None
