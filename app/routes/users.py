from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import schemas
from app.auth.auth import get_current_user_id
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import schemas
from app.auth.auth import get_current_user_id
from app.crud import crud
from app.core.config import settings
from app.db.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me/applications", response_model=list[schemas.ApplicationOut])
def get_user_applications(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    applications = crud.get_applications_for_user(db, user_id)
    return applications


@router.post("/apply", response_model=schemas.ApplicationOut)
def apply_for_job(
    job_id: int = Form(...),
    cover_letter: str = Form(None),
    resume: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Check if job exists and is active
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.is_active:
        raise HTTPException(status_code=400, detail="Job is not active")

    # Check if user already applied
    existing_applications = crud.get_applications_for_user(db, user_id)
    for app in existing_applications:
        if app.job_id == job_id:
            raise HTTPException(status_code=400, detail="Already applied to this job")

    # Save resume file
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"user_{user_id}_job_{job_id}_{timestamp}_{resume.filename}"
    filepath = upload_dir / filename

    try:
        with open(filepath, "wb") as f:
            content = resume.file.read()
            f.write(content)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save resume")

    # Create application
    application = crud.create_application(
        db=db,
        user_id=user_id,
        job_id=job_id,
        cover_letter=cover_letter,
        resume_path=str(filepath)
    )

    return application
