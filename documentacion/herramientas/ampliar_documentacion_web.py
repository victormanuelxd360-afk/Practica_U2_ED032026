"""Conserva el desarrollo existente y añade la portada y una guía real del código."""
from pathlib import Path
from io import BytesIO
from html import escape
import json
import re
import subprocess
from PIL import Image as PILImage
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from contenido_codigo_web import EJERCICIOS_DETALLADOS

BASE = Path(__file__).resolve().parents[2]
SALIDA = BASE / 'documentacion/Documentacion_WEB.pdf'
AZUL = HexColor('#173c60')
VERDE = HexColor('#11685d')
GRIS = HexColor('#405362')

def generar():
    datos = json.loads((BASE / 'documentacion/datos_portada.json').read_text(encoding='utf-8-sig'))
    fuente = (BASE / 'CSharp/Modelos.cs').read_text(encoding='utf-8-sig')
    archivos = ['CSharp/Modelos.cs', 'Web/Estado.cs', 'WebPublica/Program.cs', 'WebPublica/wwwroot/motor.js', 'Web/wwwroot/app.js']
    fuentes = {a: (BASE / a).read_text(encoding='utf-8-sig') for a in archivos}
    for e in EJERCICIOS_DETALLADOS:
        assert re.sub(r'\s+', '', e['codigo']) in re.sub(r'\s+', '', fuente), f"Fragmento distinto al código real: {e['id']}"
        for ancla in e['anclas']:
            assert ancla in fuente, ancla

    original = PdfReader(BytesIO(SALIDA.read_bytes()))
    assert len(original.pages) >= 15, 'Se necesita el desarrollo web original de 15 páginas.'
    ancho, alto = map(float, (original.pages[0].mediabox.width, original.pages[0].mediabox.height))
    tmp = BASE / 'tmp/pdfs'
    tmp.mkdir(parents=True, exist_ok=True)
    respaldo = tmp / 'Documentacion_WEB_antes_de_ampliacion.pdf'
    if not respaldo.exists():
        respaldo.write_bytes(SALIDA.read_bytes())

    portada = BytesIO()
    c = canvas.Canvas(portada, pagesize=(ancho, alto))
    imagen = BASE / 'documentacion/Portada_equipo.png'
    with PILImage.open(imagen) as img:
        iw, ih = img.size
    escala = min(ancho / iw, alto / ih)
    c.drawImage(str(imagen), (ancho-iw*escala)/2, (alto-ih*escala)/2, width=iw*escala, height=ih*escala)
    c.showPage(); c.save(); portada.seek(0)

    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle('TextoGuia', fontName='Arial', fontSize=10, leading=14.3, textColor=GRIS, spaceAfter=8))
    estilos.add(ParagraphStyle('PequenoGuia', fontName='Arial', fontSize=8.2, leading=11.1, textColor=GRIS, spaceAfter=6))
    estilos.add(ParagraphStyle('TituloGuia', fontName='ArialBold', fontSize=20, leading=24, textColor=AZUL, spaceAfter=13))
    estilos.add(ParagraphStyle('SubGuia', fontName='ArialBold', fontSize=11.5, leading=15, textColor=VERDE, spaceBefore=7, spaceAfter=7))
    estilos.add(ParagraphStyle('EtiquetaGuia', fontName='ArialBold', fontSize=8.5, leading=12, textColor=VERDE, spaceAfter=9))
    estilos.add(ParagraphStyle('CodigoGuia', fontName='Consolas', fontSize=8.3, leading=11.5, textColor=AZUL, backColor=HexColor('#f0f4f8'), borderPadding=9, spaceAfter=12))
    contenido = []
    indice = []

    def p(texto, estilo='TextoGuia'):
        contenido.append(Paragraph(escape(texto), estilos[estilo]))

    def titulo(texto):
        if contenido: contenido.append(PageBreak())
        indice.append(texto)
        p('GUÍA DEL CÓDIGO / VERSIÓN WEB', 'EtiquetaGuia')
        p(texto, 'TituloGuia')

    def sub(texto): p(texto, 'SubGuia')

    def tabla(filas, anchos=None):
        celdas = [[Paragraph(escape(str(celda)), estilos['PequenoGuia']) for celda in fila] for fila in filas]
        t = Table(celdas, colWidths=anchos, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),HexColor('#e5eef4')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('LINEBELOW',(0,0),(-1,0),0.7,AZUL),
            ('LINEBELOW',(0,1),(-1,-1),0.35,HexColor('#dce4e9')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f8fafb')])
        ]))
        contenido.append(t); contenido.append(Spacer(1,9))

    def referencia(archivo, ancla):
        texto = fuentes[archivo]
        assert ancla in texto, (archivo, ancla)
        return texto[:texto.index(ancla)].count('\n')+1

    titulo('Cómo consultar y explicar este trabajo')
    p('El desarrollo y las evidencias de los doce ejercicios se conservan en las páginas 2 a 15. Esta guía amplía la explicación del código que realmente ejecuta la práctica: estructuras utilizadas, métodos, datos que reciben, decisiones, resultados y ejemplos que pueden reproducirse durante la exposición.')
    tabla([['Parte del documento','Páginas'],['Portada enviada por el equipo','1'],['Desarrollo y evidencias originales','2 a 13'],['Pruebas y decisiones del desarrollo','14 y 15'],['Arquitectura, interfaz y conceptos comunes','16 a 20'],['Explicación de los doce ejercicios','21 a 44'],['Tiempo del juego, servidor, pruebas y exposición','45 a 49'],['Mapa de archivos y líneas de inicio','50']], [355,150])
    sub('Cómo leer cada ejercicio')
    p('La primera página identifica la estructura de datos, explica los métodos y presenta un fragmento real del programa. La segunda recorre una ejecución con un ejemplo, muestra el estado de los datos y explica las validaciones. Al final incluye una explicación breve que puede adaptarse a la exposición oral.')
    sub('Datos del equipo')
    p(datos['integrantes'])
    p(f"Grupo: {datos['grupo']}. Docente: {datos['docente']}. Fecha de entrega: {datos['fecha_entrega']}.")
    sub('Qué representa un fragmento de código')
    p('Los fragmentos se contrastan automáticamente con CSharp/Modelos.cs. Sólo se ajustan sus saltos de línea para que se lean en la página. No son pseudocódigo ni una implementación diferente. Las tablas de recorrido son ejemplos didácticos; los valores aleatorios de las capturas pueden variar.')

    titulo('Arquitectura: qué hace cada archivo')
    tabla([['Archivo','Responsabilidad'],['CSharp/Modelos.cs','Contiene Producto, Alumno, Almacen, Grupo, Compra, Algoritmos, Cola<T>, Banco, Juego y los nodos del estacionamiento. Aquí se resuelven los ejercicios.'],['Web/Estado.cs','Conserva las instancias de los modelos, interpreta módulo y acción, llama al método adecuado y prepara Vista(), que devuelve el estado actual.'],['WebPublica/Program.cs','Arranca Blazor WebAssembly y expone Consultar, Ejecutar y RestaurarRecord para que JavaScript llame al código C#.'],['WebPublica/wwwroot/motor.js','Espera a Blazor.start, usa DotNet.invokeMethodAsync y guarda o recupera el récord del navegador.'],['Web/wwwroot/app.js','Construye formularios, captura eventos, pide operaciones y dibuja tablas, listas, coches y mensajes. Se reutiliza en la publicación.'],['Web/Program.cs','Aloja la variante ASP.NET Core. Expone las rutas HTTP y conserva un Estado por sesión de navegador.']], [178,327])
    sub('Recorrido de la versión pública')
    p('Formulario HTML > app.js > motor.js > MotorWeb.Ejecutar > Estado.Ejecutar > modelo C# > Estado.Vista > JSON > render de app.js > pantalla.')
    p('GitHub Pages entrega archivos estáticos. El motor .NET se descarga y se ejecuta dentro del navegador gracias a WebAssembly. No hay un servidor C# de GitHub Pages atendiendo cada clic: los algoritmos C# se ejecutan en el dispositivo de quien abre la página.')
    sub('Por qué compartir los modelos')
    p('Los proyectos incluyen Modelos.cs y Estado.cs mediante referencias Compile. Esto permite reutilizar la misma lógica sin copiar cada algoritmo a otra implementación en JavaScript. Cambiar una regla en el modelo afecta a los proyectos que se vuelvan a compilar con esa fuente.')

    titulo('Del clic al resultado: funciones de la interfaz')
    for nombre, descripcion in [
        ('choose(m)', 'Selecciona el ejercicio, actualiza el título, la descripción, los campos y los botones. No crea un modelo C# nuevo; por eso cambiar de pestaña conserva los datos de los ejercicios.'),
        ('act(action, label)', 'Lee FormData del formulario, identifica el módulo y construye un objeto con modulo, accion y valores. En el juego añade el color del botón. Usa busy y deshabilita botones mientras procesa una operación para evitar clics simultáneos.'),
        ('sendAction(solicitud)', 'Si existe practicaMotorReady, espera el motor WebAssembly y ejecuta su acción. En la variante ASP.NET envía un POST a /api/accion con JSON y la cabecera X-Practica.'),
        ('MotorWeb.Ejecutar(json)', 'Convierte el JSON a una Solicitud de C#, valida tamaño y valores, llama a Estado.Ejecutar y devuelve mensaje y estado serializados. Los errores de validación se convierten en un objeto error.'),
        ('Estado.Ejecutar(s)', 'El switch combina módulo y acción, por ejemplo L1/retirar o P3/sumar. Obtiene los valores por nombre, los valida y llama únicamente al modelo que corresponde al ejercicio.'),
        ('Vista() y render()', 'Vista prepara datos de salida y copias de las colecciones. render toma ese estado y dibuja el resultado del ejercicio seleccionado. La pantalla presenta lo que decidió el modelo, en vez de calcular por su cuenta la suma o la cola.'),
        ('refresh()', 'Consulta el estado actual. Un setInterval pide esta actualización cada segundo cuando el juego está seleccionado. No significa que el algoritmo del juego avance exactamente una vez por segundo; el modelo usa el tiempo real transcurrido.')]:
        sub(nombre); p(descripcion)
    p('JSON es el formato de intercambio: permite representar datos como objetos, listas, números y texto. Serializar convierte los objetos C# a JSON; deserializar reconstruye la Solicitud recibida.', 'PequenoGuia')

    titulo('Validaciones y tipos de datos')
    tabla([['Función o tipo','Qué hace y por qué importa'],['Validar.Texto(valor)','Rechaza null, cadena vacía y sólo espacios; después aplica Trim para quitar espacios exteriores. No elimina los espacios interiores de un nombre.'],['Validar.Entero(valor, min, max)','Usa int.TryParse. Distingue una conversión fallida de un entero que sí pudo leerse pero quedó fuera de rango. Se usa para cantidades, capacidad y elementos de pila.'],['Validar.Decimal(valor, min, max)','Sustituye coma por punto y analiza con cultura invariante. Admite signo inicial y separador decimal, sin interpretar separadores de miles. Comprueba el rango antes de devolver el valor.'],['decimal','Se usa en dinero y calificaciones. Mantiene precisión decimal para cantidades como 15.50 y 32.75. La interfaz muestra dinero con dos decimales.'],['string','Conserva texto y los operandos grandes. SumarGrandes no convierte toda la cadena a int: sólo convierte cada dígito individual.'],['int y long','int guarda contadores y valores enteros. long permite contar milisegundos y segundos con un rango mayor en la temporización.'],['DateTime y TickCount64','DateTime representa una hora del sistema para banco y estacionamiento. TickCount64 es un reloj de tiempo transcurrido, apropiado para programar llegadas del juego.']], [168,337])
    sub('Cómo se muestra un error')
    p('El modelo lanza ArgumentException con un mensaje comprensible cuando no puede cumplir una regla. El motor o la API capturan esa excepción y la interfaz la muestra en el estado del formulario. Un OverflowException produce un mensaje específico de rango numérico.')
    p('Una validación correcta ocurre antes de modificar la colección cuando sea posible. Por ejemplo, no se agrega un producto con clave duplicada y no se elimina el frente del juego si el color solicitado es incorrecto.')

    titulo('Listas, pilas y colas: conceptos que usamos')
    tabla([['Estructura','Operaciones del código','Regla'],['List<T>','Add, Remove, Find, Where, OrderBy','Guarda una secuencia. Permite buscar o eliminar por una condición; no impone FIFO ni LIFO.'],['Stack<T>','Push, Pop, Count y construcción desde una secuencia','LIFO: el último que entra sale primero. Enumerar una Stack muestra primero su cima.'],['Queue<T>','Enqueue, Dequeue, Peek','FIFO: se agrega al final y se retira del frente. La clase Cola<T> añade comprobaciones de cupo.'],['SortedDictionary<K,V>','ContainsKey, acceso por clave y Add a su lista','Relaciona cada inicial con una lista. Ordena las claves, no necesariamente los elementos de cada lista.'],['Nodo circular doble','Anterior, Siguiente y frente','Conecta cada nodo en dos sentidos y cierra el circuito. Requiere mantener los enlaces al insertar y retirar.']], [123,167,215])
    sub('Qué significan las expresiones del código')
    p('Count es la cantidad de elementos. Una comparación como x == viejo comprueba igualdad. El operador % obtiene el residuo; / entre enteros descarta la parte fraccionaria. La expresión condición ? a : b elige uno de dos valores. ?? usa la alternativa cuando el resultado de la izquierda es null.')
    p('Una expresión lambda, como p => p.Clave == clave, representa una regla que recibe un producto y devuelve una condición. Where selecciona elementos; Any pregunta si existe alguno; Sum suma valores. ToList o ToArray crean una colección materializada para usarla después.')
    sub('Orientación a objetos en esta práctica')
    p('Un record como Producto o Cliente reúne datos de un elemento. Una clase como Banco mantiene su propia colección y las operaciones permitidas sobre ella. El controlador coordina las clases, y la interfaz se encarga de capturar y presentar. Esta división ayuda a explicar y probar los algoritmos por separado.')

    for e in EJERCICIOS_DETALLADOS:
        titulo(f"{e['id']}. {e['titulo']}: métodos")
        p(e['clase'], 'EtiquetaGuia')
        p(e['estructura'])
        for metodo, descripcion in e['metodos']:
            sub(metodo); p(descripcion)
        sub('Fragmento real que conviene explicar')
        contenido.append(Preformatted(e['codigo'], estilos['CodigoGuia']))
        lineas = [str(referencia('CSharp/Modelos.cs', ancla)) for ancla in e['anclas']]
        p('Fuente: CSharp/Modelos.cs. Líneas de inicio de las declaraciones relacionadas: ' + ', '.join(lineas) + '.', 'PequenoGuia')

        titulo(f"{e['id']}. Recorrido y ejemplo para exponer")
        for i, paso in enumerate(e['pasos'],1):
            p(f'{i}. {paso}')
        sub('Estado de los datos durante la ejecución')
        ncols = len(e['tabla'][0])
        tabla(e['tabla'], [505/ncols]*ncols)
        sub('Validaciones y límites')
        p(e['errores'])
        sub('Cómo explicarlo con nuestras palabras')
        p(e['oral'])
        p('Evidencia relacionada: la captura de este ejercicio aparece en el desarrollo inicial y en evidencias-web/publica/' + e['id'] + '.png.', 'PequenoGuia')

    titulo('Juego: entender los tiempos y la dificultad')
    contenido.append(Preformatted('public long Intervalo =>\n    Math.Max(2000, 20000 - Pintados * 2000L);', estilos['CodigoGuia']))
    p('Los valores están en milisegundos: 1000 milisegundos equivalen a un segundo. 20000 representa 20 segundos y 2000 representa dos. La L al final del literal numérico hace explícito el tipo long. Math.Max impide que al acumular muchos aciertos el intervalo llegue a cero o sea negativo.')
    sub('Por qué usamos Math.Min para la siguiente llegada')
    tabla([['Ejemplo','Cálculo','Efecto'],['Primer acierto a los 0.1 segundos','min(20, 0.1 + 18) = 18.1','La primera llegada pendiente se adelanta a 18.1 segundos.'],['Primer acierto a los 3 segundos','min(20, 3 + 18) = 20','Se mantiene la llegada ya prevista a los 20 segundos.'],['La pestaña estuvo detenida por el navegador','Actualizar revisa todas las llegadas vencidas','El while agrega los coches pendientes hasta ponerse al día o terminar la partida.']], [140,185,180])
    p('Reducir el intervalo no significa conceder siempre un intervalo completo nuevo desde el clic: si ya había una llegada más cercana, ésta se conserva. Esta decisión hace que un acierto nunca retrase la presión de la cola.')
    sub('Partida y récord son datos diferentes')
    p('Pintados pertenece a la partida actual y se reinicia al comenzar. Record y TiempoRecord se conservan. GuardarRecord los actualiza al superar el puntaje anterior y, al terminar con ese mismo puntaje, registra el tiempo hasta el fin. No se implementa una clasificación global de jugadores ni un criterio de menor tiempo para desempatar.')
    p('En la web pública, motor.js recuerda esos dos valores con localStorage y los restaura al arrancar. No guarda los coches ni las listas completas. Al recargar la página se inicia un estado nuevo para los ejercicios, con el récord recuperado si el navegador permite almacenamiento.')

    titulo('Variante ASP.NET: rutas y sesiones')
    p('La copia local incluida en Publicacion no usa el motor WebAssembly para las operaciones: ejecuta una aplicación ASP.NET Core. La misma interfaz envía solicitudes HTTP al servidor local. Los modelos y reglas son los mismos, pero cambia el lugar de ejecución.')
    tabla([['Componente','Funcionamiento'],['GET /api/estado','Obtiene la sesión y devuelve Vista. La interfaz lo utiliza al iniciar y al actualizar el juego. No realiza una inserción solicitada por el usuario, aunque Vista sí actualiza las llegadas del juego según el reloj.'],['POST /api/accion','Recibe la Solicitud, exige X-Practica = 1 y valida el tamaño de los valores. Llama a Estado.Ejecutar y responde con mensaje y estado. Los errores de validación devuelven HTTP 400.'],['Sesion(context, cache)','Busca un identificador de cookie válido. Si no existe un Estado asociado, crea un identificador aleatorio y un Estado nuevo. No comparte las listas entre todos los navegadores.'],['Cookie y MemoryCache','La cookie es HttpOnly y SameSite Strict; Secure se usa cuando la solicitud es HTTPS. La caché conserva hasta 1000 sesiones, con expiración deslizante de dos horas de inactividad. No es una base de datos.'],['lock(estado)','Evita que dos solicitudes modifiquen el mismo Estado simultáneamente. Vista toma copias de las colecciones mutables para preparar la respuesta.']], [150,355])
    sub('Diferencias que hay que explicar correctamente')
    p('En GitHub Pages los modelos viven en el navegador de cada usuario. En ASP.NET viven en el proceso del servidor. En la primera variante las horas se obtienen en el dispositivo del navegador; en la segunda se obtienen en el servidor. Cerrar o reiniciar un servidor elimina sus estados en memoria.')
    p('Abrir INICIAR_LOCAL.cmd inicia el ejecutable portable con su carpeta Publicacion como directorio de trabajo, espera a que responda y abre el navegador. La ventana de control permite detener esa instancia pulsando Enter.')

    titulo('Qué comprobamos y qué demuestra cada prueba')
    p('La documentación usa los resultados guardados de las ejecuciones reales, no una lista de pruebas inventada. No es necesario volver a compilar el programa para cambiar la portada o ampliar esta explicación.')
    tabla([['Evidencia','Qué verifica'],['pruebas-web.txt','22 verificaciones HTTP: operaciones de los doce ejercicios, valores límite, productos y placas, sobreflujo del banco, entrada inválida, aislamiento de sesiones y cabecera de solicitudes. Incluye el intervalo de 20 segundos tras el primer acierto.'],['pruebas-publica.txt','Los doce ejercicios se ejecutaron desde sus controles en el navegador con C# WebAssembly. Se confirmó también la reducción de 20 a 20 segundos.'],['evidencias-web/publica','Imágenes capturadas después de realizar las operaciones. El código del modelo produce los resultados; las imágenes permiten comprobar cómo se presentan al usuario.'],['CSharp/Pruebas.cs','Suite de modelos e interfaz de escritorio. Incluye sumas comparadas con BigInteger como oráculo, FIFO, tiempos controlados y comprobación de enlaces al insertar y retirar nodos. Su registro histórico de escritorio no sustituye las pruebas web.']], [155,350])
    sub('Casos útiles para demostrar en clase')
    for texto in ['Calificación 7 aprueba y 6.99 reprueba, sin redondear la comparación.', 'Sumar una cadena de muchos nueves y uno produce un uno seguido de ceros; muestra el acarreo final.', 'Agregar dos clientes y atender una vez retira al primero, no al que se escribió más recientemente.', 'Pintar con el color equivocado mantiene la cola y el marcador. Un acierto cambia el intervalo.', 'Insertar dos autos y sacar ambos comprueba el caso de varios nodos y el caso especial del último nodo.']:
        p('• ' + texto)
    p('Probar no significa únicamente que la pantalla abra: también debemos comprobar que los datos cambian como se espera y que los errores no dejan la estructura en un estado incorrecto.')

    titulo('Guion práctico para la exposición del equipo')
    sub('Introducción común')
    p('Esta práctica resuelve doce problemas mediante listas, pilas y colas. Separamos los datos y los algoritmos de los formularios. La versión pública ejecuta el código C# en el navegador y la alternativa local utiliza ASP.NET Core.')
    sub('Orden para presentar cualquier ejercicio')
    for i, texto in enumerate(['Explicar el problema en una frase y mencionar los datos que se capturan.', 'Identificar la clase y la estructura utilizada: List, Stack, Queue o nodos enlazados.', 'Abrir el método principal y describir el orden de las instrucciones. Indicar qué regla decide el resultado.', 'Mostrar un ejemplo pequeño y decir cómo cambian los datos, no sólo leer el mensaje final.', 'Probar un caso inválido y explicar qué validación lo detiene.', 'Cerrar explicando por qué la estructura elegida ayuda a resolver ese problema.'],1): p(f'{i}. {texto}')
    sub('Reparto sugerido, ajustable por el equipo')
    tabla([['Integrante','Ejercicios para preparar'],['Santiago Nicolás De la Mora Núñez','L1, L2 y L3: productos, paridad y alumnos.'],['Jesus Joel Canche Chac','L4, L5 y P1: compra, grupos por inicial e inversión.'],['Roger Alejandro Aguilar Nuñez','P2, P3 y P4: palíndromos, suma y reemplazo.'],['Víctor Manuel Almendarez García','C1, C2 y C3: banco, juego y estacionamiento.']], [237,268])
    p('Es una propuesta de organización, no un registro de quién programó cada módulo. Todos deben comprender el recorrido general y la diferencia entre las dos variantes web.')
    sub('Antes de exponer')
    p('Tener abierta la web, ubicar Modelos.cs y el método correspondiente, elegir datos pequeños y ensayar el caso de error. En el juego no hace falta esperar muchos coches para demostrar la dificultad: el primer acierto ya cambia el intervalo de 20 a 20 segundos.')

    titulo('Preguntas frecuentes y vocabulario')
    for pregunta, respuesta in [
        ('¿Por qué no sumar los operandos grandes con int?', 'Porque una cadena con cientos o miles de dígitos excede su rango. La solución almacena dígitos individuales en pilas y maneja un acarreo pequeño.'),
        ('¿Por qué dos pasadas en Reemplazar?', 'La primera revisa y modifica mientras invierte el orden. La segunda restaura ese orden; por eso la cima final sigue representando la cima original con los valores sustituidos.'),
        ('¿Por qué el estacionamiento no usa simplemente Queue?', 'El ejercicio exige una cola circular doblemente ligada. Los nodos, sus dos enlaces y los casos de inserción y eliminación están programados explícitamente.'),
        ('¿El tiempo de espera y el costo son aleatorios?', 'No. Se calculan restando las horas guardadas a la hora actual. Sólo cantidades y precios de productos, números de paridad y colores del juego se generan aleatoriamente.'),
        ('¿Qué es una instancia?', 'Es un objeto concreto creado a partir de una clase. Por ejemplo, cada Estado contiene su propia instancia de Banco, con sus clientes y su contador de turnos.'),
        ('¿Qué significa genérico, como Cola<T>?', 'T representa el tipo de elemento. La misma clase puede almacenar Cliente o Coche conservando las operaciones de cola y las comprobaciones de capacidad.'),
        ('¿Qué es un nodo?', 'Es el objeto que reúne un dato y referencias a otros nodos. En el estacionamiento incluye un Auto y los enlaces Anterior y Siguiente.'),
        ('¿Qué parte conserva datos después de recargar?', 'En la versión pública sólo el récord y su tiempo se guardan con localStorage. Las listas y las colas se reinician; no hay una base de datos persistente de alumnos, productos o clientes.')]:
        sub(pregunta); p(respuesta)

    titulo('Mapa de métodos en el código entregado')
    p('Estas referencias indican la línea donde comienza una declaración en CSharp/Modelos.cs. No son números de página del informe ni una lista de todos los archivos. Permiten encontrar rápidamente la clase o el método al explicar el programa.')
    filas = [['Ejercicio','Clase o métodos principales','Líneas de inicio']]
    for e in EJERCICIOS_DETALLADOS:
        filas.append([e['id'],e['clase'],', '.join(str(referencia('CSharp/Modelos.cs', a)) for a in e['anclas'])])
    tabla(filas,[65,320,120])
    tabla([['Archivo','Declaración','Línea'],['Web/Estado.cs','Ejecutar(Solicitud s)',str(referencia('Web/Estado.cs','public string Ejecutar'))],['Web/Estado.cs','Vista()',str(referencia('Web/Estado.cs','public object Vista'))],['WebPublica/Program.cs','MotorWeb',str(referencia('WebPublica/Program.cs','public static class MotorWeb'))],['Web/wwwroot/app.js','act(action, label)',str(referencia('Web/wwwroot/app.js','async function act('))],['Web/wwwroot/app.js','render()',str(referencia('Web/wwwroot/app.js','function render('))]], [185,230,90])
    p('Los números se calculan directamente de los archivos al regenerar el informe. Si se agregan líneas al programa en el futuro, hay que regenerar también esta guía. La documentación describe el comportamiento del código entregado y las decisiones actuales; no atribuye persistencia ni capacidades que la aplicación no implementa.')

    def pie(pdf, doc):
        pdf.setStrokeColor(HexColor('#d8e3eb')); pdf.line(45,41,ancho-45,41)
        pdf.setFont('Arial',8); pdf.setFillColor(GRIS)
        pdf.drawString(45,27,'Estructura de Datos / Unidad II / Explicación del código C#')
        pdf.drawRightString(ancho-45,27,str(doc.page+15))

    anexo = BytesIO()
    doc = SimpleDocTemplate(anexo,pagesize=(ancho,alto),leftMargin=45,rightMargin=45,topMargin=42,bottomMargin=54)
    doc.build(contenido,onFirstPage=pie,onLaterPages=pie)
    anexo.seek(0)
    lector_anexo = PdfReader(anexo)
    assert len(lector_anexo.pages) == len(indice), f'Desbordamiento de sección: {len(lector_anexo.pages)} páginas para {len(indice)} secciones'
    escritor = PdfWriter()
    escritor.add_page(PdfReader(portada).pages[0])
    for pagina in original.pages[1:15]: escritor.add_page(pagina)
    for pagina in lector_anexo.pages: escritor.add_page(pagina)
    escritor.add_metadata({'/Title':'Práctica Unidad II - Web - Código explicado','/Author':datos['integrantes'],'/Subject':'Listas, pilas y colas en C#; grupo 4.º A'})
    escritor.add_outline_item('Portada del equipo',0)
    escritor.add_outline_item('Desarrollo y evidencias',1)
    padre = escritor.add_outline_item('Guía detallada del código',15)
    for i, texto in enumerate(indice): escritor.add_outline_item(texto,i+15,parent=padre)
    temporal = tmp / 'Documentacion_WEB.actualizado.pdf'
    with temporal.open('wb') as f: escritor.write(f)
    verificacion = PdfReader(temporal)
    texto = '\n'.join(p.extract_text() or '' for p in verificacion.pages[15:])
    for e in EJERCICIOS_DETALLADOS: assert e['titulo'] in texto, e['id']
    for nombre in ['Víctor Manuel Almendarez García','Santiago Nicolás De la Mora Núñez','Jesus Joel Canche Chac','Roger Alejandro Aguilar Nuñez']:
        assert nombre in texto, nombre
    assert 'Pendiente de completar' not in '\n'.join(p.extract_text() or '' for p in verificacion.pages)
    SALIDA.write_bytes(temporal.read_bytes())
    (tmp/'indice-guia.txt').write_text('\n'.join(f'{i+16}. {s}' for i,s in enumerate(indice)),encoding='utf-8')
    print(f'PDF verificado: {len(verificacion.pages)} páginas; 12 ejercicios, portada y guía de código. {SALIDA}')

if __name__ == '__main__':
    generar()
