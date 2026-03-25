from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.models.models import User, Company, Job, Application, SessionToken
from app.utils.utils import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> Optional[User]:
	return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
	return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: str, password: str) -> User:
	hashed = hash_password(password)
	user = User(username=username, email=email, hashed_password=hashed)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user

def get_company_by_email(db: Session, email: str) -> Optional[Company]:
	return db.query(Company).filter(Company.email == email).first()

def get_company_by_username(db: Session, username: str) -> Optional[Company]:
	return db.query(Company).filter(Company.username == username).first()

def create_company(db: Session, company_name: str, username: str, email: str, password: str) -> Company:
	hashed = hash_password(password)
	company = Company(company_name=company_name, username=username, email=email, hashed_password=hashed)
	db.add(company)
	db.commit()
	db.refresh(company)
	return company

def create_session(db: Session, token: str, user_type: str, entity_id: int, expires_at: datetime) -> SessionToken:
	sess = SessionToken(token=token, user_type=user_type, entity_id=entity_id, expires_at=expires_at)
	db.add(sess)
	db.commit()
	db.refresh(sess)
	return sess

def authenticate_user(db: Session, email: str, password: str, user_type: str = "user"):
	if user_type == "user":
		user = get_user_by_email(db, email)
	else:
		user = get_company_by_email(db, email)

	if not user:
		return None
	if not verify_password(password, user.hashed_password):
		return None
	return user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
	return db.query(User).filter(User.id == user_id).first()

def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
	return db.query(Company).filter(Company.id == company_id).first()

def get_applications_for_user(db: Session, user_id: int) -> List[Application]:
	return db.query(Application).filter(Application.user_id == user_id).all()

def get_applications_for_job(db: Session, job_id: int) -> List[Application]:
	return db.query(Application).filter(Application.job_id == job_id).all()

def create_application(db: Session, user_id: int, job_id: int, cover_letter: Optional[str] = None, resume_path: Optional[str] = None) -> Application:
	application = Application(user_id=user_id, job_id=job_id, cover_letter=cover_letter, resume_path=resume_path)
	db.add(application)
	db.commit()
	db.refresh(application)
	return application

def get_job(db: Session, job_id: int) -> Optional[Job]:
	return db.query(Job).filter(Job.id == job_id).first()

def list_jobs(db: Session, search: Optional[str] = None, company_id: Optional[int] = None, is_active: Optional[bool] = None, skip: int = 0, limit: int = 20, sort_desc: bool = True) -> List[Job]:
	q = db.query(Job)
	if search:
		q = q.filter(Job.title.ilike(f"%{search}%"))
	if company_id:
		q = q.filter(Job.company_id == company_id)
	if is_active is not None:
		q = q.filter(Job.is_active == is_active)
	if sort_desc:
		q = q.order_by(Job.created_at.desc())
	else:
		q = q.order_by(Job.created_at.asc())
	return q.offset(skip).limit(limit).all()

def list_jobs_for_company(db: Session, company_id: int) -> List[Job]:
	return db.query(Job).filter(Job.company_id == company_id).all()

def create_job(db: Session, company_id: int, title: str, description: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Job:
	job = Job(company_id=company_id, title=title, description=description, start_date=start_date, end_date=end_date)
	db.add(job)
	db.commit()
	db.refresh(job)
	return job

