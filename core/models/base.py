from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    declared_attr,
    DeclarativeBase,
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
