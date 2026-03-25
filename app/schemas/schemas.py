from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
	access_token: str
	token_type: str
	refresh_token: Optional[str]


class UserOut(BaseModel):
	id: int
	username: str
	email: EmailStr
	is_active: bool

	class Config:
		orm_mode = True


class CompanyOut(BaseModel):
	id: int
	company_name: str
	username: str
	email: EmailStr
	is_active: bool

	class Config:
		orm_mode = True


class AuthSignup(BaseModel):
	role: str
	username: str
	email: EmailStr
	password: str
	company_name: Optional[str]


class AuthLogin(BaseModel):
	role: str
	email: EmailStr
	password: str


class AuthResponse(BaseModel):
	role: str
	profile: Optional[UserOut | CompanyOut]
	token: Token


class JobCreate(BaseModel):
	title: str
	description: Optional[str]
	start_date: Optional[datetime]
	end_date: Optional[datetime]


class JobOut(BaseModel):
	id: int
	company_id: int
	title: str
	description: Optional[str]
	is_active: bool

	class Config:
		orm_mode = True


class ApplicationOut(BaseModel):
	id: int
	user_id: int
	job_id: int
	cover_letter: Optional[str]
	resume_path: Optional[str]
	created_at: datetime

	class Config:
		orm_mode = True

