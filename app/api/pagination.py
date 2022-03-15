from rest_framework.pagination import (
    LimitOffsetPagination,
)

class ArticleLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10