@echo off

:: Check for Python 3.11 and install if not present
python --version 2>&1 | find "Python 3.11"
if %errorlevel% == 1 (
    echo Installing Python 3.11...
    powershell -Command "& {Start-Process msiexec -ArgumentList '/i https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1' -Wait}"
) else (
    echo Python 3.11 is already installed.
)

:: Install required Python packages
echo Installing required Python packages...
pip install -r requirements.txt

echo Setup completed!
