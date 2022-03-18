from rest_framework.viewsets import GenericViewSet

from common.utils.pagination import StandardResultsOptionalPagination


class GenericOptionalPageViewSet(GenericViewSet):
    """
    List a queryset. If request.param no_page=1
    return view unpaginated
    """
    pagination_class = StandardResultsOptionalPagination
