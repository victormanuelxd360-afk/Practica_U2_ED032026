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

Los formularios validan datos faltantes, rangos, duplicados, sobreflujo y colas vacías. Dinero y calificaciones usan decimal; se admite punto o coma decimal. La suma usa pilas de dígitos; el estacionamiento usa nodos circulares doblemente ligados. El juego se actualiza cada segundo en pantalla y aumenta su velocidad cada tres coches pintados; termina al acumular cinco.

## Arquitectura y sesiones

- `Web/Program.cs`: API y estado por sesión con cookie HttpOnly y SameSite Strict.
- `Web/wwwroot/`: interfaz HTML, CSS y JavaScript sin dependencias externas.
- `CSharp/Modelos.cs`: algoritmos C# compartidos con escritorio, compilados en el proyecto web mediante referencia de fuentes.
- `herramientas/probar-web.ps1`: integración HTTP de los doce ejercicios, errores y aislamiento de sesiones.
- `pruebas-web.txt`: resultado real de las pruebas.
- `evidencias-web/`: captura de la versión web en funcionamiento.

Cada navegador tiene sus propias listas, colas, resultados y récord de juego. Se conservan al cambiar de ejercicio; se eliminan tras dos horas sin actividad, al cerrar la sesión del navegador, por límite de memoria o al reiniciar el servidor. No hay base de datos ni cuentas. El servidor mantiene hasta 1000 sesiones en caché; es una práctica académica, sin persistencia duradera. El récord web se conserva durante la sesión.

Las carpetas CSharp, proyectos y legado-java conservan código de referencia. Los PDF y capturas de `documentacion/` y `evidencias-csharp/` corresponden a escritorio; no se presentan como evidencia web. Para desarrollar escritorio, cambia a la rama `escritorio`.

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

Para ejecutarla con ASP.NET Core Runtime 10, entra en `ejecutables-web` y ejecuta `dotnet PracticaWeb.dll --urls http://localhost:5188`. El repositorio contiene la aplicación; no incluye un despliegue público en un servicio de hosting.
