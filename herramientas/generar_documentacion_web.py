"""Genera la documentación de entrega usando las capturas reales de la web pública."""
from pathlib import Path
import ast
import json
from html import escape
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = Path(__file__).resolve().parents[1]
arbol = ast.parse((BASE / 'herramientas/generar_documentacion_csharp.py').read_text(encoding='utf-8-sig'))
ejercicios = next(ast.literal_eval(n.value) for n in arbol.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ejercicios' for t in n.targets))
datos = json.loads((BASE / 'datos_portada.json').read_text(encoding='utf-8-sig'))
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
estilos = getSampleStyleSheet()
for estilo in estilos.byName.values():
    estilo.fontName = 'Arial'
    estilo.leading = 13
for nombre in ('Title', 'Heading1', 'Heading2'):
    estilos[nombre].fontName = 'ArialBold'
    estilos[nombre].textColor = HexColor('#11685d')
estilos['Title'].leading = 28
estilos['Heading1'].leading = 23
contenido = []
def p(texto, estilo='BodyText'):
    contenido.append(Paragraph(escape(texto), estilos[estilo]))
    contenido.append(Spacer(1, 7))

p('Práctica de la Unidad II', 'Title')
p('Estructuras de datos básicas', 'Title')
p('Versión WEB / C# / WebAssembly', 'Heading1')
for etiqueta, valor in [('Institución', datos['institucion']), ('Asignatura', 'Estructura de Datos'), ('Docente', datos['docente']), ('Integrantes', datos['integrantes']), ('Grupo', datos['grupo']), ('Entrega', datos['fecha_entrega'])]:
    p(f'{etiqueta}: {valor}')
p('Web pública: https://victormanuelxd360-afk.github.io/Practica_U2_ED032026/')
p('Doce ejercicios de listas, pilas y colas ejecutados mediante modelos C# compartidos. Las capturas se generaron desde los controles reales de la versión pública en el navegador. Los nombres completos de integrantes y grupo deben completarse antes de entregar.')
p('Ejecución y arquitectura', 'Heading2')
p('La web pública funciona en GitHub Pages y ejecuta los algoritmos en C# WebAssembly. No depende de una computadora encendida. WebPublica contiene el motor para navegador; CSharp/Modelos.cs contiene las estructuras; Web/Estado.cs coordina los ejercicios. Web conserva la alternativa ASP.NET Core con sesiones de servidor.')
p('El ZIP incluye código, solución, pruebas, capturas y Publicacion, una copia local para Windows x64 que no necesita instalar .NET. INICIAR_LOCAL.cmd abre esa copia. ABRIR_EN_LINEA.url abre la web pública. Para modificar el código se necesita SDK .NET 10.')

for codigo, titulo, problema, entradas, proceso, salidas, pasos in ejercicios:
    contenido.append(PageBreak())
    p(f'{codigo}. {titulo}', 'Heading1')
    proceso = proceso.replace('ComboBox', 'selector web').replace('DataGridView', 'tabla web')
    pasos = pasos.replace('pulsa Sumar.', 'pulsa Sumar números.').replace('LocalAppData', 'el almacenamiento local del navegador')
    if codigo == 'C2':
        proceso = 'Un reloj monótono controla llegadas y tiempo de partida. El primer coche aparece inmediatamente y el intervalo comienza en 20 segundos. Cada coche correctamente pintado reduce 2 segundos el intervalo y adelanta la siguiente llegada si corresponde, hasta un mínimo de 2 segundos. Sólo puede retirarse el frente.'
        pasos = 'Pulsa Iniciar partida y luego el color solicitado por el coche de la izquierda. La captura muestra un acierto y el intervalo reducido de 20 a 18 segundos. Los siguientes aciertos lo reducen a 16, 14 y así hasta 2 segundos. La partida termina al acumular cinco coches. El récord y su tiempo se guardan en este navegador.'
    for etiqueta, texto in [('Problema', problema), ('Entradas', entradas), ('Proceso', proceso), ('Salidas', salidas), ('Funcionamiento y evidencia', pasos)]:
        p(f'{etiqueta}: {texto}')
    ruta = BASE / 'evidencias-web/publica' / f'{codigo}.png'
    with PILImage.open(ruta) as img:
        ancho, alto = img.size
    escala = min(505 / ancho, 390 / alto)
    contenido.append(Image(str(ruta), width=ancho * escala, height=alto * escala))

contenido.append(PageBreak())
p('Pruebas y decisiones', 'Heading1')
p('Se verificaron los doce ejercicios por sus controles en la versión C# WebAssembly y el cambio de dificultad después del primer acierto. La variante ASP.NET además tiene pruebas HTTP de validación y aislamiento de sesiones.')
for archivo in ('pruebas-publica.txt', 'pruebas-web.txt'):
    p(archivo, 'Heading2')
    for linea in (BASE / archivo).read_text(encoding='utf-8-sig').splitlines():
        p(linea)
p('En la versión pública los datos de los ejercicios permanecen al navegar y se reinician al recargar. El récord del juego se conserva en el almacenamiento local. La variante ASP.NET usa sesiones del servidor, con expiración por inactividad o reinicio. La tarifa de estacionamiento es de $2.00 por segundo completo; la salida es FIFO.')
p('Se resuelven los errores de redacción del enunciado como: mostrar aprobados y reprobados, y sustituir el valor viejo por el nuevo manteniendo el orden de la pila. El cambio de dificultad por cada coche pintado fue solicitado expresamente por el equipo.')

def pie(c, doc):
    c.setFont('Arial', 9)
    c.setFillColor(HexColor('#11685d'))
    c.drawString(40, 23, 'Unidad II / Versión WEB / C#')
    c.drawRightString(555, 23, str(doc.page))

salida = BASE / 'documentacion/Documentacion_WEB.pdf'
SimpleDocTemplate(str(salida), leftMargin=40, rightMargin=40, topMargin=35, bottomMargin=40, title='Práctica Unidad II - Versión WEB').build(contenido, onFirstPage=pie, onLaterPages=pie)
print(salida)
