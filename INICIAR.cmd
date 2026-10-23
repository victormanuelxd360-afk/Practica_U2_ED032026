@echo off
setlocal
cd /d "%~dp0"
if exist "ejecutables\General\Practica_U2.exe" (
  start "" "ejecutables\General\Practica_U2.exe"
  exit /b 0
)
dotnet run --project "CSharp\Practica.csproj" --configuration Release
if errorlevel 1 pause
