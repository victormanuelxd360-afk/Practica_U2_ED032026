@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0herramientas\probar-web.ps1"
if errorlevel 1 (
  pause
  exit /b 1
)
dotnet publish Web\PracticaWeb.csproj -c Release -o ejecutables-web
pause
