@echo off
title NEON SNAKE
cd /d "%~dp0"

echo Checking for pygame...
pip show pygame >nul 2>&1
if errorlevel 1 (
    echo Installing pygame...
    pip install pygame
    echo.
)

echo Starting NEON SNAKE...
python snake.py
pause
