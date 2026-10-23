$ErrorActionPreference = 'Stop'
$raizPractica = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $raizPractica
try {
    dotnet build Practica_U2_ED032026.sln -c Release --nologo
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar la solución C#.' }
    $pruebaPractica = Start-Process -FilePath '.\CSharp\bin\Release\net10.0-windows\Practica_U2.exe' -ArgumentList '--probar' -WindowStyle Hidden -Wait -PassThru
    Get-Content pruebas-csharp.txt
    if ($pruebaPractica.ExitCode -ne 0) { throw 'Fallaron las pruebas de C#.' }
    dotnet publish CSharp\Practica.csproj -c Release --no-restore -o ejecutables\General --nologo
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo publicar el menú general.' }
    foreach ($categoriaPractica in @('Listas','Pilas','Colas')) {
        dotnet publish "proyectos\$categoriaPractica\$categoriaPractica.csproj" -c Release --no-restore -o "ejecutables\$categoriaPractica" --nologo
        if ($LASTEXITCODE -ne 0) { throw "No se pudo publicar $categoriaPractica." }
    }
    Write-Host 'Listo: C#, cuatro ejecutables y pruebas correctas.' -ForegroundColor Green
} finally { Pop-Location }
