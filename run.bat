@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto RUN
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto RUN
)

echo [ERROR] Python not found in PATH.
exit /b 1

:RUN
%PYTHON_CMD% main.py %*
exit /b %errorlevel%
