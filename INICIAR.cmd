@echo off
setlocal
cd /d "%~dp0"
where java >nul 2>nul
if errorlevel 1 (
  echo Se requiere Java 21 o posterior instalado y agregado al PATH.
  pause
  exit /b 1
)
java -jar "Practica_U2.jar"
if errorlevel 1 pause
