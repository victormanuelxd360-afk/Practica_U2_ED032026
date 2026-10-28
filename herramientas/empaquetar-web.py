"""Empaqueta la entrega web con fuentes, informe, evidencias y ejecutable portable."""
from pathlib import Path
from datetime import datetime
import shutil
import zipfile

BASE = Path(__file__).resolve().parents[1]
DOC = BASE / 'documentacion'
trabajo = BASE / 'paquete-entrega' / datetime.now().strftime('%Y%m%d-%H%M%S')
paquete = trabajo / 'Practica_U2_ED032026_WEB'
documento = trabajo / 'Practica_U2_Documentacion'
paquete.mkdir(parents=True, exist_ok=False)

def copiar(origen, destino=None, raiz=BASE, carpeta=paquete):
    origen = raiz / origen
    destino = carpeta / (destino or origen.relative_to(raiz))
    if origen.is_dir():
        shutil.copytree(origen, destino, ignore=shutil.ignore_patterns('bin', 'obj', '__pycache__', '*.pdb'))
    else:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)

for carpeta in ('Web', 'WebPublica'):
    copiar(carpeta)
copiar('CSharp/Modelos.cs')
for archivo in ('Practica_U2_Web.sln', 'README.md', 'Dockerfile', '.dockerignore', 'railway.json', 'pruebas-web.txt'):
    copiar(archivo)
for archivo in ('probar-web.ps1', 'preparar-publica.ps1', 'empaquetar-web.py'):
    copiar('herramientas/' + archivo)
copiar('ejecutables-web-portable', 'Publicacion')
for archivo in ('Documentacion_WEB.pdf', 'Portada_equipo.png', 'Enunciado_original.pdf', 'datos_portada.json', 'pruebas-publica.txt', 'evidencias-web', 'herramientas/generar_documentacion_web.py', 'herramientas/ampliar_documentacion_web.py', 'herramientas/contenido_codigo_web.py', 'herramientas/generar_documentacion_csharp.py'):
    copiar(archivo, raiz=DOC, carpeta=documento)

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

La entrega tiene dos carpetas separadas:
- Practica_U2_ED032026_WEB: el programa (código, ejecutable y pruebas).
- Practica_U2_Documentacion: el informe, la portada y las evidencias.
  El programa no necesita esa carpeta para funcionar.

1. Para usar la web pública: abre ABRIR_EN_LINEA.url.
   No depende de esta computadora ni de un servidor local.
2. Para usarla sin conexión en Windows x64: extrae TODO el ZIP y abre INICIAR_LOCAL.cmd.
   La carpeta Publicacion incluye .NET; no necesitas instalarlo.
   Mantén abierta la ventana y pulsa Enter cuando quieras detenerla.
3. Código editable: abre Practica_U2_Web.sln con Visual Studio compatible con .NET 10,
   o ejecuta dotnet run --project Web/PracticaWeb.csproj --urls http://localhost:5188.
4. Informe de entrega: Practica_U2_Documentacion/Documentacion_WEB.pdf.
5. Resultados de las pruebas automáticas: pruebas-web.txt (en esta carpeta).
   Evidencias: Practica_U2_Documentacion/evidencias-web/publica y pruebas-publica.txt.

PORTADA: se incorporó la imagen entregada por el equipo, con los cuatro integrantes
y grupo 4.º A. Los datos editables están en Practica_U2_Documentacion/datos_portada.json.
El informe tiene 50 páginas: desarrollo y evidencias, explicación de métodos,
fragmentos reales de C#, recorridos de ejecución y guía de exposición.
Para regenerarlo, desde el repositorio: python documentacion/herramientas/generar_documentacion_web.py.
Requiere Python con reportlab, Pillow y pypdf en Windows.

JUEGO: los cinco primeros coches llegan cada 20 segundos, del 6 al 8 cada 10
y desde el 9 cada 2. Finaliza al acumular cinco coches en la cola.

Web pública: https://victormanuelxd360-afk.github.io/Practica_U2_ED032026/
Repositorio: https://github.com/victormanuelxd360-afk/Practica_U2_ED032026/tree/web
''', encoding='utf-8-sig')

zip_salida = BASE / 'Practica_U2_ED032026_WEB_Entrega.zip'
with zipfile.ZipFile(zip_salida, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for archivo in trabajo.rglob('*'):
        if archivo.is_file():
            z.write(archivo, archivo.relative_to(trabajo))
with zipfile.ZipFile(zip_salida) as z:
    assert z.testzip() is None, 'El ZIP está dañado.'
    nombres = z.namelist()
    for requerido in ('Publicacion/PracticaWeb.exe', 'Web/Program.cs', 'CSharp/Modelos.cs', 'WebPublica/Program.cs'):
        assert 'Practica_U2_ED032026_WEB/' + requerido in nombres, requerido
    assert 'Practica_U2_Documentacion/Documentacion_WEB.pdf' in nombres, 'Documentacion_WEB.pdf'
print(f'ZIP verificado: {zip_salida} ({zip_salida.stat().st_size / 1024 / 1024:.1f} MB)')
print(f'Carpetas: {paquete} y {documento}')
