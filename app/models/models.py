from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(128), unique=True, index=True, nullable=False)
	email = Column(String(256), unique=True, index=True, nullable=False)
	hashed_password = Column(String(256), nullable=False)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=datetime.utcnow)


class Company(Base):
	__tablename__ = "companies"

	id = Column(Integer, primary_key=True, index=True)
	company_name = Column(String(256), nullable=False)
	username = Column(String(128), unique=True, index=True, nullable=False)
	email = Column(String(256), unique=True, index=True, nullable=False)
	hashed_password = Column(String(256), nullable=False)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=datetime.utcnow)


class Job(Base):
	__tablename__ = "jobs"

	id = Column(Integer, primary_key=True, index=True)
	company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
	title = Column(String(256), nullable=False)
	description = Column(Text, nullable=True)
	start_date = Column(DateTime, nullable=True)
	end_date = Column(DateTime, nullable=True)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=datetime.utcnow)

	company = relationship("Company", backref="jobs")


class Application(Base):
	__tablename__ = "applications"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
	cover_letter = Column(Text, nullable=True)
	resume_path = Column(String(512), nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow)

	user = relationship("User")
	job = relationship("Job")


class SessionToken(Base):
	__tablename__ = "session_tokens"

	id = Column(Integer, primary_key=True, index=True)
	token = Column(String(512), unique=True, index=True, nullable=False)
	user_type = Column(String(32), nullable=False)  # "user" or "company"
	entity_id = Column(Integer, nullable=False)
	expires_at = Column(DateTime, nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow)
