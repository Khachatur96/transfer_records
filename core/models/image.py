from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
if TYPE_CHECKING:
    from .document import Document


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'))

    document: Mapped["Document"] = relationship("Document", back_populates="images")

