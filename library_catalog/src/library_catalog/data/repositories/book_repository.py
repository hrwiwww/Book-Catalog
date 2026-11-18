from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repository import BaseRepository
from ..models.book import Book


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

    def _apply_filters(
        self,
        query,
        title: str | None = None,
        author: str | None = None,
        genre: str | None = None,
        year: int | None = None,
        available: bool | None = None,
    ):
        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.where(Book.author.ilike(f"%{author}%"))
        if genre:
            query = query.where(Book.genre.ilike(f"%{genre}%"))
        if year is not None:
            query = query.where(Book.year == year)
        if available is not None:
            query = query.where(Book.available == available)
        return query

    async def find_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
            limit: int = 20,
            offset: int = 0,
    ) -> list[Book]:
        """Поиск книг с фильтрацией."""
        query = select(Book)
        query = self._apply_filters(
            query,
            title=title,
            author=author,
            genre=genre,
            year=year,
            available=available,
        )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        result = await self.session.execute(
            select(Book).where(Book.isbn == isbn)
        )
        return result.scalar_one_or_none()

    async def count_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
    ) -> int:
        """Подсчитать количество книг по фильтрам."""
        query = select(func.count(Book.book_id))
        query = self._apply_filters(
            query,
            title=title,
            author=author,
            genre=genre,
            year=year,
            available=available,
        )
        result = await self.session.execute(query)
        return result.scalar_one()
