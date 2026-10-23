"""Genera la documentación a partir de las evidencias reales y los datos de portada.
Requiere: reportlab, Pillow, pypdf. No modifica el enunciado ni las fuentes Java.
"""
from pathlib import Path
import json
import re
import subprocess
from html import escape
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'documentacion' / 'Documentacion_Unidad_II.pdf'
DATOS = json.loads((BASE / 'datos_portada.json').read_text(encoding='utf-8-sig'))
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial', boldItalic='Arial-Bold')
AZUL = HexColor('#1a3457')
VERDE = HexColor('#107057')
GRIS = HexColor('#4c5c6e')
W, H = A4
M = 43
ANCHO = W - M * 2
c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('Práctica Unidad II - Listas, pilas y colas')
c.setAuthor(DATOS['integrantes'])
paginas = []
y = H - 65

def estilo(size=10, color=GRIS, bold=False):
    return ParagraphStyle('p', fontName='Arial-Bold' if bold else 'Arial', fontSize=size,
                          leading=size * 1.33, textColor=color, spaceAfter=0)

def parrafo(texto, size=10, color=GRIS, bold=False, espacio=7):
    global y
    p = Paragraph(texto, estilo(size, color, bold))
    _, alto = p.wrap(ANCHO, H)
    if y - alto < 47:
        raise ValueError(f'Desbordamiento en página {len(paginas)}: {texto[:75]}')
    p.drawOn(c, M, y - alto)
    y -= alto + espacio

def nueva(titulo, seccion):
    global y
    if paginas:
        pie()
        c.showPage()
    paginas.append(titulo)
    y = H - 65
    c.setFillColor(AZUL)
    c.rect(0, H - 36, W, 36, fill=1, stroke=0)
    c.setFont('Arial-Bold', 9)
    c.setFillColor(white)
    c.drawString(M, H - 23, 'ESTRUCTURA DE DATOS   /   UNIDAD II')
    c.setFont('Arial', 8)
    c.drawRightString(W-M, H-23, seccion)
    parrafo(titulo, 21, AZUL, True, 14)

def pie():
    c.setStrokeColor(HexColor('#dce4ed'))
    c.line(M, 37, W-M, 37)
    c.setFillColor(GRIS)
    c.setFont('Arial', 8)
    c.drawString(M, 24, 'Listas / Pilas / Colas - Práctica de octubre de 2026')
    c.drawRightString(W-M, 24, str(len(paginas)))

def tabla(filas, anchos=None, size=9):
    global y
    anchos = anchos or [90, ANCHO-90]
    contenido = [[Paragraph(escape(str(v)), estilo(size, AZUL if i==0 else GRIS, i==0)) for i,v in enumerate(f)] for f in filas]
    t = Table(contenido, colWidths=anchos, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),HexColor('#eaf0f7')),
                          ('GRID',(0,0),(-1,-1),0.4,HexColor('#d9e1eb')),
                          ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
                          ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),
                          ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    _, alto=t.wrap(ANCHO,H)
    if y-alto<47: raise ValueError('Tabla desbordada')
    t.drawOn(c,M,y-alto);y-=alto+10

def imagen(nombre, explicacion, maxalto=310):
    global y
    path=BASE/'evidencias'/nombre
    with PILImage.open(path) as im:
        iw,ih=im.size
    escala=min(ANCHO/iw,maxalto/ih)
    ancho,alto=iw*escala,ih*escala
    if y-alto<75: raise ValueError('Imagen desbordada: '+nombre)
    c.drawImage(str(path), M+(ANCHO-ancho)/2, y-alto, ancho, alto)
    c.setStrokeColor(HexColor('#dce4ed'))
    c.rect(M+(ANCHO-ancho)/2,y-alto,ancho,alto,fill=0,stroke=1)
    y-=alto+7
    parrafo(explicacion,8.5,GRIS,espacio=10)

EJERCICIOS = [
dict(id='L1', titulo='Productos disponibles y retirados',
 problema='Almacenar objetos Producto escaneados con cantidad y precio aleatorios, permitir su retiro e informar cuántos productos están disponibles y cuántos fueron retirados.',
 entrada='Acción Escanear; clave del producto que se desea retirar.',
 proceso='Crear Producto con clave secuencial, nombre productoN, cantidad 1 a 20 y precio $1.00 a $500.00. Insertarlo en ArrayList; al retirarlo, moverlo a otra lista.',
 salida='Tabla con ambos estados, cantidad y precio unitario; contadores de objetos disponibles y retirados.',
 pasos='1. Escanear cuatro productos. 2. Escribir P2 en Clave. 3. Pulsar Retirar producto. 4. Revisar los contadores y el historial.',
 evidencia='Se ejecutaron cuatro escaneos y un retiro mediante los botones. Quedan tres objetos disponibles y uno retirado; producto2 conserva sus datos en el historial. Los valores aleatorios pueden variar.',
 prueba='Se verificaron 100 altas, rangos aleatorios, traslado a retirados y rechazo de un segundo retiro de la misma clave.'),
dict(id='L2', titulo='Pares e impares',
 problema='Generar una lista de números aleatorios y separar los valores pares e impares en dos listas adicionales.',
 entrada='Cantidad entera de elementos, entre 1 y 500.',
 proceso='Generar enteros de 0 a 999. Recorrer la lista original y aplicar número % 2: resto cero se agrega a pares, los demás a impares.',
 salida='Lista original, lista de pares y lista de impares, cada una con su número de elementos.',
 pasos='1. Introducir 15 en Cantidad. 2. Pulsar Generar y clasificar. 3. Comparar las tres listas; repetir sin cerrar la aplicación.',
 evidencia='El botón produjo una lista de 15 números y mostró su distribución. La suma de las cantidades de pares e impares coincide con el tamaño original; se conservan los repetidos.',
 prueba='Con semilla fija se generaron 500 valores y se verificó su paridad y la conservación de todas sus multiplicidades. Se rechaza cantidad cero.'),
dict(id='L3', titulo='Aprobados y reprobados',
 problema='Registrar alumnos con sus calificaciones y extraer de la lista inicial a quienes tengan menos de siete para almacenarlos en reprobados.',
 entrada='Nombre no vacío y calificación decimal de 0 a 10.',
 proceso='Agregar el objeto Alumno a la lista inicial. Recorrerla con Iterator y trasladar a reprobados los registros con nota menor que 7.',
 salida='Tabla que identifica la lista de cada alumno, su nota y las cantidades de aprobados y reprobados.',
 pasos='1. Registrar Ana López con 9.5. 2. Registrar Luis Pérez con 6.9. 3. Registrar María Díaz con 7. 4. Revisar ambas listas.',
 evidencia='Ana y María aparecen en aprobados; Luis fue trasladado a reprobados. La nota 7 se considera aprobatoria y admite valores decimales.',
 prueba='Se comprobaron notas 0, 6.99, 7 y 10. Se rechazan 11 y el nombre vacío. Se interpreta la repetición de “aprobaron” del enunciado como mostrar aprobados y reprobados.'),
dict(id='L4', titulo='Eliminar y ordenar productos',
 problema='Agregar productos con clave, nombre y precio, eliminar por clave, mostrar los nombres ordenados y calcular el costo total de compra.',
 entrada='Clave única, nombre y precio decimal no negativo; clave a eliminar.',
 proceso='Guardar Producto en ArrayList. Eliminar la coincidencia por clave. Ordenar una copia por nombre y sumar los precios con BigDecimal.',
 salida='Tabla alfabética y total monetario actualizado después de cada operación.',
 pasos='1. Agregar Zanahoria ($15.50), Arroz ($32.75), Leche ($26.25) y Pan ($20.00). 2. Eliminar P4 (Pan). 3. Revisar orden y total.',
 evidencia='Después de eliminar P4, se muestran Arroz, Leche y Zanahoria. El total correcto es $74.50. Los importes se calculan sin errores de punto flotante.',
 prueba='Se verificó orden por nombre, total $74.50, eliminación y recálculo; se rechazan claves duplicadas, inexistentes y precios negativos.'),
dict(id='L5', titulo='Listar palabras por letra',
 problema='Almacenar palabras y distribuirlas en listas según su primera letra, creando una nueva lista para cada inicial diferente.',
 entrada='Una palabra por registro, formada exclusivamente por letras; acepta acentos.',
 proceso='Conservar ArrayList original. Obtener la primera letra en mayúsculas y agrupar en un mapa ordenado cuyas entradas contienen listas independientes.',
 salida='Lista original y una lista rotulada por cada inicial encontrada.',
 pasos='1. Agregar Fresa y Fresca. 2. Agregar Orilla, Oso, Peso y Pez. 3. Agregar Árbol. 4. Revisar la nueva lista de Á.',
 evidencia='Las palabras del ejemplo quedan reunidas en F, O y P. Al registrar Árbol se crea automáticamente una cuarta lista con la inicial Á.',
 prueba='Se comprobó la agrupación sin distinguir mayúsculas, la inicial acentuada y el rechazo de una cadena con varias palabras.'),
dict(id='P1', titulo='Invertir palabra',
 problema='Leer una palabra e invertir sus caracteres mediante una pila, como UTM que produce MTU.',
 entrada='Palabra o texto no vacío.',
 proceso='Recorrer los puntos de código Unicode e insertarlos con push. Extraer cada uno con pop y concatenarlo al resultado hasta vaciar la pila.',
 salida='Entrada original y secuencia invertida.',
 pasos='1. Escribir UTM en Palabra. 2. Pulsar Invertir. 3. Leer la salida MTU. 4. Introducir otra palabra y repetir.',
 evidencia='La pantalla muestra UTM y MTU. El resultado se obtiene por la extracción LIFO de los caracteres, sin usar reverse como sustituto de la pila.',
 prueba='Se validaron UTM y una cadena con un carácter Unicode fuera del plano básico. Una entrada vacía produce un mensaje de datos faltantes.'),
dict(id='P2', titulo='Palíndromo',
 problema='Determinar si una palabra, número o frase se lee igual de izquierda a derecha que en sentido inverso.',
 entrada='Texto con al menos una letra o un dígito.',
 proceso='Pasar a minúsculas y conservar letras y dígitos. Invertir la secuencia normalizada mediante una pila y comparar ambas cadenas.',
 salida='Mensaje afirmativo o negativo sobre si es un palíndromo.',
 pasos='1. Introducir Anita lava la tina. 2. Pulsar Comprobar palíndromo. 3. Revisar el resultado. 4. Repetir con Casa para un caso negativo.',
 evidencia='Anita lava la tina se identifica como palíndromo al ignorar espacios y mayúsculas. Los acentos se conservan y no se eliminan de la comparación.',
 prueba='Se verificaron una frase, 12321 y Casa. Una entrada compuesta sólo por signos se rechaza porque carece de letras y números.'),
dict(id='P3', titulo='Suma de números grandes',
 problema='Sumar enteros muy grandes representados como cadenas usando pilas de dígitos, evitando el límite de los tipos enteros básicos.',
 entrada='Dos cadenas de dígitos del 0 al 9, sin signos ni separadores; se consideran enteros no negativos.',
 proceso='Apilar cada operando. Extraer unidades, sumar los dígitos y el acarreo, apilar el dígito resultante y repetir. Extraer la tercera pila para formar la suma.',
 salida='Suma exacta como cadena, sin ceros iniciales innecesarios.',
 pasos='1. Introducir treinta dígitos 9 en el primer campo. 2. Introducir 1 en el segundo. 3. Pulsar Sumar con pilas y revisar el acarreo final.',
 evidencia='La suma de treinta nueves y uno produce un 1 seguido de treinta ceros. Los operandos no se convierten a int, long ni BigInteger en la solución.',
 prueba='Se compararon 200 sumas aleatorias de hasta 1234 dígitos con BigInteger como oráculo exclusivo de pruebas. También se verificaron ceros iniciales y entradas inválidas.'),
dict(id='P4', titulo='Reemplazar valor en pila',
 problema='Implementar Reemplazar(pila, nuevo, viejo) para sustituir todas las apariciones del valor viejo por el nuevo sin alterar el orden de la pila.',
 entrada='Enteros para apilar; valores enteros viejo y nuevo, dentro del rango de int.',
 proceso='Desapilar en una pila auxiliar, sustituyendo las coincidencias y contando cambios. Devolver los elementos a la pila original para restaurar su orden.',
 salida='Pila mostrada de cima a base y cantidad de reemplazos realizados.',
 pasos='1. Apilar 1, 2, 3 y 2 en ese orden. 2. Introducir viejo=2 y nuevo=9. 3. Pulsar Reemplazar. 4. Revisar cima y base.',
 evidencia='Antes, la pila de cima a base era [2, 3, 2, 1]. Después queda [9, 3, 9, 1], con dos reemplazos. La posición relativa de los otros elementos se conserva.',
 prueba='Se comprobó la sustitución múltiple, valor ausente y pila vacía. Se interpreta el error de redacción del instrumento como reemplazar viejo por nuevo.'),
dict(id='C1', titulo='Ventanilla de un banco',
 problema='Administrar una cola de clientes con turno, nombre, movimiento y hora de llegada; atender al primero y calcular su tiempo de espera.',
 entrada='Capacidad (inicial 5), nombre y movimiento seleccionado en combo; turno y llegada se obtienen automáticamente.',
 proceso='InsertaCola agrega al final si ColaLlena es falso. EliminaCola atiende el frente si ColaVacia es falso y resta la llegada a la hora actual del sistema.',
 salida='Tabla actualizada, frente/final, confirmación del alta y aviso con el cliente atendido y espera en segundos.',
 pasos='1. Registrar Ana, Luis y María. 2. Seleccionar el movimiento antes de cada alta. 3. Pulsar Atender en ventanilla. 4. Revisar los turnos restantes.',
 evidencia='Ana, turno 1, fue atendida primero. Luis y María permanecen en orden; frente=2, final=3. El mensaje muestra la espera medida por el sistema durante esta ejecución.',
 prueba='Se verificaron FIFO, sobreflujo, cola vacía y espera exacta de 18 segundos con instantes controlados. La capacidad se modifica sólo con la cola vacía.'),
dict(id='C2', titulo='Juego: pintar coches',
 problema='Pintar el primer coche de una cola con el color solicitado antes de que se acumulen cinco coches; mostrar coches pintados, duración y récord.',
 entrada='Botón Iniciar y selección de color en la paleta.',
 proceso='Encolar un coche inicial y otro cada 20 s con color aleatorio. Validar el color del frente; al acertar, desencolar. Cada tres aciertos reducir el intervalo 2 s hasta 2 s.',
 salida='Coches ilustrados, etiquetas de color, siguiente llegada, tiempo, puntaje, récord y fin de partida al alcanzar cinco.',
 pasos='1. Pulsar Iniciar. 2. Leer la etiqueta del primer coche. 3. Seleccionar ese color en la paleta. 4. Continuar mientras llegan nuevos coches.',
 evidencia='La captura corresponde a 40 segundos simulados en el modelo real: hay tres coches. El frente se identifica en verde y sólo su color puede retirar un coche de la cola.',
 prueba='Se comprobaron llegada a los 20 s, color equivocado, aceleración, intervalo mínimo, reinicio y fin exacto con cinco coches. El récord se guarda localmente.'),
dict(id='C3', titulo='Estacionamiento para autos',
 problema='Administrar un estacionamiento sin cupo fijo mediante una cola circular doblemente ligada, con entrada por el final y salida por el frente; cobrar $2.00 por segundo.',
 entrada='Placas y propietario no vacíos; fecha y hora de entrada tomadas del sistema.',
 proceso='Crear un nodo Auto y enlazarlo con el último y el primero. Para salir, quitar el nodo frente y reparar ambos enlaces. Multiplicar los segundos completos por $2.00.',
 salida='Confirmación de entrada, tabla FIFO y recibo con placas, propietario, entrada, salida, tiempo y costo.',
 pasos='1. Registrar ABC-123 y XYZ-987. 2. Dar salida al primer auto. 3. Revisar su recibo. 4. Agregar MEX-456 y verificar los enlaces.',
 evidencia='Se retiró ABC-123 tras 30 segundos de prueba, por $60.00. Los autos restantes son XYZ-987 y MEX-456 en ese orden. La pantalla confirma que los enlaces circulares son correctos.',
 prueba='Se comprobaron salida en vacío, placas duplicadas, caso de un solo nodo, cobro y mil inserciones/salidas sin cupo fijo, validando los enlaces en cada eliminación.')
]

nueva('Práctica de la Unidad II', 'DOCUMENTACIÓN DEL PROYECTO')
parrafo('Estructuras de datos básicas', 27, AZUL, True, 20)
c.setFillColor(HexColor('#e8eff7'));c.roundRect(M,y-120,ANCHO,120,14,fill=1,stroke=0)
c.setFillColor(AZUL);c.setFont('Arial-Bold',32);c.drawString(M+22,y-48,'LISTAS   PILAS   COLAS')
c.setFont('Arial',13);c.drawString(M+22,y-82,'12 ejercicios / 3 proyectos de escritorio / Java 21')
y-=150
tabla([('Institución',DATOS['institucion']),('División','Tecnologías de la Información y Comunicación'),
       ('Carrera','Ingeniería en Tecnologías de la Información e Innovación Digital'),('Asignatura','Estructura de Datos'),
       ('Docente',DATOS['docente']),('Integrantes',DATOS['integrantes']),('Grupo',DATOS['grupo']),
       ('Entrega',DATOS['fecha_entrega']),('Elaboración','16 de octubre de 2026')],size=10)
parrafo('Implementación orientada a objetos con menús funcionales, validación de entradas y documentación de resultados.',11,VERDE,espacio=12)
parrafo('Datos por completar: integrantes y grupo. No se inventaron identidades ni un grupo del equipo.',9)

nueva('Guía de ejecución y contenido', 'GUÍA DE USO')
parrafo('<b>Objetivo.</b> Implementar las operaciones de listas, pilas y colas y comprobar su comportamiento mediante interfaces de escritorio y pruebas reproducibles.')
parrafo('<b>Requisitos.</b> Windows con Java 21 o posterior. La aplicación usa únicamente la biblioteca estándar: Swing, colecciones, BigDecimal y java.time. No requiere Internet. Para recompilar se necesita un JDK.')
parrafo('<b>Inicio.</b> Abrir INICIAR.cmd para acceder al menú general, o el INICIAR.cmd de proyectos/Listas, proyectos/Pilas o proyectos/Colas para trabajar con cada estructura por separado.')
parrafo('<b>Navegación.</b> Elegir una opción en el menú lateral. Los módulos conservan sus datos mientras la aplicación permanece abierta. Cada acción valida los campos y permite continuar sin reiniciar todo el programa. Salir cierra el proyecto.')
imagen('menu_general.png','Figura 1. Menú general y primer ejercicio después de ejecutar las operaciones de demostración. Los tres proyectos independientes ofrecen sólo las opciones de su estructura.',maxalto=300)
tabla([('Listas','L1-L5: productos, pares/impares, alumnos, compra, palabras.'),('Pilas','P1-P4: inversión, palíndromo, suma grande, reemplazo.'),('Colas','C1-C3: banco, juego de coches, estacionamiento.'),('Verificación','Evidencias ampliadas, validaciones, resultados de pruebas y trazabilidad.')],size=9)

nueva('Arquitectura y decisiones', 'DESARROLLO')
tabla([('Modelo','Estructuras.java: objetos Producto, Alumno, Cliente, Coche y Auto; operaciones de cada estructura sin dependencias de Swing.'),
       ('Interfaz','PracticaApp.java: un panel por ejercicio, campos con nombres descriptivos, botones, tablas no editables y mensajes de error o confirmación.'),
       ('Proyectos','Listas, Pilas y Colas incluyen Inicio.java, fuentes, clases y JAR. Cada Inicio abre su menú correspondiente.'),
       ('Pruebas','Pruebas.java: validaciones de algoritmos, límites, FIFO/LIFO, enlaces, tiempos e integración de botones. Produce registro y evidencias.'),
       ('Recursos','Ilustraciones originales de coches dibujadas con Graphics2D; sin imágenes remotas ni dependencias adicionales.')])
parrafo('<b>Estructuras empleadas.</b> ArrayList almacena listas. ArrayDeque se usa como pila mediante push/pop y como base de la cola FIFO acotada. El estacionamiento no usa una lista como sustituto de sus enlaces: implementa nodos con anterior y siguiente, cerrados circularmente.')
parrafo('<b>Entradas numéricas.</b> Precios y calificaciones aceptan decimales con punto o coma. Los importes se manejan con BigDecimal y se muestran con dos decimales. Cantidades, turnos y valores de pila requieren enteros. La suma grande recibe cadenas de dígitos no negativos.')
parrafo('<b>Reglas no especificadas.</b> Se fija capacidad inicial del banco en 5, modificable entre 1 y 1000; generación aleatoria de 0 a 999 y máximo de 500 números. En el juego se reduce el intervalo 2 s cada 3 aciertos, con mínimo 2 s y primer coche inmediato.')
parrafo('<b>Tiempo y datos.</b> Las operaciones normales usan la hora del sistema. El estacionamiento cobra segundos completos a $2.00 cada uno. Los datos permanecen durante la sesión. El récord del juego se guarda en la carpeta de usuario .practica-u2/record.properties.')
parrafo('<b>Interpretación del instrumento.</b> En listas 3, la repetición de “aprobaron” se resuelve mostrando ambas listas. En pilas 4 se entiende viejo como el valor buscado y nuevo como su sustituto. Se elige Java Swing porque el lenguaje y el tipo de aplicación son libres.')

for e in EJERCICIOS:
    nueva(f"{e['id']}. {e['titulo']}", 'LISTAS' if e['id'][0]=='L' else 'PILAS' if e['id'][0]=='P' else 'COLAS')
    parrafo('<b>Problema.</b> '+e['problema'],9.5)
    tabla([('Entradas',e['entrada']),('Proceso',e['proceso']),('Salidas',e['salida'])],size=9)
    parrafo('<b>Funcionamiento paso a paso.</b> '+e['pasos'],9.5)
    imagen(e['id']+'_resultado.png','Figura '+e['id']+'. '+e['evidencia'],maxalto=287)
    parrafo('<b>Pruebas y validaciones.</b> '+e['prueba'],9.2)

nueva('Juego: aceleración y fin de partida','EVIDENCIAS ADICIONALES')
imagen('juego_aceleracion.png','Figura C2-A. Después de tres aciertos, el contador indica tres coches pintados y el intervalo disminuye de 20 a 18 segundos. El modelo avanza con un reloj controlado para probar el cambio sin esperas reales.',maxalto=257)
imagen('juego_fin.png','Figura C2-B. Sin pintar coches, se acumulan cinco al segundo 80 (uno inicial y cuatro llegadas). El juego detiene su tiempo y conserva el resultado. No permite retirar coches hasta iniciar otra partida.',maxalto=257)
parrafo('Durante la ejecución interactiva, un Timer de Swing revisa el reloj cada 100 ms. El modelo decide las llegadas con marcas de tiempo; si hay un retraso, procesa las llegadas pendientes en orden.',9)

negativas=[
 ('validacion_numeros.png','Entrada no numérica','Al introducir 12x en la suma, se muestra un mensaje que solicita enteros no negativos. La aplicación permanece abierta y permite corregir la entrada.'),
 ('validacion_faltantes.png','Datos faltantes','Al intentar registrar un producto sin nombre se muestra “Hay datos faltantes”. La lista y el total se conservan sin agregar un registro incompleto.'),
 ('validacion_cola_vacia.png','Cola vacía','Después de atender a todos los clientes, una nueva solicitud de atención informa que la cola está vacía. Frente y final se muestran como -1.'),
 ('validacion_cola_llena.png','Cola llena','Con capacidad 1 y un cliente esperando, una segunda inserción se rechaza sin alterar la cola. Se conserva un solo cliente y se informa el sobreflujo.'),
 ('validacion_rango.png','Calificación fuera de rango','La entrada 11 se rechaza porque la calificación debe estar entre 0 y 10. Los alumnos ya registrados mantienen sus notas y clasificación.')
]
for n in range(0,len(negativas),2):
    nueva('Validaciones de entrada y operación',f'PRUEBAS {n//2+1}')
    for archivo,titulo,caption in negativas[n:n+2]:
        parrafo(titulo,12,AZUL,True)
        imagen(archivo,caption,maxalto=251)

registro=(BASE/'documentacion'/'pruebas_resultados.txt').read_text(encoding='utf-8')
total=re.search(r'TOTAL: (\d+)',registro).group(1)
nueva('Verificación y entrega', 'RESULTADOS')
parrafo(f'<b>Resultado comprobado:</b> {total} verificaciones correctas, sin fallos, ejecutadas con Java 21.0.11. El registro completo se incluye en pruebas_resultados.txt.',12,VERDE)
tabla([('Listas','Altas/retiros, rangos aleatorios, paridad y multiplicidad, umbral 7, orden alfabético, total exacto, claves e iniciales.'),
       ('Pilas','LIFO, Unicode, palíndromos positivos/negativos, acarreos y ceros, 200 sumas grandes contra oráculo, reemplazo con conservación del orden.'),
       ('Colas','FIFO, sobreflujo y vacío; espera de 18 s; llegadas, color y aceleración; fin con cinco coches; tarifa y mil nodos circulares.'),
       ('Interfaz','Se activan los controles reales de los doce módulos; se revisan mensajes y datos. Los paneles se pintan a PNG mediante Swing en modo de prueba.')])
parrafo('<b>Origen de las imágenes.</b> Son renderizaciones de los mismos paneles de la aplicación tras ejecutar las acciones de prueba. No son fotografías del monitor. Para las reglas temporales se usan instantes controlados; el uso normal toma el tiempo del sistema. Las capturas muestran resultados realmente producidos por el código.')
parrafo('<b>Reproducción.</b> Ejecutar COMPILAR_Y_PROBAR.cmd. El script compila, ejecuta pruebas, regenera imágenes y crea los cuatro JAR. Para actualizar este documento, ejecutar herramientas/generar_documentacion.py después de completar datos_portada.json; requiere Python con reportlab, Pillow y pypdf.')
parrafo('<b>Archivos para entregar.</b> El RAR incluye tres proyectos completos con fuentes y ejecutables, el menú general, este PDF, el enunciado original, las evidencias y el registro de pruebas. Verificar los nombres de integrantes y el grupo antes de subirlo.')
parrafo('<b>Entrega indicada.</b> Viernes 23 de octubre de 2026, por equipo; un integrante realiza la carga en Teams. La carga no se ha realizado desde este proyecto.')
parrafo('<b>Fuente de requisitos.</b> Instrumento F-SGC-033, revisión 00, Unidad II, Practica_U2_ED032026.pdf, 9 páginas, proporcionado por el usuario; copia de referencia en documentacion/Enunciado_original.pdf.',9)

nueva('Trazabilidad de la implementación','REFERENCIA DEL CÓDIGO')
filas=[('Requisito','Clase o método')]
for k,v in [
 ('L1: productos','Estructuras.Almacen; ProductosPanel'),('L2: paridad','Estructuras.generarNumeros; ParesPanel'),
 ('L3: alumnos','Estructuras.Grupo; AlumnosPanel'),('L4: compra','Estructuras.Compra; CompraPanel'),
 ('L5: palabras','Estructuras.agrupar; PalabrasPanel'),('P1: invertir','Estructuras.invertir; InvertirPanel'),
 ('P2: palíndromo','Estructuras.palindromo; PalindromoPanel'),('P3: suma','Estructuras.sumarGrandes; SumaPanel'),
 ('P4: reemplazo','Estructuras.Reemplazar; ReemplazoPanel'),('C1: banco','Estructuras.Cola y Banco; BancoPanel'),
 ('C2: juego','Estructuras.Juego; JuegoPanel y LienzoAutos'),('C3: estacionar','Estructuras.ColaCircularDoblementeLigada; ParkingPanel')]:filas.append((k,v))
tabla(filas,anchos=[125,ANCHO-125],size=9)
parrafo('<b>Costos de las operaciones.</b> Altas al final de ArrayList: O(1) amortizado; búsquedas por clave y clasificación de alumnos: O(n). Orden de compra: O(n log n). Invertir y sumar: O(n); reemplazar: O(n) y una pila auxiliar. Cola acotada: O(1) por inserción/extracción. En estacionamiento, enlazar o extraer es O(1); validar placas únicas recorre O(n).',9.5)
parrafo('<b>Alcance de las pruebas.</b> La evidencia verifica lógica y renderización Swing, sin depender de un IDE. La legibilidad final puede variar con la escala de pantalla del equipo; las ventanas son redimensionables y la tabla se puede desplazar. Los datos de trabajo, salvo el récord, no se guardan al cerrar.',9.5)

lineas=[l for l in registro.splitlines() if l.startswith('OK |')]
for i in range(0,len(lineas),35):
    nueva('Registro de pruebas automáticas',f'ANEXO {i//35+1}')
    for l in lineas[i:i+35]:parrafo(escape(l),8.3,espacio=4)
    if i+35>=len(lineas):parrafo(f'TOTAL: {total} verificaciones correctas. Sin fallos.',10,VERDE,True)
pie();c.save()
lector=PdfReader(str(OUT))
assert len(lector.pages)==len(paginas)
contenido='\n'.join(p.extract_text() for p in lector.pages)
for e in EJERCICIOS:assert e['titulo'] in contenido
assert f'{total} verificaciones correctas' in contenido
print(f'PDF verificado: {len(paginas)} páginas; {total} pruebas. {OUT}')
(BASE/'documentacion'/'indice_paginas.txt').write_text('\n'.join(f'{i+1}. {t}' for i,t in enumerate(paginas)),encoding='utf-8')

rar=Path('C:/Program Files/WinRAR/Rar.exe')
if rar.exists():
    destino=BASE.parent/(BASE.name+'.rar')
    subprocess.run([str(rar),'a','-r','-ep1','-idq',str(destino),BASE.name],cwd=BASE.parent,check=True)
    print('RAR actualizado:',destino)
