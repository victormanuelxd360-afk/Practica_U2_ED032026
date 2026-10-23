@echo off
setlocal
cd /d "%~dp0"
java -jar "Listas.jar"
if errorlevel 1 pause
