# Practica_U2_ED032026 — C#

Práctica de la Unidad II de Estructura de Datos: **12 ejercicios en C# con Windows Forms y .NET 10**. Incluye solución para Visual Studio, menú general y un proyecto independiente por estructura.

## Abrir y ejecutar

Necesitas Windows y el SDK de .NET 10 para compilar. Abre `Practica_U2_ED032026.sln` en Visual Studio compatible con .NET 10 y la carga de trabajo de escritorio de .NET. Desde terminal:

```powershell
dotnet run --project CSharp/Practica.csproj -c Release
```

Haz doble clic en `INICIAR.cmd` para iniciar el menú general. Las pestañas mantienen sus datos durante la sesión; el menú superior lleva a cada estructura.

`COMPILAR_Y_PROBAR.cmd` compila, prueba y genera cuatro programas en `ejecutables`: General, Listas, Pilas y Colas. Los programas publicados requieren **.NET Desktop Runtime 10 para Windows**. Distribuye todos los archivos de cada carpeta, incluyendo EXE, DLL y JSON. También están disponibles en Releases de GitHub.

## Ejercicios

| Estructura | Ejercicios |
| --- | --- |
| Listas | Productos disponibles y retirados; pares e impares; aprobados y reprobados; eliminar y ordenar productos; palabras por letra |
| Pilas | Invertir palabra; palíndromo; suma de números grandes; reemplazar valor |
| Colas | Ventanilla de banco; juego de pintar coches; estacionamiento con cola circular doblemente ligada |

Proyectos independientes:

```powershell
dotnet run --project proyectos/Listas/Listas.csproj -c Release
dotnet run --project proyectos/Pilas/Pilas.csproj -c Release
dotnet run --project proyectos/Colas/Colas.csproj -c Release
```

## Contenido y decisiones

- `CSharp/Modelos.cs`: modelos, algoritmos y validaciones.
- `CSharp/Program.cs`: interfaz Windows Forms, tablas y coches dibujados con GDI+.
- `CSharp/Pruebas.cs`: pruebas de algoritmos, temporización y acciones reales de botones.
- `proyectos/`: tres proyectos C# con fuentes compartidas mediante referencias Compile.
- `pruebas-csharp.txt`: resultados reales de pruebas.
- `evidencias-csharp/`: doce pantallas con datos procesados por los controles.
- `documentacion/Documentacion_CSharp.pdf`: análisis, funcionamiento y capturas de C#.
- `legado-java/`: versión anterior; sus capturas y documentación corresponden a Java.

Dinero y calificaciones usan decimal, con punto o coma decimal; cantidades, turnos y valores de pila son enteros. Se validan faltantes, rangos, duplicados, colas llenas y vacías. La suma usa pilas de dígitos; BigInteger sólo aparece como oráculo en pruebas. El palíndromo ignora mayúsculas, espacios y signos, conservando acentos. Reemplazar sustituye viejo por nuevo sin alterar el orden.

Los objetos siguen la convención del enunciado: el formulario es `frmPractica` y cada control lleva prefijo por tipo (`btnRetirar`, `txtClaveRetiro`, `lblEstadoL1`, `dgvTablaC1`, `cboMovimiento`, `pnlCoches`, `tabC2`, `mnuSalir`); las pruebas verifican prefijos y nombres únicos.

Banco: capacidad inicial 5, configurable sólo con cola vacía; muestra el siguiente No. Turno, y frente y final muestran turnos, o -1 si está vacío. Al formar un cliente aparece la ventana "SE AGREGA UN CLIENTE AL FINAL DE LA COLA" y al atenderlo "TIEMPO DE ESPERA EN LA COLA"; "Salida del sistema" cierra la aplicación. Juego: primer coche inmediato y siguientes cada 20 segundos; cada tres aciertos reduce el intervalo 2 segundos hasta un mínimo de 2; termina con cinco coches. Los coches esperan sin pintar con una etiqueta del color pedido, la paleta son botones coloreados y el coche atendido se muestra pintado. Récord en `%LOCALAPPDATA%\Practica_U2_CSharp\record.txt`. Estacionamiento: nodos circulares doblemente ligados, salida FIFO y tarifa de $2.00 por segundo completo; la entrada se confirma con un mensaje y la salida muestra el recibo en una ventana.

En pruebas y capturas (`--probar`) los mensajes se registran sin abrir ventanas modales y no se modifica el récord del usuario.

## Equipo

El repositorio es público; para editar directamente hay que aceptar la invitación como colaborador. GitHub Actions compila y prueba C# con cada push y pull request. Integrantes y grupo pendientes en `datos_portada.json`. Entrega del enunciado: 23 de octubre de 2026.
