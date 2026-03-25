from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.auth.auth import get_current_company_id
from app.crud import crud
from app.db.database import get_db

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/jobs", response_model=schemas.JobOut, status_code=201)
def create_job(
    payload: schemas.JobCreate,
    company_id: int = Depends(get_current_company_id),
    db: Session = Depends(get_db)
):
    return crud.create_job(
        db,
        company_id=company_id,
        title=payload.title,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date
    )

@router.get("/jobs", response_model=list[schemas.JobOut])
def get_company_jobs(
    company_id: int = Depends(get_current_company_id),
    db: Session = Depends(get_db)
):
    return crud.list_jobs_for_company(db, company_id)

@router.get("/jobs/{job_id}/applications", response_model=list[schemas.ApplicationOut])
def get_job_applications(
    job_id: int,
    company_id: int = Depends(get_current_company_id),
    db: Session = Depends(get_db)
):
    job = crud.get_job(db, job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Job not found or access denied")
    
    return crud.get_applications_for_job(db, job_id)