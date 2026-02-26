@echo off
REM AI Conversation Archive Search - Easy Launcher (Windows)
REM Double-click this file to start everything

echo ================================================
echo AI Conversation Archive Search
echo ================================================
echo.

REM Check if first run
if not exist config.txt (
    echo FIRST TIME SETUP
    echo ================
    echo.
    set /p VAULT_PATH="Enter path to your conversation exports: "
    echo !VAULT_PATH! > config.txt
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Try running: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed!
    echo.
    echo Indexing your conversations...
    python embed_vault.py --index
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to index conversations
        echo Check that VAULT_PATH is correct in embed_vault.py
        pause
        exit /b 1
    )
    echo.
    echo Setup complete!
    echo.
)

REM Load vault path
set /p VAULT_PATH=<config.txt

echo Starting search daemon...
echo Keep this window open while using Claude Desktop
echo.
echo Status: RUNNING
echo Vault: %VAULT_PATH%
echo.
echo Press Ctrl+C to stop
echo ================================================
echo.

python search_daemon.py

pause
