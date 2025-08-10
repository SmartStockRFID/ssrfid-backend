@echo off
REM Comando para rodar o servidor FastAPI localmente
cd /d %~dp0\app
..\venv\Scripts\python.exe -m uvicorn main:app --reload
