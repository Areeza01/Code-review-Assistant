import os
import shutil

from fastapi import APIRouter
from fastapi import UploadFile

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

@router.post("/upload")
async def upload_code(file: UploadFile):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "filename": file.filename,
        "status": "uploaded"
    }