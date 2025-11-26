
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.formats import router as formats_router

app = FastAPI(title="WebMorph")

origins = [
    # "http://localhost:5173",
    # "http://127.0.0.1:5173",
    "https://webmorph-client-1pm63eyfs-xpydrs-projects.vercel.app",
    "https://webmorph-client.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(formats_router, prefix="/files")
app.include_router(upload_router, prefix="/files")

@app.get("/")
def root():
    return {"message": "Welcome to the File Converter API!"}
