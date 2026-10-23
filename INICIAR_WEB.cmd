@echo off
setlocal
cd /d "%~dp0"
echo Abre http://localhost:5188 en tu navegador.
echo Mantiene esta ventana abierta. Ctrl+C detiene el servidor.
dotnet run --project Web\PracticaWeb.csproj --configuration Release --urls http://localhost:5188
if errorlevel 1 pause
