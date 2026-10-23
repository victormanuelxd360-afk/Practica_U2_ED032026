$ErrorActionPreference = 'Stop'
$raizPractica = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $raizPractica
try {
    $javacPractica = (Get-Command javac -ErrorAction Stop).Source
    $jarPractica = (Get-Command jar -ErrorAction Stop).Source
    $javaPractica = (Get-Command java -ErrorAction Stop).Source
    New-Item -ItemType Directory -Force -Path 'build' | Out-Null
    $fuentesPractica = @(Get-ChildItem -LiteralPath 'src' -Filter '*.java' | ForEach-Object { $_.FullName })
    & $javacPractica -encoding UTF-8 -d build @fuentesPractica
    if ($LASTEXITCODE -ne 0) { throw 'La compilación no terminó correctamente.' }
    & $javaPractica '-Djava.awt.headless=true' -cp build Pruebas $raizPractica
    if ($LASTEXITCODE -ne 0) { throw 'Hay pruebas fallidas. No se empaquetará la entrega.' }
    & $jarPractica --create --file 'Practica_U2.jar' --main-class PracticaApp -C build .
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el ejecutable general.' }
    foreach ($categoriaPractica in @('Listas','Pilas','Colas')) {
        $proyectoPractica = Join-Path $raizPractica "proyectos\$categoriaPractica"
        $srcPractica = Join-Path $proyectoPractica 'src'
        $buildPractica = Join-Path $proyectoPractica 'build'
        New-Item -ItemType Directory -Force -Path $srcPractica,$buildPractica | Out-Null
        Copy-Item -LiteralPath 'src\Estructuras.java','src\PracticaApp.java' -Destination $srcPractica -Force
        $inicioPractica = "public class Inicio { public static void main(String[] args) { PracticaApp.main(new String[] { `"$categoriaPractica`" }); } }"
        [System.IO.File]::WriteAllText((Join-Path $srcPractica 'Inicio.java'),$inicioPractica,(New-Object System.Text.UTF8Encoding($false)))
        $fuentesProyecto = @(Get-ChildItem -LiteralPath $srcPractica -Filter '*.java' | ForEach-Object { $_.FullName })
        & $javacPractica -encoding UTF-8 -d $buildPractica @fuentesProyecto
        if ($LASTEXITCODE -ne 0) { throw "Error de compilación en $categoriaPractica." }
        & $jarPractica --create --file (Join-Path $proyectoPractica "$categoriaPractica.jar") --main-class Inicio -C $buildPractica .
        if ($LASTEXITCODE -ne 0) { throw "Error al empaquetar $categoriaPractica." }
    }
    Write-Host 'Listo: tres proyectos, ejecutable general y pruebas correctas.' -ForegroundColor Green
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host 'Para compilar se requiere JDK 21 o posterior en PATH.'
    exit 1
}
