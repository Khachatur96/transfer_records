from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .company import Company


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)

    companies: Mapped[List["Company"]] = relationship(
        "Company", secondary="companies_categories", back_populates="categories"
    )
