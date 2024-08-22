from sqlalchemy.orm import Session

from core.models.companies_categories import CompanyCategory
from core.models.company import Company
from core.models.category import Category


class CompanyService:

    @staticmethod
    def create_company(category: Category, site_url: str, title: str, description: str, session: Session) -> Company:
        """Create a single company associated with a category."""
        company = Company(
            category_id=category.id,
            site_url=site_url,
            title=title,
            description=description
        )
        session.add(company)
        session.commit()
        return company

    @staticmethod
    def find_or_create_company(dev_company, prod_session: Session) -> Company:
        """Find or create a company in the PROD database, associating it with categories."""
        existing_company = prod_session.query(Company).filter_by(site_url=dev_company.site_url).first()
        if not existing_company:
            existing_company = Company(
                title=dev_company.title,
                description=dev_company.description,
                site_url=dev_company.site_url,
                category_id=dev_company.category_id
            )
            prod_session.add(existing_company)
            prod_session.commit()

            for dev_category in dev_company.categories:
                company_category = CompanyCategory(
                    company_id=existing_company.id,
                    category_id=dev_category.id
                )
                prod_session.add(company_category)
            prod_session.commit()
        return existing_company
