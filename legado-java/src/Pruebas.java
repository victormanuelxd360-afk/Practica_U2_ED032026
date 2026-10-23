import java.io.*;
import java.math.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.time.*;
import java.util.*;
import javax.swing.SwingUtilities;

/** Pruebas reproducibles de modelos, temporización e integración de controles. */
public class Pruebas {
  static int correctas;
  static final StringBuilder log =
      new StringBuilder(
          "PRUEBAS DE LA UNIDAD II\nJava " + System.getProperty("java.version") + "\n\n");

  static void verificar(boolean condicion, String nombre) {
    if (!condicion) throw new AssertionError(nombre);
    correctas++;
    log.append("OK | ").append(nombre).append('\n');
  }

  static void rechaza(Runnable r, String nombre) {
    try {
      r.run();
    } catch (IllegalArgumentException e) {
      verificar(e.getMessage() != null && !e.getMessage().isBlank(), nombre);
      return;
    }
    throw new AssertionError("Debió rechazar: " + nombre);
  }

  static BigDecimal bd(String s) {
    return new BigDecimal(s);
  }

  public static void main(String[] args) throws Exception {
    Path base = Path.of(args.length == 0 ? "." : args[0]).toAbsolutePath();
    Estructuras.Almacen almacen = new Estructuras.Almacen();
    for (int i = 0; i < 100; i++) almacen.escanear();
    verificar(almacen.disponibles.size() == 100, "L1: escanear 100 objetos Producto");
    verificar(
        almacen.disponibles.stream()
            .allMatch(
                p ->
                    p.cantidad() >= 1
                        && p.cantidad() <= 20
                        && p.precio().compareTo(bd("1")) >= 0
                        && p.precio().compareTo(bd("500")) <= 0),
        "L1: rangos aleatorios de cantidad y precio");
    almacen.retirar("P2");
    verificar(
        almacen.disponibles.size() == 99
            && almacen.retirados.size() == 1
            && almacen.retirados.get(0).nombre().equals("producto2"),
        "L1: retiro sin pérdida del historial");
    rechaza(() -> almacen.retirar("P2"), "L1: no retirar dos veces");
    var numeros = Estructuras.generarNumeros(500, new Random(2026));
    verificar(
        numeros.original().size() == 500
            && numeros.pares().size() + numeros.impares().size() == 500
            && numeros.pares().stream().allMatch(x -> x % 2 == 0)
            && numeros.impares().stream().allMatch(x -> x % 2 != 0),
        "L2: genera 500 números y clasifica todos correctamente");
    Map<Integer, Long> original =
        numeros.original().stream()
            .collect(
                java.util.stream.Collectors.groupingBy(
                    x -> x, java.util.stream.Collectors.counting()));
    List<Integer> unidos = new ArrayList<>(numeros.pares());
    unidos.addAll(numeros.impares());
    verificar(
        original.equals(
            unidos.stream()
                .collect(
                    java.util.stream.Collectors.groupingBy(
                        x -> x, java.util.stream.Collectors.counting()))),
        "L2: conserva todos los números, incluidos repetidos");
    rechaza(
        () -> Estructuras.generarNumeros(0, new Random()), "L2: rechaza cantidad fuera de rango");
    Estructuras.Grupo grupo = new Estructuras.Grupo();
    grupo.agregar("Ana", bd("7"));
    grupo.agregar("Luis", bd("6.99"));
    grupo.agregar("Eva", bd("10"));
    grupo.agregar("Pedro", bd("0"));
    verificar(
        grupo.aprobados.size() == 2 && grupo.reprobados.size() == 2,
        "L3: separación en el límite 7");
    verificar(
        grupo.aprobados.stream().allMatch(a -> a.calificacion().compareTo(bd("7")) >= 0),
        "L3: reprobados extraídos de la lista inicial");
    rechaza(() -> grupo.agregar("X", bd("11")), "L3: rechaza notas mayores a diez");
    rechaza(() -> grupo.agregar(" ", bd("8")), "L3: rechaza nombre vacío");
    Estructuras.Compra compra = new Estructuras.Compra();
    compra.agregar("P1", "Zanahoria", bd("15.50"));
    compra.agregar("P2", "Arroz", bd("32.75"));
    compra.agregar("P3", "Leche", bd("26.25"));
    verificar(
        compra.ordenados().get(0).nombre().equals("Arroz"), "L4: orden alfabético por nombre");
    verificar(compra.total().compareTo(bd("74.50")) == 0, "L4: total decimal exacto 74.50");
    compra.eliminar("p2");
    verificar(
        compra.total().compareTo(bd("41.75")) == 0, "L4: elimina por clave y recalcula total");
    rechaza(
        () -> compra.agregar("p1", "Duplicado", bd("2")),
        "L4: claves únicas sin distinguir mayúsculas");
    rechaza(() -> compra.eliminar("XX"), "L4: clave inexistente");
    rechaza(() -> compra.agregar("P4", "Pan", bd("-1")), "L4: precio negativo");
    var letras =
        Estructuras.agrupar(
            List.of("Fresa", "Fresca", "Orilla", "Oso", "Peso", "Pez", "árbol", "Águila"));
    verificar(
        letras.size() == 4 && letras.get("F").size() == 2 && letras.get("Á").size() == 2,
        "L5: creación dinámica de listas e inicial acentuada");
    rechaza(() -> Estructuras.agrupar(List.of("dos palabras")), "L5: valida palabra individual");
    verificar(Estructuras.invertir("UTM").equals("MTU"), "P1: ejemplo UTM -> MTU");
    verificar(Estructuras.invertir("a😀b").equals("b😀a"), "P1: caracteres Unicode completos");
    rechaza(() -> Estructuras.invertir(" "), "P1: entrada faltante");
    verificar(Estructuras.palindromo("Anita lava la tina"), "P2: frase palíndroma");
    verificar(
        Estructuras.palindromo("12321") && !Estructuras.palindromo("Casa"),
        "P2: número y caso negativo");
    rechaza(() -> Estructuras.palindromo("!!!"), "P2: requiere letras o números");
    verificar(
        Estructuras.sumarGrandes("999999999999999999999999999999", "1")
            .equals("1000000000000000000000000000000"),
        "P3: acarreo de 30 dígitos");
    verificar(Estructuras.sumarGrandes("0000", "000").equals("0"), "P3: cero y ceros iniciales");
    Random azar = new Random(2026);
    boolean sumas = true;
    for (int i = 0; i < 200; i++) {
      BigInteger a = new BigInteger(4096, azar), b = new BigInteger(4096, azar);
      sumas &= Estructuras.sumarGrandes(a.toString(), b.toString()).equals(a.add(b).toString());
    }
    verificar(
        sumas,
        "P3: 200 sumas aleatorias de hasta 1234 dígitos contra oráculo BigInteger (sólo en"
            + " pruebas)");
    rechaza(() -> Estructuras.sumarGrandes("-1", "2"), "P3: contrato de enteros no negativos");
    rechaza(() -> Estructuras.sumarGrandes("12x", "2"), "P3: rechaza letras");
    Deque<Integer> pila = new ArrayDeque<>();
    for (int x : new int[] {1, 2, 3, 2}) pila.push(x);
    verificar(
        Estructuras.Reemplazar(pila, 9, 2) == 2
            && new ArrayList<>(pila).equals(List.of(9, 3, 9, 1)),
        "P4: reemplaza todas las apariciones y conserva el orden");
    verificar(Estructuras.Reemplazar(pila, 5, 77) == 0, "P4: valor ausente");
    verificar(Estructuras.Reemplazar(new ArrayDeque<>(), 5, 1) == 0, "P4: pila vacía");
    Instant t = Instant.parse("2026-10-16T12:00:00Z");
    Estructuras.Banco banco = new Estructuras.Banco(2);
    rechaza(() -> banco.atender(t), "C1: atiende cola vacía con mensaje");
    banco.llegar("Ana", "Depósito", t);
    banco.llegar("Luis", "Retiro", t.plusSeconds(2));
    verificar(
        banco.cola.ColaLlena() && banco.cola.frente().turno() == 1 && banco.cola.fin().turno() == 2,
        "C1: capacidad, frente y final");
    rechaza(() -> banco.llegar("Eva", "Retiro", t), "C1: rechaza sobreflujo");
    var at = banco.atender(t.plusSeconds(18));
    verificar(
        at.cliente().nombre().equals("Ana") && at.esperaSegundos() == 18,
        "C1: FIFO y tiempo de espera exacto de 18 segundos");
    banco.atender(t.plusSeconds(20));
    verificar(banco.cola.ColaVacia(), "C1: queda vacía después de atender");
    Estructuras.Juego juego = new Estructuras.Juego();
    juego.iniciar(0);
    verificar(
        juego.cola.size() == 1 && juego.intervalo() == 20000,
        "C2: primer coche e intervalo inicial de 20 segundos");
    juego.actualizar(19999);
    verificar(juego.cola.size() == 1, "C2: no llega antes del tiempo");
    juego.actualizar(20000);
    verificar(juego.cola.size() == 2, "C2: llegada exacta a los 20 segundos");
    Estructuras.ColorAuto correcto = juego.cola.frente().color(),
        incorrecto = Estructuras.ColorAuto.values()[(correcto.ordinal() + 1) % 5];
    rechaza(() -> juego.pintar(incorrecto, 20001), "C2: color incorrecto no elimina el frente");
    verificar(juego.cola.size() == 2 && juego.pintados == 0, "C2: la cola se conserva tras error");
    juego.pintar(correcto, 20002);
    juego.pintar(juego.cola.frente().color(), 20003);
    juego.actualizar(40000);
    juego.pintar(juego.cola.frente().color(), 40001);
    verificar(
        juego.pintados == 3 && juego.intervalo() == 18000,
        "C2: acelera de 20 a 18 segundos cada tres aciertos");
    verificar(juego.record == 3 && juego.tiempoRecord == 40, "C2: récord con cantidad y tiempo");
    juego.iniciar(0);
    juego.actualizar(80000);
    verificar(
        !juego.activo && juego.cola.size() == 5 && juego.transcurrido(999999) == 80,
        "C2: fin exacto en cinco coches y tiempo detenido en 80 s");
    rechaza(
        () -> juego.pintar(juego.cola.frente().color(), 80001),
        "C2: no permite pintar después del final");
    juego.iniciar(100000);
    verificar(
        juego.activo && juego.pintados == 0 && juego.record == 3,
        "C2: reinicia partida y conserva récord");
    for (int i = 0; i < 40; i++) {
      if (juego.cola.ColaVacia()) juego.actualizar(juego.proximaLlegada);
      juego.pintar(juego.cola.frente().color(), juego.proximaLlegada - 1);
    }
    verificar(juego.intervalo() == 2000, "C2: límite inferior de dos segundos");
    Estructuras.ColaCircularDoblementeLigada parking =
        new Estructuras.ColaCircularDoblementeLigada();
    rechaza(() -> parking.salir(t), "C3: salida con estacionamiento vacío");
    parking.insertar("abc-123", "Ana", t);
    parking.insertar("xyz-987", "Luis", t.plusSeconds(10));
    verificar(
        parking.enlacesValidos() && parking.size() == 2,
        "C3: enlaces anterior/siguiente y circularidad");
    rechaza(() -> parking.insertar("ABC-123", "Otro", t), "C3: rechaza placas duplicadas");
    var recibo = parking.salir(t.plusSeconds(30));
    verificar(
        recibo.auto().placas().equals("ABC-123")
            && recibo.segundos() == 30
            && recibo.costo().compareTo(bd("60")) == 0,
        "C3: salida FIFO y cobro de 30 x 2 = 60 pesos");
    parking.salir(t.plusSeconds(31));
    verificar(
        parking.ColaVacia() && parking.enlacesValidos(),
        "C3: elimina último nodo y restablece estructura");
    for (int i = 0; i < 1000; i++) parking.insertar("PLACA" + i, "Dueño " + i, t);
    boolean enlaces = true;
    for (int i = 0; i < 1000; i++) {
      enlaces &= parking.enlacesValidos();
      enlaces &= parking.salir(t.plusSeconds(1)).auto().placas().equals("PLACA" + i);
    }
    verificar(
        enlaces && parking.enlacesValidos(),
        "C3: mil nodos sin cupo fijo; verifica FIFO y enlaces en cada salida");
    verificar(
        Estructuras.decimal("8,5", bd("0"), bd("10")).compareTo(bd("8.5")) == 0,
        "Validación: separador decimal coma");
    rechaza(() -> Estructuras.entero("2.5", 1, 500), "Validación: cantidad requiere entero");
    rechaza(
        () -> Estructuras.entero("999999999999999", 1, 500), "Validación: desbordamiento numérico");
    rechaza(() -> Estructuras.decimal("NaN", bd("0"), bd("10")), "Validación: rechaza NaN");
    rechaza(() -> Estructuras.decimal("", bd("0"), bd("10")), "Validación: datos faltantes");
    SwingUtilities.invokeAndWait(
        () -> {
          try {
            PracticaApp.generarEvidencias(base.resolve("evidencias").toFile());
            verificar(
                PracticaApp.MODULOS.size() == 12,
                "Interfaz: doce pantallas y acciones ejecutadas mediante sus controles");
            var l1 = (PracticaApp.ProductosPanel) PracticaApp.MODULOS.get(0);
            verificar(
                l1.modelo.disponibles.size() == 3 && l1.modelo.retirados.size() == 1,
                "Interfaz L1: botón de retiro actualiza datos y tabla");
            var l2 = (PracticaApp.ParesPanel) PracticaApp.MODULOS.get(1);
            verificar(
                l2.resultado.getText().contains("PARES")
                    && l2.resultado.getText().contains("IMPARES"),
                "Interfaz L2: botón genera las tres listas");
            var c1 = (PracticaApp.BancoPanel) PracticaApp.MODULOS.get(9);
            verificar(
                c1.estado.getText().contains("llena") && c1.banco.cola.size() == 1,
                "Interfaz C1: botón captura sobreflujo sin modificar la cola");
            var suma = (PracticaApp.SumaPanel) PracticaApp.MODULOS.get(7);
            verificar(
                suma.estado.getText().contains("enteros no negativos"),
                "Interfaz P3: mensaje adecuado al introducir letras");
            var l3 = (PracticaApp.AlumnosPanel) PracticaApp.MODULOS.get(2);
            verificar(
                l3.estado.getText().contains("rango"),
                "Interfaz L3: muestra error de calificación fuera de rango");
            var l4 = (PracticaApp.CompraPanel) PracticaApp.MODULOS.get(3);
            verificar(
                l4.estado.getText().contains("faltantes"),
                "Interfaz L4: muestra error de datos faltantes");
            for (String categoria : List.of("Listas", "Pilas", "Colas")) {
              PracticaApp.construir(categoria);
              int esperado = categoria.equals("Listas") ? 5 : categoria.equals("Pilas") ? 4 : 3;
              verificar(
                  PracticaApp.MODULOS.size() == esperado,
                  "Proyecto independiente " + categoria + ": menú con " + esperado + " ejercicios");
            }
          } catch (Exception ex) {
            throw new RuntimeException(ex);
          }
        });
    log.append("\nTOTAL: ").append(correctas).append(" verificaciones correctas. Sin fallos.\n");
    Files.createDirectories(base.resolve("documentacion"));
    Files.writeString(
        base.resolve("documentacion/pruebas_resultados.txt"),
        log.toString(),
        StandardCharsets.UTF_8);
    System.out.print(log);
  }
}
