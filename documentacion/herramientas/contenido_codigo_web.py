"""Explicación didáctica contrastada con los modelos C# de la práctica."""
EJERCICIOS_DETALLADOS = [
dict(id='L1', titulo='Productos disponibles y retirados', clase='Producto y Almacen',
 anclas=['public record Producto', 'public Producto Escanear()', 'public void Retirar(string clave)'],
 estructura='Dos List<Producto>: Disponibles representa el almacén actual y Retirados conserva el historial. Cada Producto es un record con Clave, Nombre, Cantidad y Precio.',
 metodos=[('Escanear()', 'Incrementa secuencia con ++ para generar una clave distinta, como P1. Construye el nombre producto1, obtiene una cantidad aleatoria de 1 a 20 y un precio de $1.00 a $500.00. Random.Shared.Next excluye el límite superior: por eso se usan 21 y 50001. Divide entre 100m para obtener un decimal monetario y agrega el objeto con Add.'),
 ('Retirar(clave)', 'Limpia la clave con Validar.Texto. Find recorre disponibles y compara sin distinguir mayúsculas. Si no encuentra el producto, ?? throw genera un error. Si existe, Remove lo quita de disponibles y Add incorpora el mismo objeto al historial; no se pierde su cantidad ni su precio.'),
 ('Presentación', 'Estado.Ejecutar conecta L1/escanear y L1/retirar con esos métodos. Vista devuelve copias de ambas listas y render dibuja dos tablas. Los contadores muestran el número de objetos Producto, no la suma de unidades del campo Cantidad.')],
 codigo='''string k = Validar.Texto(clave);
var p = Disponibles.Find(p => p.Clave.Equals(k,
    StringComparison.OrdinalIgnoreCase))
    ?? throw new ArgumentException(
        "Clave no encontrada entre disponibles.");
Disponibles.Remove(p);
Retirados.Add(p);''',
 pasos=['El botón Escanear envía el módulo L1 y la acción escanear. La primera llamada crea P1 y la segunda P2; sus cantidades y precios son aleatorios.', 'El usuario escribe P1 y pulsa Retirar por clave. El controlador pasa el texto a Almacen.Retirar.', 'Find localiza P1. Se elimina únicamente de Disponibles y se añade a Retirados. P2 permanece disponible.', 'Vista prepara el estado actualizado; la página vuelve a pintar las tablas y cambia los contadores a uno disponible y uno retirado.'],
 tabla=[['Operación','Disponibles','Retirados'],['Inicio','vacía','vacía'],['Escanear dos veces','P1, P2','vacía'],['Retirar P1','P2','P1']],
 errores='Una clave vacía se rechaza antes de buscar. Una clave inexistente o ya retirada muestra el mensaje correspondiente y no modifica ninguna lista.',
 oral='Usamos dos listas para distinguir la existencia actual del historial. Retirar no destruye el registro: lo mueve conservando sus datos. Podemos demostrarlo escaneando dos productos y retirando sólo P1.'),

dict(id='L2', titulo='Pares e impares', clase='Algoritmos.Clasificar',
 anclas=['public static (List<int> Original, List<int> Pares, List<int> Impares) Clasificar'],
 estructura='Tres List<int>: Original conserva cada número generado; Pares e Impares reciben copias de esos valores según su paridad. Se permiten repetidos.',
 metodos=[('Clasificar(cantidad)', 'Primero exige una cantidad entre 1 y 500. El ciclo for se repite exactamente cantidad veces. En cada vuelta Next(1000) genera un entero entre 0 y 999, lo añade a Original y lo coloca en una sola lista de clasificación.'),
 ('n % 2 == 0', 'El operador % calcula el residuo. Un residuo cero indica que n es divisible entre dos y, por tanto, es par. La expresión condicional elige Pares o Impares; Add guarda el número en la lista elegida.'),
 ('Resultado devuelto', 'El método devuelve una tupla con las tres listas. Estado convierte sus miembros en un objeto que se puede serializar. La interfaz muestra cada lista por separado sin perder el orden de generación dentro de cada grupo.')],
 codigo='''List<int> original = [], pares = [], impares = [];
for (int i = 0; i < cantidad; i++)
{
    int n = Random.Shared.Next(1000);
    original.Add(n);
    (n % 2 == 0 ? pares : impares).Add(n);
}
return (original, pares, impares);''',
 pasos=['Se lee la cantidad del formulario y Validar.Entero la convierte a un entero dentro del rango.', 'Por cada vuelta del for se genera un número. Original siempre recibe ese número, aunque ya exista otro igual.', 'La condición del residuo decide el destino. Como las opciones son excluyentes, cada número aparece en una sola de las dos listas de clasificación.', 'Al terminar, la suma de las cantidades de pares e impares coincide con la cantidad original. El ejemplo de abajo es ilustrativo: una ejecución real genera otros números.'],
 tabla=[['Número ilustrativo','Residuo entre 2','Destino'],['8','0','Pares'],['3','1','Impares'],['0','0','Pares'],['3','1','Impares; se conserva el repetido']],
 errores='Cero, cantidades mayores que 500, letras o cantidades decimales se rechazan antes de generar la lista. Generar otra vez sustituye el resultado anterior de este ejercicio.',
 oral='Recorremos los números una sola vez y usamos el residuo para separarlos. Comprobamos que ningún elemento se pierde: pares más impares debe ser igual al total generado.'),

dict(id='L3', titulo='Aprobados y reprobados', clase='Alumno y Grupo',
 anclas=['public record Alumno', 'public sealed class Grupo'],
 estructura='Alumno conserva Nombre y Calificacion como decimal. Grupo tiene dos List<Alumno>: Aprobados y Reprobados.',
 metodos=[('Agregar(nombre, nota)', 'Comprueba que la nota esté entre cero y diez y valida el nombre. Agrega inicialmente el alumno a Aprobados. Después busca dentro de esa lista a quienes tengan nota menor que siete y los traslada a Reprobados.'),
 ('Where(...).ToList()', 'Where selecciona únicamente las notas menores que siete. ToList crea una lista temporal de esos alumnos. Es importante porque se va a eliminar de la lista original: recorrer directamente una colección mientras se modifica puede invalidar su enumerador.'),
 ('Remove y Add', 'Por cada alumno seleccionado se ejecutan ambas operaciones. Al concluir, nadie con nota menor que siete permanece en Aprobados. Una nota igual a siete sí aprueba; no se redondea 6.99 para convertirla en siete.')],
 codigo='''Aprobados.Add(new Alumno(Validar.Texto(nombre), nota));
foreach (var a in Aprobados.Where(
    a => a.Calificacion < 7).ToList())
{
    Aprobados.Remove(a);
    Reprobados.Add(a);
}''',
 pasos=['La pantalla envía el nombre y la nota. Validar.Decimal admite punto o coma decimal, por ejemplo 8.5 y 8,5.', 'Se construye el record Alumno y se agrega a la lista de aprobados, que funciona como lista inicial de captura.', 'Si la nota es menor que siete, el foreach la encuentra en la selección temporal y mueve el alumno a la otra lista.', 'Vista devuelve las dos listas y render dibuja dos tablas. El mismo nombre puede capturarse más de una vez: esta versión no establece una matrícula única.'],
 tabla=[['Alumno','Nota','Lista final'],['Ana','7.00','Aprobados'],['Luis','6.99','Reprobados'],['Eva','10.00','Aprobados'],['Pedro','0.00','Reprobados']],
 errores='Un nombre vacío o una calificación fuera del intervalo 0 a 10 produce un mensaje sin agregar el alumno. El tipo decimal evita depender de aproximaciones binarias para comparar el límite de siete.',
 oral='La regla es menor que siete reprueba. La parte importante es que primero obtenemos una copia de los alumnos que vamos a mover; así no modificamos la misma lista que estamos enumerando.'),

dict(id='L4', titulo='Eliminar y ordenar productos', clase='Compra y Producto',
 anclas=['public sealed class Compra', 'public List<Producto> Ordenados()', 'public decimal Total()'],
 estructura='Compra mantiene una List<Producto>. En este ejercicio cada registro representa un producto con cantidad uno; el precio de cada registro contribuye al total.',
 metodos=[('Agregar(clave, nombre, precio)', 'Valida la clave y comprueba con Any que no exista otra equivalente, sin distinguir mayúsculas. Rechaza precios negativos y nombres vacíos. Sólo después agrega un Producto a la lista. El controlador también impide que el total exceda el rango de decimal.'),
 ('Eliminar(clave)', 'RemoveAll retira las coincidencias de la clave. Como las claves son únicas, normalmente elimina un solo producto. El valor devuelto es el número de eliminaciones; si es cero, se informa que la clave no existe.'),
 ('Ordenados() y Total()', 'OrderBy construye una vista ordenada por nombre con comparación de español de México e ignorando mayúsculas. ToList la materializa sin ordenar físicamente la lista original. Sum suma todos los precios como decimal, y la pantalla los presenta con dos decimales.')],
 codigo='''string k = Validar.Texto(clave);
if (Productos.RemoveAll(p => p.Clave.Equals(k,
    StringComparison.OrdinalIgnoreCase)) == 0)
    throw new ArgumentException("Clave no encontrada.");''',
 pasos=['Se capturan clave, nombre y precio. Agregar comprueba sus reglas y guarda el producto.', 'Cada respuesta usa Ordenados para que la tabla se presente por nombre, aunque los productos se hayan capturado en otro orden.', 'Total vuelve a calcular la suma a partir de la lista actual. Por eso eliminar un producto también cambia el total sin llevar una suma paralela que pueda quedar desactualizada.', 'Para eliminar basta con escribir una clave y pulsar Eliminar por clave. Los otros campos del formulario no son necesarios en esa operación.'],
 tabla=[['Acción','Tabla por nombre','Total'],['Agregar P1 Zanahoria 15.50','Zanahoria','15.50'],['Agregar P2 Arroz 32.75','Arroz, Zanahoria','48.25'],['Eliminar P2','Zanahoria','15.50']],
 errores='Se rechazan claves duplicadas, claves inexistentes al eliminar, precios negativos y textos faltantes. La validación de precio sólo corresponde a agregar; no debe impedir una eliminación por clave.',
 oral='Separar almacenar de presentar nos permite conservar la lista y mostrar una copia ordenada. El total se calcula desde los productos vigentes, así que nunca incluye un producto que ya eliminamos.'),

dict(id='L5', titulo='Palabras por letra', clase='Algoritmos.Agrupar',
 anclas=['public static SortedDictionary<string, List<string>> Agrupar'],
 estructura='Una lista conserva todas las palabras. Un SortedDictionary<string, List<string>> usa la letra inicial como clave y una lista de palabras como valor.',
 metodos=[('Agrupar(palabras)', 'Recorre las entradas, elimina espacios exteriores y exige que todos sus caracteres sean letras. EnumerateRunes permite trabajar con puntos de código Unicode, en lugar de separar a la mitad caracteres que ocupen más de una unidad UTF-16.'),
 ('Inicial y ContainsKey', 'Obtiene el primer Rune y lo convierte a mayúscula. Así Fresa y fresca se clasifican en F. Si esa inicial todavía no existe, crea una lista vacía; después añade la palabra al grupo.'),
 ('Coordinación y salida', 'Estado valida primero la nueva palabra usando Agrupar con una entrada. Si es válida, la añade al historial. Vista vuelve a agrupar el historial completo. El diccionario ordena las claves; no ordena alfabéticamente las palabras dentro de cada lista.')],
 codigo='''string inicial = p.EnumerateRunes().First()
    .ToString().ToUpperInvariant();
if (!grupos.ContainsKey(inicial)) grupos[inicial] = [];
grupos[inicial].Add(p);''',
 pasos=['Se captura una sola palabra, por ejemplo Fresa. El controlador valida antes de modificar la lista original.', 'El método identifica la inicial F. Como todavía no hay grupo F, crea una List<string> para esa clave.', 'Al agregar Fresca se encuentra la clave F existente y se reutiliza su lista. Al agregar Oso se crea una segunda lista bajo O.', 'La interfaz muestra la lista original y, debajo, todos los grupos que devuelve el diccionario. No hay una cantidad fija de iniciales programadas.'],
 tabla=[['Entrada','Clave','Contenido del grupo'],['Fresa','F','Fresa'],['Fresca','F','Fresa, Fresca'],['Oso','O','Oso'],['Orilla','O','Oso, Orilla']],
 errores='La cadena vacía, una frase con espacios interiores, un número o signos se rechazan. Los acentos se conservan; la versión no elimina tildes para fusionar iniciales. Las palabras repetidas se conservan como capturas independientes.',
 oral='La clave del diccionario nos dice qué lista utilizar. Si la inicial es nueva, creamos una lista; si ya existe, añadimos la palabra a la lista existente. Así el ejercicio se adapta a nuevas letras.'),

dict(id='P1', titulo='Invertir palabra', clase='Algoritmos.Invertir',
 anclas=['public static string Invertir(string entrada)'],
 estructura='Una Stack<Rune> almacena los caracteres. La pila trabaja como LIFO: el último elemento que entra es el primero que sale.',
 metodos=[('Invertir(entrada)', 'Valida y limpia el texto. El constructor de Stack recibe los Rune en el orden de lectura y los coloca en la pila; por eso el último carácter queda en la cima.'),
 ('Pop y StringBuilder', 'Mientras Count sea mayor que cero, Pop saca el elemento de la cima. StringBuilder.Append lo agrega al resultado sin construir una cadena nueva completa en cada vuelta. Cuando la pila queda vacía, ToString entrega el texto final.'),
 ('Qué se conserva', 'Se conserva cada punto de código Unicode completo. Esto evita romper un carácter como un emoji compuesto por un par sustituto, aunque no pretende tratar todas las secuencias combinadas de varios Rune como una sola unidad visual.')],
 codigo='''Stack<Rune> pila = new(
    Validar.Texto(entrada).EnumerateRunes());
StringBuilder r = new();
while (pila.Count > 0) r.Append(pila.Pop().ToString());
return r.ToString();''',
 pasos=['Se lee UTM y se valida que no sea una entrada vacía.', 'Los caracteres se apilan como U, después T y finalmente M. La cima queda en M.', 'El while desapila M y lo añade al resultado; luego hace lo mismo con T y con U.', 'La pila termina vacía y el resultado MTU se devuelve al controlador y a la pantalla. El método sólo utiliza la pila temporal, no cambia las listas de otros ejercicios.'],
 tabla=[['Extracción','Pila: cima a base','Resultado'],['Antes de extraer','M, T, U','vacío'],['Pop de M','T, U','M'],['Pop de T','U','MT'],['Pop de U','vacía','MTU']],
 errores='Una entrada vacía o formada únicamente por espacios produce un error. Validar.Texto recorta espacios al inicio y al final; los espacios interiores forman parte del texto invertido.',
 oral='No intercambiamos posiciones directamente en la cadena. Aprovechamos el comportamiento LIFO de la pila: lo último que leímos será lo primero que mostraremos.'),

dict(id='P2', titulo='Palíndromo', clase='Algoritmos.Palindromo e Invertir',
 anclas=['public static bool Palindromo(string entrada)', 'public static string Invertir(string entrada)'],
 estructura='La cadena normalizada se compara con una segunda cadena obtenida por inversión mediante Stack<Rune>. No se usa una lista para simular la pila.',
 metodos=[('Normalización', 'Validar.Texto comprueba la entrada. ToLowerInvariant elimina diferencias entre mayúsculas y minúsculas. Where(Rune.IsLetterOrDigit) conserva sólo letras y dígitos, quitando espacios y signos. string.Concat une los elementos filtrados.'),
 ('Comparación', 'Si la cadena normalizada queda vacía, se rechaza. Si contiene datos, se pasa a Invertir y se compara con ==. El resultado bool se convierte en un mensaje afirmativo o negativo dentro de Estado.Ejecutar.'),
 ('Decisión sobre acentos', 'Los acentos no se eliminan. La aplicación no presupone que una vocal acentuada sea igual a la misma vocal sin acento. Esta regla evita cambios implícitos en el texto y está documentada como una decisión de la implementación.')],
 codigo='''if (normal.Length == 0)
    throw new ArgumentException(
        "Introduce al menos una letra o número.");
return normal == Invertir(normal);''',
 pasos=['El usuario escribe Anita lava la tina. La comparación no se hace todavía sobre la frase original.', 'La normalización produce anitalavalatina: todas las letras quedan en minúsculas y los espacios desaparecen.', 'Invertir construye la secuencia en orden contrario usando una pila. Ambas cadenas resultan iguales.', 'Palindromo devuelve true y el controlador genera Sí es palíndromo. Con Casa se compara casa contra asac y se devuelve false.'],
 tabla=[['Entrada','Texto normalizado','Resultado'],['Anita lava la tina','anitalavalatina','Sí'],['12321','12321','Sí'],['Casa','casa','No'],['!!!','vacío','Error de validación']],
 errores='Los signos por sí solos no se aceptan como un palíndromo vacío. Las frases se admiten porque los espacios se eliminan antes de comparar; esa regla es distinta de la validación del ejercicio de palabras por inicial.',
 oral='Primero definimos qué caracteres cuentan para comparar. Luego reutilizamos el método de inversión con pila. La igualdad entre el texto limpio y su inversión determina el resultado.'),

dict(id='P3', titulo='Suma de números grandes', clase='Algoritmos.Digitos y SumarGrandes',
 anclas=['private static Stack<int> Digitos(string entrada)', 'public static string SumarGrandes(string a, string b)'],
 estructura='Tres Stack<int>: una por operando y otra para el resultado. Cada elemento guarda un dígito, no el número completo; por eso el tamaño no depende del rango de int o long.',
 metodos=[('Digitos(entrada)', 'Exige al menos un carácter y permite únicamente los caracteres ASCII de 0 a 9. c - \'0\' convierte cada carácter en un entero entre cero y nueve. El constructor apila los dígitos y deja las unidades en la cima.'),
 ('SumarGrandes(a, b)', 'Repite el ciclo mientras alguna pila tenga dígitos o quede acarreo. Si un operando ya se agotó, aporta cero. Cada suma parcial produce un dígito con n % 10 y el nuevo acarreo con la división entera n / 10.'),
 ('Pila resultado', 'Cada dígito calculado se apila. Como se calculan primero las unidades, al enumerar la pila terminada se obtiene el orden correcto. TrimStart quita ceros iniciales; si no queda ningún carácter, se devuelve la cadena 0. BigInteger se utiliza para pruebas, no para resolver esta suma.')],
 codigo='''while (p.Count > 0 || q.Count > 0 || acarreo > 0)
{
    int n = acarreo + (p.Count > 0 ? p.Pop() : 0)
        + (q.Count > 0 ? q.Pop() : 0);
    resultado.Push(n % 10);
    acarreo = n / 10;
}''',
 pasos=['Con 592 y 3784, las cimas iniciales son 2 y 4. Los operandos se conservan como cadenas y como pilas de dígitos, sin convertirlos a un entero grande del lenguaje.', 'Se extrae un dígito de cada pila, se suma junto con el acarreo y se guarda sólo la cifra de las unidades en la pila resultado.', 'Al agotarse un operando se sigue trabajando con el otro. Si después de los últimos dígitos queda un acarreo, el while hace una vuelta adicional.', 'Al finalizar se obtiene 4376. El mismo procedimiento permite sumar miles de dígitos; el límite práctico es la memoria y el límite de longitud del formulario, no el tipo numérico de un operando.'],
 tabla=[['Columna','Suma parcial','Dígito','Acarreo'],['Unidades','2 + 4 + 0 = 6','6','0'],['Decenas','9 + 8 + 0 = 17','7','1'],['Centenas','5 + 7 + 1 = 13','3','1'],['Millares','0 + 3 + 1 = 4','4','0']],
 errores='Se rechazan negativos, decimales, signos y letras. Los ceros iniciales sí se aceptan. La interfaz limita cada campo a 20000 caracteres: que el algoritmo no use un entero fijo no significa que el formulario sea ilimitado.',
 oral='Hacemos la misma suma por columnas que en papel, pero con pilas. El acarreo es la parte que pasa a la siguiente columna. Nunca intentamos meter el operando completo en un int.'),

dict(id='P4', titulo='Reemplazar valor', clase='Algoritmos.Reemplazar',
 anclas=['public static int Reemplazar(Stack<int> pila, int nuevo, int viejo)'],
 estructura='Se usa la pila recibida y una Stack<int> auxiliar. La auxiliar permite revisar todos los elementos y después recuperar el orden original.',
 metodos=[('Reemplazar(pila, nuevo, viejo)', 'Mientras la pila original tenga elementos, extrae su cima con Pop. Si el entero coincide con viejo, cambia la variable local a nuevo y aumenta el contador cambios. Después lo apila en auxiliar.'),
 ('Segundo recorrido', 'El primer traslado invierte el orden. El segundo while desapila la auxiliar y vuelve a apilar en la original, invirtiendo una segunda vez. Dos inversiones restauran el orden relativo de los elementos.'),
 ('Valor devuelto y referencias', 'El método devuelve la cantidad de sustituciones y modifica la misma pila recibida. No devuelve una pila nueva: Stack es un objeto de referencia. El controlador convierte la pila final a un arreglo para mostrarla de cima a base.')],
 codigo='''while (pila.Count > 0)
{
    int n = pila.Pop();
    if (n == viejo) { n = nuevo; cambios++; }
    auxiliar.Push(n);
}
while (auxiliar.Count > 0) pila.Push(auxiliar.Pop());
return cambios;''',
 pasos=['La entrada 1,2,3,2 se separa por comas y cada elemento se convierte a entero. Se apilan de izquierda a derecha, de modo que el último 2 queda en la cima.', 'Con viejo 2 y nuevo 9, cada aparición se sustituye al salir. Los elementos que no coinciden se conservan.', 'La pila auxiliar queda con el orden invertido. El segundo while la vacía hacia la original para recuperar el orden.', 'Se muestran la pila 9,3,9,1 desde la cima y el contador 2. Si el valor no aparece, el contador es cero y el orden permanece intacto.'],
 tabla=[['Momento','Cima a base','Cambios'],['Original','2, 3, 2, 1','0'],['Auxiliar al terminar el primer ciclo','1, 9, 3, 9','2'],['Original restaurada','9, 3, 9, 1','2']],
 errores='Una entrada como 1,,2 contiene un elemento vacío y se rechaza. Las letras o enteros fuera del rango de int también se rechazan. El método admite una pila vacía y devuelve cero, aunque el formulario pide al menos un valor.',
 oral='Si usáramos sólo una pila auxiliar, el resultado quedaría al revés. El segundo traslado es el que mantiene el orden y permite cambiar todas las coincidencias sin desordenar los demás valores.'),

dict(id='C1', titulo='Ventanilla de banco', clase='Cola<T>, Cliente y Banco',
 anclas=['public sealed class Cola<T>', 'public sealed class Banco', 'public Cliente Llegar'],
 estructura='Banco usa una Cola<Cliente> de capacidad limitada. Internamente Cola<T> encapsula una Queue<T>. Es FIFO: el cliente con mayor tiempo en la cola se atiende primero.',
 metodos=[('ColaLlena e InsertaCola', 'ColaLlena compara Count con Capacidad. InsertaCola comprueba esa condición antes de usar Enqueue, que agrega al final. La capacidad debe ser mayor que cero; el valor inicial de la pantalla es cinco.'),
 ('Llegar(nombre, movimiento, ahora)', 'Comprueba el cupo, valida nombre y movimiento y crea un Cliente con turno + 1 y la hora recibida. Después de insertar incrementa turno. De esta forma una inserción fallida no consume un número de turno.'),
 ('Atender(ahora)', 'EliminaCola rechaza la cola vacía; si hay clientes, Dequeue retira el frente. La espera se calcula restando Llegada a la hora de atención y tomando segundos completos. Frente usa Peek sin eliminar y Final obtiene el último elemento.')],
 codigo='''public (Cliente Cliente, long Segundos)
    Atender(DateTime ahora)
{
    var c = Clientes.EliminaCola();
    return (c, Math.Max(0,
        (long)(ahora - c.Llegada).TotalSeconds));
}''',
 pasos=['El usuario elige el movimiento en el selector y escribe el nombre. Estado sólo permite uno de los movimientos ofrecidos por la pantalla.', 'Al agregar, el cliente recibe un turno y DateTime.Now como hora de llegada. La tabla se actualiza y el cliente se forma al final.', 'Atender retira automáticamente el primer cliente; no pide un turno para elegir a alguien intermedio. Se muestran su nombre y su espera.', 'Después de cada operación se actualizan frente y final. Si la cola queda vacía, la pantalla usa -1 como indicador. La capacidad sólo se puede cambiar con la cola vacía.'],
 tabla=[['Evento','Cola: frente a final','Efecto'],['Ana llega a las 12:00:00','Ana, turno 1','Frente y final = 1'],['Luis llega a las 12:00:02','Ana, Luis','Frente 1; final 2'],['Atender a las 12:00:18','Luis','Ana esperó 20 segundos']],
 errores='La cola llena impide nuevas inserciones y la vacía impide atender. Se rechazan nombres faltantes, movimientos ajenos al selector y cambios de capacidad con clientes pendientes. Math.Max evita mostrar tiempos negativos.',
 oral='La cola impone el orden de atención. Agregar utiliza el final y atender utiliza el frente. La espera se calcula con las horas guardadas, no con una cantidad inventada por la interfaz.'),

dict(id='C2', titulo='Juego de pintar coches', clase='ColorAuto, Coche y Juego',
 anclas=['public sealed class Juego', 'public long Intervalo', 'public void Pintar(ColorAuto color, long ahora)'],
 estructura='Juego mantiene una Cola<Coche> con capacidad cinco. Cada coche tiene un número y un color solicitado. Las variables de tiempo se expresan en milisegundos y se basan en Environment.TickCount64.',
 metodos=[('Iniciar y Encolar', 'Iniciar vacía la cola anterior, pone el marcador en cero, conserva el récord y crea el primer coche inmediatamente. Encolar elige aleatoriamente uno de los cinco colores y aumenta la secuencia. La siguiente llegada se programa como ahora + Intervalo.'),
 ('Actualizar(ahora)', 'Mientras la partida siga activa y haya vencido la siguiente llegada, agrega coches. El while recupera llegadas vencidas si la pestaña se retrasó. Cuando la cola alcanza cinco, marca Activo = false y guarda el instante exacto de fin.'),
 ('Pintar e Intervalo', 'Pintar primero actualiza las llegadas y valida partida, cola y color del frente. Sólo un acierto elimina ese frente e incrementa Pintados. Intervalo calcula max(2000, 20000 - Pintados * 2000): cada acierto reduce dos segundos hasta un mínimo de dos.'),
 ('Récord y visualización', 'Transcurrido usa el reloj actual si la partida sigue activa o Fin si terminó. GuardarRecord actualiza puntaje y tiempo; motor.js conserva estos datos en localStorage para la versión pública. La pantalla consulta el estado cada segundo cuando este ejercicio está seleccionado.')],
 codigo='''Coches.EliminaCola(); Pintados++;
ProximaLlegada = Math.Min(ProximaLlegada,
    ahora + Intervalo);
GuardarRecord(ahora);''',
 pasos=['Al iniciar aparece un coche. Si nadie pinta, llegan otros a los 20, 40, 60 y 80 segundos; al quinto coche termina la partida.', 'Al acertar el color, el frente sale y el marcador aumenta. Si era el primer acierto, Intervalo cambia de 20000 a 18000 milisegundos.', 'Math.Min conserva la llegada que ocurra antes: la ya programada o ahora + el intervalo reducido. Acertar nunca retrasa una llegada que ya estaba próxima.', 'El segundo acierto reduce a 16 segundos, el tercero a 14 y así hasta dos. Un error de color conserva el coche y el marcador. Si una llegada acaba de llenar la cola antes de pintar, ya no se admite el acierto.'],
 tabla=[['Coches pintados','Cálculo en milisegundos','Intervalo'],['0','20000 - 0','20 segundos'],['1','20000 - 2000','20 segundos'],['3','20000 - 6000','14 segundos'],['9 o más','mínimo permitido: 2000','2 segundos']],
 errores='No se puede pintar sin partida, con la cola vacía ni después del final. Se comprueba únicamente el color del frente. Cambiar de ejercicio no pausa el reloj: al consultar otra vez se calculan las llegadas que hayan vencido.',
 oral='La dificultad no aumenta reduciendo un contador decorativo: cambia el intervalo real de llegada. Cada acierto resta dos segundos y además puede adelantar la siguiente llegada. El límite inferior evita intervalos cero o negativos.'),

dict(id='C3', titulo='Estacionamiento de autos', clase='Auto, Recibo y ColaCircularDoblementeLigada',
 anclas=['public sealed class ColaCircularDoblementeLigada', 'public void Insertar(string placas', 'public Recibo Salir(DateTime ahora)', 'public bool EnlacesValidos()'],
 estructura='Esta cola no se delega a Queue<T>. Cada Nodo contiene un Auto y dos referencias: Anterior y Siguiente. El último apunta al primero y el primero al último. frente identifica al siguiente vehículo que debe salir.',
 metodos=[('Insertar(placas, propietario, ahora)', 'Normaliza las placas a mayúsculas, busca duplicados y valida al propietario. Si es el primer nodo, sus dos enlaces apuntan a él mismo. En otro caso inserta después del último, que se obtiene como frente.Anterior, sin cambiar el frente.'),
 ('Salir(ahora)', 'Si no hay frente, informa que está vacío. Con un solo nodo pone frente en null. Con varios avanza frente al siguiente y une el último con el nuevo frente en ambos sentidos. Reduce Count y construye un Recibo con horas, segundos y costo.'),
 ('Lista y EnlacesValidos', 'Lista usa do/while para recorrer una vuelta y se detiene cuando vuelve al frente. EnlacesValidos comprueba que Siguiente.Anterior y Anterior.Siguiente regresen al mismo nodo y que se visite exactamente Count nodos. Ayuda a detectar enlaces mal actualizados en las pruebas.')],
 codigo='''if (frente is null)
{
    n.Anterior = n.Siguiente = n; frente = n;
}
else
{
    Nodo ultimo = frente.Anterior;
    n.Anterior = ultimo; n.Siguiente = frente;
    ultimo.Siguiente = n; frente.Anterior = n;
}
Count++;''',
 pasos=['Se registra ABC-123 con su propietario y la hora del sistema. El primer nodo se enlaza consigo mismo; Count pasa a uno.', 'Al registrar XYZ-987 se conecta detrás de ABC-123. El circuito queda cerrado en ambos sentidos y el frente continúa en ABC-123.', 'Salida de auto retira ABC-123 por FIFO. XYZ-987 pasa a ser el frente y, al quedar solo, sus dos enlaces vuelven a apuntar a él mismo.', 'Se calcula la diferencia entre salida y entrada, se toman segundos completos y se multiplican por 2m. Por ejemplo, 30 segundos cuestan $60.00. La cola no tiene un cupo fijo programado; su límite práctico es la memoria.'],
 tabla=[['Situación','Enlace siguiente','Enlace anterior'],['Un nodo A','A apunta a A','A apunta a A'],['Dos nodos A y B','A a B; B a A','A a B; B a A'],['Sale A; queda B','B apunta a B','B apunta a B'],['Sale B','frente = null','Count = 0']],
 errores='Se rechazan placas repetidas aunque cambien las mayúsculas, textos vacíos y salida sin autos. La salida es siempre del frente, no por placas. La tarifa usa segundos completos y evita cobros negativos si el reloj retrocede.',
 oral='El punto importante son los enlaces. Siempre debemos reparar el enlace de ida y el de regreso. El caso de un solo auto se trata aparte para dejar la cola realmente vacía al retirarlo.')
]
