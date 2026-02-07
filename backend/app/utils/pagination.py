"""Pagination helper utilities."""

from typing import TypeVar

T = TypeVar("T")


def paginate(items: list[T], page: int = 1, page_size: int = 20) -> list[T]:
    """Return a page slice from a list of items."""

    normalized_page = max(page, 1)
    normalized_page_size = max(page_size, 1)
    start = (normalized_page - 1) * normalized_page_size
    end = start + normalized_page_size
    return items[start:end]
