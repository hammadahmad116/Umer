@echo off
REM Set the name of the virtual environment directory
set VENV_DIR=virtual_environment

REM Check if the virtual environment directory exists
if not exist %VENV_DIR% (
    echo "Creating virtual environment..."
    python -m venv %VENV_DIR%
)

REM Activate the virtual environment
call %VENV_DIR%\Scripts\activate

REM Check if all required libraries are installed
echo "Checking for required libraries..."
pip freeze > installed_packages.txt

REM Read requirements.txt and check for missing packages
set MISSING_LIBS=0
for /f "tokens=*" %%i in (requirements.txt) do (
    findstr /i "%%i" installed_packages.txt >nul
    if errorlevel 1 (
        echo "Missing library: %%i"
        set MISSING_LIBS=1
    )
)

REM Install libraries if any are missing
if %MISSING_LIBS%==1 (
    echo "Installing missing libraries..."
    pip install -r requirements.txt
)

REM Run the Streamlit app
echo "Running Streamlit app..."
streamlit run main.py

REM Pause to keep the window open
pause
