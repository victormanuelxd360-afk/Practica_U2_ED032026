@echo off
setlocal
cd /d "%~dp0"
java -jar "Colas.jar"
if errorlevel 1 pause
