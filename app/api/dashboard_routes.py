from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.review import Review

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    reviews = db.query(
        Review
    ).all()

    return {
        "total_reviews": len(reviews),
        "reviews": [
            {
                "id": review.id,
                "filename": review.filename,
                "language": review.language,
                "issues_found": review.issues_found
            }
            for review in reviews
        ]
    }