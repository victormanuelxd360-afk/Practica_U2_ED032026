"""Genera el informe C# desde evidencias y pruebas reales. Requiere reportlab y Pillow."""
from pathlib import Path
from html import escape
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
styles = getSampleStyleSheet()
for style in styles.byName.values():
    style.fontName = 'Arial'
    style.leading = 14
styles['Title'].fontName = styles['Heading1'].fontName = styles['Heading2'].fontName = 'ArialBold'
styles['Title'].leading = 28
styles['Heading1'].leading = 22
styles['Heading1'].textColor = colors.HexColor('#1b3457')
datos = json.loads((BASE / 'datos_portada.json').read_text(encoding='utf-8-sig'))
story = []
def p(texto, estilo='BodyText'):
    story.append(Paragraph(escape(texto), styles[estilo]))
    story.append(Spacer(1, 8))

p('Práctica de la Unidad II', 'Title')
p('Estructuras de datos básicas', 'Title')
p('C# / Windows Forms / .NET 10', 'Heading1')
for etiqueta, valor in [('Institución', datos['institucion']), ('Asignatura', 'Estructura de Datos'), ('Docente', datos['docente']), ('Integrantes', datos['integrantes']), ('Grupo', datos['grupo']), ('Entrega', datos['fecha_entrega']), ('Versión C#', '23 de octubre de 2026')]:
    p(f'{etiqueta}: {valor}')
p('Doce ejercicios, tres proyectos independientes y un menú general. Las capturas de este informe provienen de los controles reales de la versión C#.')
p('Uso y arquitectura', 'Heading2')
p('Abrir Practica_U2_ED032026.sln o ejecutar INICIAR.cmd. COMPILAR_Y_PROBAR.cmd compila y verifica los cuatro proyectos. Las clases de Modelos.cs resuelven la lógica; Program.cs contiene la interfaz; Pruebas.cs valida modelos y botones.')
p('Convención de nombres: el formulario es frmPractica y cada control lleva prefijo por tipo y nombre descriptivo: btnRetirar, txtClaveRetiro, lblEstadoL1, dgvTablaC1, cboMovimiento, pnlCoches, tabC2, mnuSalir. Las pruebas verifican que todos los nombres tengan prefijo y sean únicos. Cada pestaña muestra un ícono de su estructura (lista, pila o cola).')
p('Requisitos: Windows y SDK .NET 10 para compilar. Los ejecutables publicados requieren .NET Desktop Runtime 10. Los datos se mantienen durante la sesión; el récord del juego se conserva en LocalAppData.')

ejercicios = [
('L1', 'Productos disponibles y retirados', 'Administrar el almacén de productos escaneados y conservar los retirados.', 'Clave del producto a retirar; la cantidad y el precio se generan automáticamente.', 'Escanear crea un objeto Producto y lo agrega a List<Producto>. Retirar busca por clave y mueve el objeto a otra lista.', 'Productos disponibles y retirados, con cantidades, precios y número de elementos.', 'Pulsa Escanear producto dos veces; escribe P1 y pulsa Retirar producto. La imagen muestra el producto1 retirado y el producto2 disponible. Una clave inexistente produce un mensaje sin perder datos.'),
('L2', 'Pares e impares', 'Separar una lista de números aleatorios en listas por paridad.', 'Cantidad entera entre 1 y 500.', 'Genera números de 0 a 999 y usa el residuo entre dos para agregarlos a las listas de pares e impares.', 'Lista original y las dos listas clasificadas.', 'Introduce 20 y pulsa Generar y separar. La captura muestra las tres listas; ningún número se pierde. Cero, decimales y letras se rechazan como cantidad.'),
('L3', 'Aprobados y reprobados', 'Clasificar alumnos según su calificación.', 'Nombre y calificación decimal de 0 a 10.', 'Agrega al alumno y extrae de la lista inicial los que tengan calificación menor que siete, trasladándolos a reprobados.', 'Listas de aprobados y reprobados con sus notas.', 'Registra Ana con 8.5 y Luis con 6.5. La captura muestra a cada alumno en su lista. Una nota igual a 7 aprueba; un nombre vacío o nota fuera de rango genera error.'),
('L4', 'Eliminar y ordenar productos', 'Mantener una compra con eliminación por clave y total.', 'Clave única, nombre y precio decimal no negativo.', 'Agrega a una lista, elimina por clave, ordena por nombre con comparación en español y suma precios usando decimal.', 'Tabla ordenada y costo total.', 'Agrega Arroz de 32.75 y Leche de 26.25. La imagen muestra total 59.00. Para eliminar, escribe la clave y pulsa Eliminar por clave. Se rechazan claves duplicadas y precios negativos.'),
('L5', 'Palabras por letra', 'Crear listas dinámicas según la primera letra de cada palabra.', 'Una palabra formada por letras en cada captura.', 'Conserva la lista original y agrupa por inicial en un diccionario ordenado cuyos valores son List<string>.', 'Lista original y una lista por inicial.', 'Agrega Fresa, Fresca, Oso, Orilla y Pez. La captura muestra grupos F, O y P. Nuevas iniciales crean listas automáticamente; se respetan letras acentuadas.'),
('P1', 'Invertir palabra', 'Mostrar una palabra en orden inverso mediante una pila.', 'Palabra no vacía.', 'Apila cada Rune del texto y desapila hasta vaciar la estructura.', 'Texto invertido, preservando los caracteres Unicode completos.', 'Escribe UTM y pulsa Invertir. La captura muestra MTU. El texto vacío genera un mensaje de datos faltantes.'),
('P2', 'Palíndromo', 'Determinar si un texto se lee igual en ambos sentidos.', 'Palabra, frase o número.', 'Normaliza mayúsculas y elimina espacios y signos; compara con la inversión realizada mediante pila.', 'Mensaje afirmativo o negativo.', 'Introduce Anita lava la tina y pulsa Comprobar. La captura muestra que es palíndromo. Se conservan acentos y se rechazan entradas compuestas únicamente por signos.'),
('P3', 'Suma de números grandes', 'Sumar enteros que exceden los tipos numéricos ordinarios.', 'Dos cadenas de dígitos, no negativas y sin separadores.', 'Apila dígitos de ambos operandos, desapila de derecha a izquierda, suma con acarreo y construye el resultado con una tercera pila.', 'Suma completa sin límite fijo de dígitos.', 'Introduce treinta nueves y 1, y pulsa Sumar. La imagen muestra un uno seguido de treinta ceros. Letras y signos se rechazan. BigInteger sólo se usa para comprobar las pruebas.'),
('P4', 'Reemplazar valor', 'Sustituir un entero por otro en una pila sin alterar su orden.', 'Enteros separados por comas, valor viejo y valor nuevo.', 'Desapila hacia una pila auxiliar sustituyendo coincidencias; después restaura la pila original.', 'Pila desde la cima y cantidad de reemplazos.', 'Con valores 1,2,3,2, viejo 2 y nuevo 9, pulsa Reemplazar. La captura muestra 9,3,9,1 desde la cima y dos reemplazos. Se interpreta el error de redacción del enunciado como reemplazar viejo por nuevo.'),
('C1', 'Ventanilla de banco', 'Administrar clientes mediante cola FIFO con capacidad limitada.', 'Nombre, movimiento del ComboBox y capacidad configurable con cola vacía.', 'Asigna turno y hora DateTime.Now; InsertaCola valida ColaLlena. Atender usa EliminaCola tras validar ColaVacia y calcula la espera.', 'DataGridView actualizado, No. Turno siguiente, frente y final; ventana "SE AGREGA UN CLIENTE AL FINAL DE LA COLA" con turno, nombre, movimiento y hora de llegada; ventana "TIEMPO DE ESPERA EN LA COLA" al atender.', 'Registra Ana y Luis y atiende a Ana. Cada alta abre la ventana de confirmación y la atención abre la ventana con el tiempo de espera. La captura deja a Luis en la cola. La capacidad inicial es cinco; se validan sobreflujo y atención con cola vacía. El botón Salida del sistema cierra la aplicación.'),
('C2', 'Juego de pintar coches', 'Atender coches en orden y pintarlos del color solicitado antes de que se acumulen cinco.', 'Botón Iniciar partida y selección de color en la paleta de botones coloreados.', 'Un Timer actualiza el modelo con un reloj monótono. El primer coche aparece inmediatamente; los siguientes cada 20 segundos. Cada tres aciertos reduce dos segundos el intervalo, hasta un mínimo de dos.', 'Coches en cola dibujados sin pintar con una etiqueta del color solicitado; el último coche atendido aparece pintado con su color. Puntuación, tiempo, cuenta regresiva del siguiente coche y récord.', 'Pulsa Iniciar partida y, en la paleta, el color de la etiqueta del primer coche. La captura muestra 45 segundos de partida: el coche atendido ya pintado y dos coches esperando con su etiqueta de color. Un color incorrecto no elimina el coche. Al llegar a cinco finaliza y se guarda el récord en LocalAppData.'),
('C3', 'Estacionamiento de autos', 'Controlar autos en un estacionamiento sin cupo fijo y cobrar dos pesos por segundo completo.', 'Placas y propietario; hora de entrada y salida tomadas del sistema.', 'Inserta cada auto como nodo de una cola circular doblemente ligada. Salir retira el frente, repara enlaces y calcula segundos transcurridos por 2.00.', 'Ventana "ENTRADA DE AUTO" que confirma cada ingreso; tabla de autos y ventana "SALIDA DE AUTO" con placas, propietario, horas, tiempo y costo.', 'Registra ABC-123 y XYZ-987 con la opción 1. Entrada de auto; cada ingreso se confirma con un mensaje. Pulsa 2. Salida de autos: la captura muestra el recibo del primero y el segundo todavía en cola. Se rechazan placas repetidas y salida con estacionamiento vacío.')
]
for codigo, titulo, problema, entradas, proceso, salidas, pasos in ejercicios:
    story.append(PageBreak())
    p(f'{codigo}. {titulo}', 'Heading1')
    for etiqueta, texto in [('Problema', problema), ('Entradas', entradas), ('Proceso', proceso), ('Salidas', salidas), ('Funcionamiento y evidencia', pasos)]:
        p(f'{etiqueta}: {texto}')
    story.append(Spacer(1, 8))
    story.append(Image(str(BASE / 'evidencias-csharp' / f'{codigo}.png'), width=505, height=318))

story.append(PageBreak())
p('Validación y pruebas', 'Heading1')
p('La suite verifica rangos, decimales, listas, orden de las pilas, colas vacías y llenas, tiempos controlados, récord y enlaces circulares. Compara 200 sumas de números grandes con BigInteger y recorre mil nodos de estacionamiento. También ejecuta los flujos de los doce ejercicios mediante sus botones antes de capturar evidencias.')
for linea in (BASE / 'pruebas-csharp.txt').read_text(encoding='utf-8-sig').splitlines():
    p(linea)

def pie(c, doc):
    c.setFont('Arial', 9)
    c.setFillColor(colors.HexColor('#1b3457'))
    c.drawString(40, 24, 'Unidad II - C# / Windows Forms')
    c.drawRightString(555, 24, str(doc.page))

SimpleDocTemplate(str(BASE / 'documentacion' / 'Documentacion_CSharp.pdf'), rightMargin=40, leftMargin=40, topMargin=35, bottomMargin=40, title='Práctica Unidad II - C#').build(story, onFirstPage=pie, onLaterPages=pie)
