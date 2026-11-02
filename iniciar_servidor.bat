@echo off
cd /d "%~dp0"
echo Iniciando o Django em http://127.0.0.1:8000/
echo Deixe esta janela aberta. Para parar: Ctrl+C
echo.
if exist "%~dp0venv\Scripts\activate.bat" call "%~dp0venv\Scripts\activate.bat"
python manage.py runserver 127.0.0.1:8000
pause
