from typing import Optional, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from fastapi import FastAPI


from core.database import DevSession, ProdSession
from core.models.document import Document
from core.services.category_service import CategoryService
from core.services.company_service import CompanyService
from core.services.document_service import DocumentService
from core.services.image_service import ImageService

app = FastAPI()


def populate_dev_database(session: Optional[Union[DevSession, ProdSession]]):
    """Populate the DEV database with test data."""
    category = CategoryService.create_category("Technology", "Tech companies", session)
    company = CompanyService.create_company(
        category=category,
        site_url="https://techcompany.com",
        title="Tech Company",
        description="A leading technology company.",
        session=session
    )

    documents = DocumentService.create_documents(company, 100, session)
    ImageService.create_images_for_documents(documents, session)
    print("Database populated with 100 documents, each with associated images.")


def transfer_documents():
    dev_session = DevSession()
    prod_session = ProdSession()

    try:
        new_records = DocumentService.fetch_new_records(dev_session)
        print(f"Found {len(new_records)} new records to transfer.")
        if new_records:
            for record in new_records:
                existing_record = prod_session.query(Document).filter_by(file_path=record.file_path).first()
                if not existing_record:
                    dev_company = record.company
                    for dev_category in dev_company.categories:
                        CategoryService.find_or_create_category(dev_category, prod_session)
                    existing_company = CompanyService.find_or_create_company(dev_company, prod_session)
                    DocumentService.transfer_document(record, existing_company, prod_session)

                # Debugging print to ensure this is reached
                print(f"Marking document {record.id} as transferred.")
                DocumentService.mark_document_as_transferred(record, dev_session)

            print(f"Transferred {len(new_records)} new records from DEV to PROD.")
        else:
            print("No new records to transfer.")

    except Exception as e:
        dev_session.rollback()
        prod_session.rollback()
        print(f"An error occurred: {e}")

    finally:
        dev_session.close()
        prod_session.close()


scheduler = BlockingScheduler()
scheduler.add_job(transfer_documents, 'interval', seconds=10)

if __name__ == "__main__":
    # populate_dev_database() # populate databases (dev and prod) with some data
    transfer_documents()
    scheduler.start()
