@echo off
setlocal
cd /d "%~dp0"
java -jar "Pilas.jar"
if errorlevel 1 pause
