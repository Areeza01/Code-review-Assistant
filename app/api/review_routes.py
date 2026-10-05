import os

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.review import Review

from app.services.code_analyzer import (
    analyze_python,
    analyze_javascript
)

from app.services.ai_agent import (
    generate_review
)

router = APIRouter()


@router.post("/review")
async def review_code(
    filename: str,
    db: Session = Depends(get_db)
):

    path = f"uploads/{filename}"

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        code = f.read()

    findings = []

    language = "Unknown"

    if filename.endswith(".py"):

        language = "Python"

        findings = analyze_python(
            code
        )

    elif filename.endswith(".js"):

        language = "JavaScript"

        findings = analyze_javascript(
            code
        )

    report = generate_review(
        code,
        findings
    )

    review = Review(
        filename=filename,
        language=language,
        issues_found=len(findings),
        review_report=report
    )

    db.add(review)

    db.commit()

    return {
        "filename": filename,
        "language": language,
        "issues": findings,
        "report": report
    }