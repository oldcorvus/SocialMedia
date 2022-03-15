from rest_framework.pagination import (
    LimitOffsetPagination,
)


class ArticleLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10

class BookmarkLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 30
