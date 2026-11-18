import pytest

from library_catalog.api.v1.schemas.book import BookCreate


def test_book_create_rejects_empty_title():
    """BookCreate не принимает пустое название книги"""
    with pytest.raises(ValueError):
        BookCreate(
            title="",
            author="Robert C. Martin",
            year=2008,
            genre="Programming",
            pages=464,
        )


def test_book_create_rejects_negative_pages():
    """BookCreate не принимает отрицательное количество страниц"""
    with pytest.raises(ValueError):
        BookCreate(
            title="Clean Code",
            author="Robert C. Martin",
            year=2008,
            genre="Programming",
            pages=-10,
        )


def test_book_create_accepts_valid_data():
    """BookCreate принимает корректные данные"""
    book = BookCreate(
        title="Clean Code",
        author="Robert C. Martin",
        year=2008,
        genre="Programming",
        pages=464,
    )
    assert book.title == "Clean Code"
    assert book.pages == 464
