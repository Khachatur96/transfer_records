from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .document import Document
    from .category import Category

from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.models.base import Base


class Company(Base):
    __tablename__ = "companies"

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    site_url: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    # One-to-many relationship with Document
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="company")

    # Many-to-many relationship with Category through companies_categories
    categories: Mapped[List["Category"]] = relationship(
        "Category", secondary="companies_categories", back_populates="companies"
    )