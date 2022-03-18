# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number


class StandardResultsOptionalPagination(StandardResultsSetPagination):
    """request.param no_page=1 returns unpaginated queryset    """
    optional_pagination_query_param = 'no_page'

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get(self.optional_pagination_query_param, 0) == "1":
            return None

        return super().paginate_queryset(queryset, request, view=view)
