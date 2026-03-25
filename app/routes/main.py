from fastapi import APIRouter

from app.routes import auth, users, companies, jobs

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(companies.router)
router.include_router(jobs.router)