from sqlalchemy.orm import Session
from typing import List

from core.models.document import Document
from core.models.company import Company
from core.models.image import Image


class DocumentService:

    @staticmethod
    def fetch_new_records(dev_session: Session):
        """Fetch all new records from the DEV database that haven't been transferred yet."""
        return dev_session.query(Document).filter_by(transferred=False).all()

    @staticmethod
    def create_documents(company: Company, num_documents: int, session: Session) -> List[Document]:
        """Create a specified number of documents associated with a company."""
        documents = []
        for i in range(num_documents):
            document = Document(
                company_id=company.id,
                file_path=f"/files/tech_doc{i + 1}.pdf",
                title=f"Tech Document {i + 1}",
                description=f"Description for Tech Document {i + 1}.",
                transferred=False,
            )
            documents.append(document)
        session.add_all(documents)
        session.commit()
        return documents

    @staticmethod
    def transfer_document(record, existing_company, prod_session: Session):
        """Transfer a single document and its associated images from DEV to PROD."""
        new_doc = Document(
            company_id=existing_company.id,
            file_path=record.file_path,
            title=record.title,
            description=record.description,
            transferred=True
        )
        prod_session.add(new_doc)
        prod_session.commit()

        for img in record.images:
            new_image = Image(
                document_id=new_doc.id,
                image_url=img.image_url
            )
            prod_session.add(new_image)
        prod_session.commit()

    @staticmethod
    def mark_document_as_transferred(record, dev_session: Session):
        """Mark a document as transferred in the DEV database."""

        record.transferred = True
        dev_session.add(record)
        dev_session.commit()
