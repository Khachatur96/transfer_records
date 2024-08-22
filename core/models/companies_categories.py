from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from core.models.base import Base


class CompanyCategory(Base):
    __tablename__ = "companies_categories"

    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), primary_key=True)
