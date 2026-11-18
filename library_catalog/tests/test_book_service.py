from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from library_catalog.api.v1.schemas.book import BookCreate
from library_catalog.domain.exceptions import (
    InvalidYearException,
)
from library_catalog.domain.services.book_service import BookService


def _future_year() -> int:
    """Год в будущем"""
    return datetime.now().year + 1


def _make_mock_book(**overrides):
    """Создать заглушку книги"""
    defaults = {
        "book_id": uuid4(),
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "genre": "Programming",
        "pages": 464,
        "available": True,
        "isbn": None,
        "description": None,
        "extra": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.mark.asyncio
async def test_create_book_success():
    """Успешное создание книги: ISBN уникален, обогащение проходит"""
    book_repo = AsyncMock()
    book_repo.find_by_isbn.return_value = None
    book_repo.create.return_value = _make_mock_book()

    ol_client = AsyncMock()
    ol_client.enrich.return_value = None

    service = BookService(book_repo, ol_client)

    book_data = BookCreate(
        title="Clean Code",
        author="Robert C. Martin",
        year=2008,
        genre="Programming",
        pages=464,
    )

    result = await service.create_book(book_data)

    book_repo.find_by_isbn.assert_not_awaited()
    ol_client.enrich.assert_awaited_once_with(
        title="Clean Code",
        author="Robert C. Martin",
        isbn=None,
    )
    book_repo.create.assert_awaited_once()
    assert result.title == "Clean Code"
    assert result.author == "Robert C. Martin"



@pytest.mark.asyncio
async def test_create_book_invalid_year_in_future():
    """Ошибка валидации года, если год в будущем"""
    book_repo = AsyncMock()
    ol_client = AsyncMock()

    service = BookService(book_repo, ol_client)

    book_data = BookCreate(
        title="Future Book",
        author="Some Author",
        year=_future_year(),
        genre="Sci-Fi",
        pages=100,
    )

    with pytest.raises(InvalidYearException):
        await service.create_book(book_data)

    book_repo.find_by_isbn.assert_not_awaited()
    book_repo.create.assert_not_awaited()
    ol_client.enrich.assert_not_awaited()
