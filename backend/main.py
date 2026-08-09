from fastapi import FastAPI 
from contextlib import asynccontextmanager
from backend.database.db import database
from fastapi.middleware.cors import CORSMiddleware
from backend.auth.controllers.auth_controller import router as auth_router
from backend.Interview.controllers.interview_controller import (
    router as interview_router,
)
from backend.Resume.controllers.resume_controller import (
    router as resume_router,

)
from backend.Jobs.controllers.job_controller import router as job_router
from backend.Applications.controllers.application_controller import (
    router as application_router,

)



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect_db()
    yield
    await database.disconnect_db()


app = FastAPI(
    tile = "PlacekoV5",
    description = "This is my agentic AI application",
    lifespan=lifespan
   
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "connected"
    }



app.include_router(interview_router)



app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(job_router)
app.include_router(application_router)
