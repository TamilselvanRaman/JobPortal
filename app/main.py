from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database components
from app.db.database import engine, Base
from app.models.models import User, Company, Job, Application, SessionToken

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Job Portal API",
    version="1.0.0",
    description="A comprehensive job portal API for users and companies"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Job Portal API is running successfully! 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

# Import and include routes only if they exist
try:
    from app.routes.main import router
    app.include_router(router)
    print("✅ Routes included successfully")
except Exception as e:
    print(f"⚠️  Routes not available yet: {e}")

# Start scheduler if available
try:
    from app.tasks.scheduler import scheduler

    @app.on_event("startup")
    async def startup_event():
        if not getattr(scheduler, 'running', False):
            scheduler.start()
        print("🚀 Job Portal API started successfully!")

    @app.on_event("shutdown")
    async def shutdown_event():
        if getattr(scheduler, 'running', False):
            scheduler.shutdown()
        print("👋 Job Portal API stopped!")
except Exception:
    print("⚠️  Scheduler not available yet")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)