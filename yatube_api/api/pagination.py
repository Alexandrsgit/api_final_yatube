from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    """Кастомный класс пагинации для вывода постов."""

    page_size = 10
