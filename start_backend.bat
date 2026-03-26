@echo off
cd Backend
echo Starting Backend...
call venv\Scripts\activate
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
