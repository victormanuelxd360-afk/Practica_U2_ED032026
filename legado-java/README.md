# Practica_U2_ED032026

Práctica de la Unidad II: Estructuras de datos básicas. Repositorio nuevo para los 12 ejercicios de listas, pilas y colas.

## Trabajo en equipo en GitHub

Este repositorio es público: cualquiera puede consultar el código o proponer cambios mediante un fork y un pull request. Para trabajar directamente en el repositorio, el propietario debe invitar a cada integrante desde **Settings > Collaborators**, utilizando su usuario de GitHub.

La carpeta `src` contiene las fuentes principales. Después de modificarlas, ejecuta `COMPILAR_Y_PROBAR.cmd`: sincroniza las fuentes de los tres proyectos y genera los ejecutables. GitHub Actions también compila y ejecuta las pruebas con cada push y pull request.

## Ejercicios incluidos

| Estructura | Ejercicios |
| --- | --- |
| Listas | Productos disponibles y retirados; pares e impares; aprobados y reprobados; eliminar y ordenar productos; palabras por letra |
| Pilas | Invertir palabra; palíndromo; suma de números grandes; reemplazar valor |
| Colas | Ventanilla de banco; juego de pintar coches; estacionamiento con cola circular doblemente ligada |

Asignatura: Estructura de Datos. Carrera: Ingeniería en Tecnologías de la Información e Innovación Digital.
Docente: Ing. Mirian Magaly Canché Caamal. Entrega indicada: viernes 23 de octubre de 2026.

## Abrir y usar

1. Instala Java 21 o posterior si el equipo no lo tiene. En el equipo de elaboración se verificó con Java 21.0.11.
2. Haz doble clic en `INICIAR.cmd`. Se abre el menú general con los 12 ejercicios.
3. Para abrir un proyecto por estructura, usa `proyectos/Listas/INICIAR.cmd`, `proyectos/Pilas/INICIAR.cmd` o `proyectos/Colas/INICIAR.cmd`.
4. Selecciona una opción del menú lateral. Los datos se conservan al cambiar de ejercicio durante la sesión. Usa Salir para cerrar.

También puedes abrir los archivos JAR o ejecutar `java -jar Practica_U2.jar`. No requiere Internet ni librerías externas. Swing incluye las ilustraciones de coches dibujadas por el programa.

## Contenido

- `src/`: modelos orientados a objetos, interfaz y pruebas del conjunto.
- `proyectos/`: tres proyectos independientes, cada uno con fuentes, clases compiladas y JAR con su propio menú.
- `documentacion/Documentacion_Unidad_II.pdf`: portada, análisis de entradas/proceso/salida, funcionamiento y evidencia explicada de cada ejercicio, pruebas y decisiones de implementación.
- `documentacion/pruebas_resultados.txt`: resultado real de las comprobaciones automáticas.
- `evidencias/`: pantallas renderizadas desde los paneles reales después de ejecutar los controles; incluye resultados y errores de validación.
- `herramientas/`: compilación, regeneración de evidencias y generación del PDF.
- `datos_portada.json`: datos de portada editables; completa nombres y grupo antes de entregar.

## Compilar y verificar

Necesitas un JDK 21 o posterior con `java`, `javac` y `jar` en PATH. Ejecuta `COMPILAR_Y_PROBAR.cmd`. Compila y prueba todo antes de generar los cuatro JAR. También puedes abrir cada carpeta de `proyectos` como proyecto Java en un IDE y ejecutar `Inicio.java`.

Para compilar manualmente un proyecto (desde su carpeta):

```powershell
javac -encoding UTF-8 -d build src\Estructuras.java src\PracticaApp.java src\Inicio.java
java -cp build Inicio
```

Las pruebas se ejecutan en modo sin ventanas, activan los mismos botones y renderizan los mismos paneles. El tiempo del juego y del estacionamiento se verifica además con instantes controlados; no se espera artificialmente 80 segundos.

## Decisiones y límites

- Listas: `ArrayList`; pilas: `ArrayDeque` con `push` y `pop`; banco y juego: cola FIFO acotada; estacionamiento: nodos circulares doblemente ligados implementados expresamente.
- Dinero: `BigDecimal`, con dos decimales. Calificaciones: 0 a 10; se aprueba desde 7. Cantidades, turnos y elementos de pila son enteros por la naturaleza del ejercicio.
- Cantidad de productos aleatoria: 1 a 20; precio aleatorio: $1.00 a $500.00. Se cuentan objetos Producto disponibles y retirados.
- Generación de números: entre 1 y 500 elementos, valores de 0 a 999.
- Suma mediante pilas: enteros no negativos; no usa `BigInteger` en la solución. Se usa `BigInteger` únicamente como oráculo de las pruebas.
- Palíndromos: ignora mayúsculas, espacios y signos; los acentos se conservan.
- Se interpreta el error de redacción de listas 3 como mostrar aprobados y reprobados; en pilas 4 se sustituye viejo por nuevo.
- Banco: capacidad inicial 5, configurable entre 1 y 1000 sólo con cola vacía. Frente y final muestran los números de turno, o -1 si está vacía.
- Juego: primer coche inmediato, siguientes cada 20 segundos; reduce el intervalo 2 segundos cada 3 aciertos hasta un mínimo de 2. Al alcanzar 5 coches termina. El récord se conserva en `%USERPROFILE%\.practica-u2\record.properties`. Los demás datos son de sesión.
- Estacionamiento: salida FIFO; tarifa de $2.00 por segundo completo transcurrido. Registra placas únicas, propietario y horas del sistema; no tiene cupo fijo.

## Portada y entrega

Los nombres de los integrantes y el grupo están pendientes de completar porque no fueron proporcionados. Edita `datos_portada.json` y regenera el PDF con `herramientas/generar_documentacion.py` (Python con `reportlab`, `Pillow` y `pypdf`). Después vuelve a comprimir la carpeta con WinRAR. El script de documentación también vuelve a producir el RAR si WinRAR está disponible en su ruta habitual.

El RAR preparado contiene los proyectos completos y el PDF. La entrega en Teams corresponde a un integrante del equipo.
