"""Empaqueta la entrega web con fuentes, informe, evidencias y ejecutable portable."""
from pathlib import Path
from datetime import datetime
import shutil
import zipfile

BASE = Path(__file__).resolve().parents[1]
trabajo = BASE / 'paquete-entrega' / datetime.now().strftime('%Y%m%d-%H%M%S')
paquete = trabajo / 'Practica_U2_ED032026_WEB'
paquete.mkdir(parents=True, exist_ok=False)

def copiar(origen, destino=None):
    origen = BASE / origen
    destino = paquete / (destino or origen.relative_to(BASE))
    if origen.is_dir():
        shutil.copytree(origen, destino, ignore=shutil.ignore_patterns('bin', 'obj', '__pycache__', '*.pdb'))
    else:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)

for carpeta in ('Web', 'WebPublica', 'evidencias-web'):
    copiar(carpeta)
copiar('CSharp/Modelos.cs')
for archivo in ('Practica_U2_Web.sln', 'README.md', 'datos_portada.json', 'Dockerfile', '.dockerignore', 'railway.json', 'pruebas-web.txt', 'pruebas-publica.txt', 'documentacion/Documentacion_WEB.pdf', 'documentacion/Enunciado_original.pdf'):
    copiar(archivo)
for archivo in ('probar-web.ps1', 'preparar-publica.ps1', 'generar_documentacion_web.py', 'generar_documentacion_csharp.py', 'empaquetar-web.py'):
    copiar('herramientas/' + archivo)
copiar('ejecutables-web-portable', 'Publicacion')

(paquete / 'ABRIR_EN_LINEA.url').write_text('[InternetShortcut]\nURL=https://victormanuelxd360-afk.github.io/Practica_U2_ED032026/\n', encoding='utf-8')
(paquete / 'INICIAR_LOCAL.cmd').write_text('@echo off\r\ncd /d "%~dp0"\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0herramientas\\abrir-local.ps1"\r\n', encoding='ascii')
(paquete / 'herramientas/abrir-local.ps1').write_text(r'''$ErrorActionPreference = 'Stop'
$carpetaWeb = Join-Path (Split-Path -Parent $PSScriptRoot) 'Publicacion'
$puertoWeb = 5190
$urlWeb = "http://localhost:$puertoWeb"
$servidorWeb = Start-Process -FilePath (Join-Path $carpetaWeb 'PracticaWeb.exe') -ArgumentList "--urls $urlWeb" -WorkingDirectory $carpetaWeb -WindowStyle Hidden -PassThru
try {
    $listoWeb = $false
    for ($i = 0; $i -lt 80; $i++) {
        if ($servidorWeb.HasExited) { throw 'No pudo iniciarse la web. Cierra cualquier otra copia local y vuelve a intentar.' }
        try { Invoke-WebRequest "$urlWeb/api/estado" -UseBasicParsing | Out-Null; $listoWeb = $true; break } catch { Start-Sleep -Milliseconds 250 }
    }
    if (-not $listoWeb) { throw 'El servidor no respondió.' }
    Start-Process $urlWeb
    Write-Host 'La web local está funcionando. No necesitas instalar .NET.'
    Read-Host 'Deja esta ventana abierta. Pulsa Enter para detener la web local'
} finally {
    if (-not $servidorWeb.HasExited) { Stop-Process -Id $servidorWeb.Id }
}
''', encoding='utf-8-sig')
(paquete / 'LEEME_ANTES_DE_ENTREGAR.txt').write_text('''PRÁCTICA UNIDAD II - VERSIÓN WEB

1. Para usar la web pública: abre ABRIR_EN_LINEA.url.
   No depende de esta computadora ni de un servidor local.
2. Para usarla sin conexión en Windows x64: extrae TODO el ZIP y abre INICIAR_LOCAL.cmd.
   La carpeta Publicacion incluye .NET; no necesitas instalarlo.
   Mantén abierta la ventana y pulsa Enter cuando quieras detenerla.
3. Código editable: abre Practica_U2_Web.sln con Visual Studio compatible con .NET 10,
   o ejecuta dotnet run --project Web/PracticaWeb.csproj --urls http://localhost:5188.
4. Informe de entrega: documentacion/Documentacion_WEB.pdf.
5. Evidencias y resultados: evidencias-web/publica, pruebas-web.txt y pruebas-publica.txt.

IMPORTANTE: los integrantes y el grupo están pendientes porque no se proporcionaron.
Complétalos en datos_portada.json y regenera el informe antes de la entrega formal.
La generación del PDF requiere Python con reportlab y Pillow en Windows.

JUEGO: cada coche pintado reduce dos segundos el intervalo de llegada,
desde 20 segundos hasta un mínimo de 2. Finaliza al acumular cinco coches.

Web pública: https://victormanuelxd360-afk.github.io/Practica_U2_ED032026/
Repositorio: https://github.com/victormanuelxd360-afk/Practica_U2_ED032026/tree/web
''', encoding='utf-8-sig')

zip_salida = BASE / 'Practica_U2_ED032026_WEB_Entrega.zip'
with zipfile.ZipFile(zip_salida, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for archivo in paquete.rglob('*'):
        if archivo.is_file():
            z.write(archivo, archivo.relative_to(trabajo))
with zipfile.ZipFile(zip_salida) as z:
    assert z.testzip() is None, 'El ZIP está dañado.'
    nombres = z.namelist()
    for requerido in ('Publicacion/PracticaWeb.exe', 'documentacion/Documentacion_WEB.pdf', 'Web/Program.cs', 'CSharp/Modelos.cs', 'WebPublica/Program.cs'):
        assert 'Practica_U2_ED032026_WEB/' + requerido in nombres, requerido
print(f'ZIP verificado: {zip_salida} ({zip_salida.stat().st_size / 1024 / 1024:.1f} MB)')
print(f'Carpeta: {paquete}')
