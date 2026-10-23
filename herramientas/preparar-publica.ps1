$ErrorActionPreference = 'Stop'
$raizPractica = Split-Path -Parent $PSScriptRoot
$origenPractica = Join-Path $raizPractica 'Web\wwwroot'
$destinoPractica = Join-Path $raizPractica 'WebPublica\wwwroot'
Copy-Item (Join-Path $origenPractica 'app.js'),(Join-Path $origenPractica 'style.css') -Destination $destinoPractica -Force
$htmlPractica = [System.IO.File]::ReadAllText((Join-Path $origenPractica 'index.html'))
$htmlPractica = $htmlPractica.Replace('<head>','<head><base href="./">').Replace('href="/style.css"','href="./style.css"').Replace('href="/"','href="./"')
$htmlPractica = $htmlPractica.Replace('<script src="/app.js" defer></script>','<script src="./_framework/blazor.webassembly.js" autostart="false" defer></script><script src="./motor.js" defer></script><script src="./app.js" defer></script>')
$htmlPractica = $htmlPractica.Replace('<body>','<body><div id="motor-csharp" hidden></div>')
$htmlPractica = $htmlPractica.Replace('Tus datos se conservan al cambiar de ejercicio. La sesión termina tras dos horas sin actividad o al reiniciar el servidor.','Los ejercicios se ejecutan en C# dentro de tu navegador. Las listas se reinician al recargar; el récord se guarda en este navegador.')
$htmlPractica = $htmlPractica.Replace('C# · ASP.NET Core','C# · WebAssembly')
[System.IO.File]::WriteAllText((Join-Path $destinoPractica 'index.html'), $htmlPractica)
