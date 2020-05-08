@ECHO OFF
ECHO Starting classifier experiments...
call ..\venv\Scripts\activate.bat
python run_experiments.py 109 100 2 1 True >> run.log