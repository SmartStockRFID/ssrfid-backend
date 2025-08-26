from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.exception_handler import ExceptionHandler
from app.routers import auth, conferencia, peca, usuario
from app.settings import app_settings

app = FastAPI(
    title=app_settings.PROJECT_NAME,
    description=app_settings.PROJECT_DESCRIPTION,
    version=app_settings.PROJECT_VERSION,
)


# Redirecionamento padrão para /docs
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


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

ExceptionHandler.handle(app)
