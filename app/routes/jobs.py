from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud
from app.db.database import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("", response_model=list[schemas.JobOut])
def list_jobs(
    search: Optional[str] = None,
    company_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    from typing import Optional

    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session

    from app import schemas
    from app.crud import crud
    from app.db.database import get_db

    router = APIRouter(prefix="/jobs", tags=["Jobs"])


    @router.get("", response_model=list[schemas.JobOut])
    def list_jobs(
        search: Optional[str] = None,
        company_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
        sort: str = "desc",
        db: Session = Depends(get_db)
    ):
        if limit > 100:
            limit = 100

        sort_desc = sort.lower() != "asc"

        jobs = crud.list_jobs(
            db,
            search=search,
            company_id=company_id,
            is_active=is_active,
            skip=skip,
            limit=limit,
            sort_desc=sort_desc
        )
        return jobs


    @router.get("/{job_id}", response_model=schemas.JobOut)
    def get_job(job_id: int, db: Session = Depends(get_db)):
        job = crud.get_job(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
