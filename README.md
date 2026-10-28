# Practica_U2_ED032026 — versión web

Aplicación de los **12 ejercicios en C# con ASP.NET Core y .NET 10**, para usar desde el navegador. Esta es la rama `web`.

## Dos versiones

- [Rama escritorio](https://github.com/victormanuelxd360-afk/Practica_U2_ED032026/tree/escritorio): C# con Windows Forms, cuatro proyectos y ejecutables para Windows.
- [Rama web](https://github.com/victormanuelxd360-afk/Practica_U2_ED032026/tree/web): servidor ASP.NET Core, interfaz adaptable al navegador y los mismos algoritmos C#.

`main` conserva la versión base de escritorio. No se necesita mezclar las ramas para ejecutar cada versión.

## Ejecutar la web

Instala el SDK .NET 10. Funciona en Windows, Linux y macOS:

```powershell
git switch web
dotnet run --project Web/PracticaWeb.csproj --urls http://localhost:5188
```

Abre http://localhost:5188 en el navegador. En Windows también puedes hacer doble clic en `INICIAR.cmd` o `INICIAR_WEB.cmd`. Mantén el servidor en ejecución mientras usas la página; Ctrl+C lo detiene. Puedes abrir `Practica_U2_Web.sln` en Visual Studio compatible con .NET 10.

## Ejercicios incluidos

| Estructura | Ejercicios |
| --- | --- |
| Listas | Productos disponibles y retirados; pares e impares; aprobados y reprobados; eliminar y ordenar productos; palabras por letra |
| Pilas | Invertir palabra; palíndromo; suma de números grandes; reemplazar valor |
| Colas | Ventanilla de banco; juego de pintar coches; estacionamiento con cola circular doblemente ligada |

Los formularios validan datos faltantes, rangos, duplicados, sobreflujo y colas vacías. Dinero y calificaciones usan decimal; se admite punto o coma decimal. La suma usa pilas de dígitos; el estacionamiento usa nodos circulares doblemente ligados. El juego se actualiza cada segundo en pantalla, acelera por niveles según los coches pintados y termina al acumular cinco.

### Dónde está el código C# de cada ejercicio

| Ejercicio | Carpeta en `CSharp/Ejercicios/` | Clase o método |
| --- | --- | --- |
| L1 Productos disponibles y retirados | `Listas/L1_Productos/` | `Almacen` |
| L2 Pares e impares | `Listas/L2_ParesImpares/` | `Algoritmos.Clasificar` |
| L3 Aprobados y reprobados | `Listas/L3_Calificaciones/` | `Alumno`, `Grupo` |
| L4 Eliminar y ordenar productos | `Listas/L4_Compra/` | `Compra` |
| L5 Palabras por letra | `Listas/L5_Palabras/` | `Algoritmos.Agrupar` |
| P1 Invertir palabra | `Pilas/P1_InvertirPalabra/` | `Algoritmos.Invertir` |
| P2 Palíndromo | `Pilas/P2_Palindromo/` | `Algoritmos.Palindromo` |
| P3 Suma de números grandes | `Pilas/P3_SumaGrande/` | `Algoritmos.SumarGrandes` |
| P4 Reemplazar valor | `Pilas/P4_Reemplazar/` | `Algoritmos.Reemplazar` |
| C1 Ventanilla de banco | `Colas/C1_Banco/` | `Cliente`, `Banco` |
| C2 Juego de pintar coches | `Colas/C2_JuegoCoches/` | `ColorAuto`, `Coche`, `Juego` |
| C3 Estacionamiento | `Colas/C3_Estacionamiento/` | `Auto`, `Recibo`, `ColaCircularDoblementeLigada` |

`Comun/` contiene `Validar` y `Producto`, que usan L1 y L4. `Colas/Cola.cs` es la cola de capacidad fija que usan C1 y C2. `Algoritmos` es una clase `partial`: cada ejercicio de listas y pilas aporta su método desde su propia carpeta. La interfaz de los doce ejercicios sigue en una sola página (`Web/wwwroot/`) y `Web/Estado.cs` conecta cada botón con su clase.

## Arquitectura y sesiones

- `Web/Program.cs`: API y estado por sesión con cookie HttpOnly y SameSite Strict.
- `Web/wwwroot/`: interfaz HTML, CSS y JavaScript sin dependencias externas.
- `CSharp/Ejercicios/`: algoritmos C# compartidos con escritorio, una carpeta por ejercicio, compilados en el proyecto web mediante referencia de fuentes.
- `herramientas/probar-web.ps1`: integración HTTP de los doce ejercicios, errores y aislamiento de sesiones.
- `pruebas-web.txt`: resultado real de las pruebas.
- `documentacion/`: informe PDF, portada, `datos_portada.json`, evidencias y los scripts que generan el informe (`documentacion/herramientas/`). El programa no depende de esta carpeta.

Cada navegador tiene sus propias listas, colas, resultados y récord de juego. Se conservan al cambiar de ejercicio; se eliminan tras dos horas sin actividad, al cerrar la sesión del navegador, por límite de memoria o al reiniciar el servidor. No hay base de datos ni cuentas. El servidor mantiene hasta 1000 sesiones en caché; es una práctica académica, sin persistencia duradera. El récord web se conserva durante la sesión.

Las carpetas CSharp, proyectos y legado-java conservan código de referencia. `documentacion/Documentacion_WEB.pdf` y `documentacion/evidencias-web/` corresponden a la versión web. `documentacion/Documentacion_CSharp.pdf` y `documentacion/evidencias-csharp/` corresponden a escritorio. Para desarrollar escritorio, cambia a la rama `escritorio`.

## Compilar y probar

En Windows con PowerShell:

```powershell
./COMPILAR_Y_PROBAR.cmd
```

También puedes ejecutar `pwsh -File herramientas/probar-web.ps1`. Compila, inicia un servidor temporal en el puerto 5187, comprueba los ejercicios y detiene el proceso al terminar. GitHub Actions ejecuta estas verificaciones con cada push y pull request de esta rama.

Publicación compilada:

```powershell
dotnet publish Web/PracticaWeb.csproj -c Release -o ejecutables-web
```

Para ejecutarla con ASP.NET Core Runtime 10, entra en `ejecutables-web` y ejecuta `dotnet PracticaWeb.dll --urls http://localhost:5188`. La versión pública funciona en GitHub Pages: https://victormanuelxd360-afk.github.io/Practica_U2_ED032026/ .

## Documento para entregar y exponer

`documentacion/Documentacion_WEB.pdf` contiene 50 páginas con la portada enviada por el equipo, grupo 4.º A, los cuatro integrantes y el apellido **Almendarez**, con Z. Conserva el desarrollo y las evidencias, y añade la explicación de clases, métodos, estructuras, fragmentos reales de código, recorridos con datos y una guía para la exposición de los doce ejercicios. El mapa final permite localizar los métodos por su línea de inicio en el código.

La fuente de la portada es `documentacion/Portada_equipo.png`. Los datos editables están en `documentacion/datos_portada.json`. Para regenerar la documentación, ejecuta `python documentacion/herramientas/generar_documentacion_web.py` con Python, reportlab, Pillow y pypdf en Windows. El script conserva el desarrollo inicial y reemplaza la guía anterior al regenerar, para evitar duplicarla.

## Web pública independiente de esta computadora

La URL pública es https://victormanuelxd360-afk.github.io/Practica_U2_ED032026/ . La carpeta `WebPublica` compila los mismos modelos y controladores de ejercicios a C# WebAssembly, de modo que los doce ejercicios funcionan en el navegador sin un servidor ASP.NET encendido. GitHub Actions publica automáticamente los cambios de la rama web.

En la versión pública, las listas se conservan al cambiar de ejercicio y se reinician al recargar la página; el récord se guarda en el almacenamiento local del navegador. La versión ASP.NET sigue disponible en `Web`, con sesiones de servidor.

El juego comienza con un coche inmediato y un intervalo de 20 segundos. Los primeros 5 coches usan 20 s; los coches 6 a 8 usan 10 s; desde el coche 9 el intervalo es de 2 s. Sólo se puede pintar el frente y el juego termina con cinco coches en cola.

Para compilar la versión pública: ejecuta `herramientas/preparar-publica.ps1` y después `dotnet publish WebPublica/PracticaPublica.csproj -c Release -o publicacion-pages`. El contenido de `publicacion-pages/wwwroot` se puede alojar como sitio estático. `Dockerfile` y `railway.json` quedan disponibles para quien prefiera alojar la variante ASP.NET en un servidor propio.
