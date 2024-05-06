@echo off
setlocal

:: Check OS and delegate to the appropriate script
if "%OS%"=="Windows_NT" (
    echo Running Windows setup...
    call windows.bat
) else (
    echo Trying to run Unix setup script...
    bash -c "chmod +x setup_unix.sh && unix.sh
)

endlocal
