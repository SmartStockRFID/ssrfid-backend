from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, conferencia, peca, usuario

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(peca.router)
app.include_router(usuario.router)
app.include_router(conferencia.router)
