@ECHO OFF
ECHO Starting BCI application...
call ..\venv\Scripts\activate.bat
python main.py >> run_logs.txt