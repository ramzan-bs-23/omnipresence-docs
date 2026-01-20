from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that returns pagination metadata in the response.
    """

    page_size = 50
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'errors': None,
            'meta': {
                'page': self.page.number,
                'per_page': self.page.paginator.per_page,
                'total': self.page.paginator.count,
            }
        })
