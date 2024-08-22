from sqlalchemy.orm import Session
from core.models.image import Image
from core.models.document import Document
from typing import List


class ImageService:

    @staticmethod
    def create_images_for_documents(documents: List[Document], session: Session):
        """Create images for each document."""
        images = []
        for i, document in enumerate(documents):
            image1 = Image(
                document_id=document.id,
                image_url=f"https://picsum.photos/200/{i+1}.png"
            )
            image2 = Image(
                document_id=document.id,
                image_url=f"https://picsum.photos/200/{i+1}.png"
            )
            images.extend([image1, image2])
        session.add_all(images)
        session.commit()
