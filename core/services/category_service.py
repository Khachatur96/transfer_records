from sqlalchemy.orm import Session
from core.models.category import Category


class CategoryService:

    @staticmethod
    def create_category(title: str, description: str, session: Session) -> Category:
        """Create a single category."""
        category = Category(title=title, description=description)
        session.add(category)
        session.commit()
        return category

    @staticmethod
    def find_or_create_category(dev_category, prod_session: Session) -> Category:
        """Find or create a category in the PROD database."""
        existing_category = prod_session.query(Category).filter_by(id=dev_category.id).first()
        if not existing_category:
            existing_category = Category(
                id=dev_category.id,
                title=dev_category.title,
                description=dev_category.description
            )
            prod_session.add(existing_category)
            prod_session.commit()
        return existing_category
