from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import peca

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(peca.router)
