from typing import List, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .image import Image

if TYPE_CHECKING:
    from .company import Company


class Document(Base):
    __tablename__ = "documents"

    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))
    file_path: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    company: Mapped["Company"] = relationship("Company", back_populates="documents")

    images: Mapped[List["Image"]] = relationship("Image", back_populates="document", cascade="all, delete-orphan")
    transferred: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

