import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.*;
import java.util.*;

/** Modelos y algoritmos independientes de la interfaz. */
public final class Estructuras {
  private Estructuras() {}

  public static String texto(String s) {
    if (s == null || s.isBlank()) throw new IllegalArgumentException("Hay datos faltantes.");
    return s.trim();
  }

  public static int entero(String s, int min, int max) {
    try {
      int n = Integer.parseInt(texto(s));
      if (n < min || n > max)
        throw new IllegalArgumentException("Introducir un entero entre " + min + " y " + max + ".");
      return n;
    } catch (NumberFormatException e) {
      throw new IllegalArgumentException(
          "Introducir sólo números enteros dentro del rango permitido.");
    }
  }

  public static BigDecimal decimal(String s, BigDecimal min, BigDecimal max) {
    try {
      BigDecimal n = new BigDecimal(texto(s).replace(',', '.'));
      if (n.compareTo(min) < 0 || n.compareTo(max) > 0)
        throw new IllegalArgumentException("Número fuera de rango: " + min + " a " + max + ".");
      return n;
    } catch (NumberFormatException e) {
      throw new IllegalArgumentException("Introducir sólo números decimales.");
    }
  }

  public static String dinero(BigDecimal n) {
    return "$" + n.setScale(2, RoundingMode.HALF_UP).toPlainString();
  }

  public record Producto(String clave, String nombre, int cantidad, BigDecimal precio) {}

  public static class Almacen {
    public final List<Producto> disponibles = new ArrayList<>(), retirados = new ArrayList<>();
    private int secuencia;
    private final Random random = new Random();

    public Producto escanear() {
      int n = ++secuencia;
      Producto p =
          new Producto(
              "P" + n,
              "producto" + n,
              random.nextInt(20) + 1,
              BigDecimal.valueOf(random.nextInt(49901) + 100, 2));
      disponibles.add(p);
      return p;
    }

    public void retirar(String clave) {
      Producto p =
          disponibles.stream()
              .filter(x -> x.clave().equalsIgnoreCase(texto(clave)))
              .findFirst()
              .orElseThrow(
                  () -> new IllegalArgumentException("Clave no encontrada entre disponibles."));
      disponibles.remove(p);
      retirados.add(p);
    }
  }

  public record Alumno(String nombre, BigDecimal calificacion) {}

  public record Clasificacion(List<Integer> original, List<Integer> pares, List<Integer> impares) {}

  public static Clasificacion generarNumeros(int cantidad, Random random) {
    if (cantidad < 1 || cantidad > 500)
      throw new IllegalArgumentException("La cantidad debe estar entre 1 y 500.");
    List<Integer> original = new ArrayList<>(),
        pares = new ArrayList<>(),
        impares = new ArrayList<>();
    for (int i = 0; i < cantidad; i++) {
      int valor = random.nextInt(1000);
      original.add(valor);
      if (valor % 2 == 0) pares.add(valor);
      else impares.add(valor);
    }
    return new Clasificacion(original, pares, impares);
  }

  public static class Grupo {
    public final List<Alumno> aprobados = new ArrayList<>(), reprobados = new ArrayList<>();

    public void agregar(String nombre, BigDecimal nota) {
      if (nota.compareTo(BigDecimal.ZERO) < 0 || nota.compareTo(BigDecimal.TEN) > 0)
        throw new IllegalArgumentException("Calificación entre 0 y 10.");
      aprobados.add(new Alumno(texto(nombre), nota));
      Iterator<Alumno> it = aprobados.iterator();
      while (it.hasNext()) {
        Alumno a = it.next();
        if (a.calificacion().compareTo(BigDecimal.valueOf(7)) < 0) {
          reprobados.add(a);
          it.remove();
        }
      }
    }
  }

  public static class Compra {
    public final List<Producto> productos = new ArrayList<>();

    public void agregar(String clave, String nombre, BigDecimal precio) {
      String k = texto(clave);
      if (productos.stream().anyMatch(p -> p.clave().equalsIgnoreCase(k)))
        throw new IllegalArgumentException("La clave ya existe.");
      if (precio.signum() < 0)
        throw new IllegalArgumentException("El precio no puede ser negativo.");
      productos.add(new Producto(k, texto(nombre), 1, precio));
    }

    public void eliminar(String clave) {
      String k = texto(clave);
      if (!productos.removeIf(p -> p.clave().equalsIgnoreCase(k)))
        throw new IllegalArgumentException("Clave no encontrada.");
    }

    public List<Producto> ordenados() {
      List<Producto> r = new ArrayList<>(productos);
      r.sort(Comparator.comparing(Producto::nombre, String.CASE_INSENSITIVE_ORDER));
      return r;
    }

    public BigDecimal total() {
      return productos.stream().map(Producto::precio).reduce(BigDecimal.ZERO, BigDecimal::add);
    }
  }

  public static Map<String, List<String>> agrupar(List<String> palabras) {
    Map<String, List<String>> grupos = new TreeMap<>();
    for (String entrada : palabras) {
      String p = texto(entrada);
      if (!p.codePoints().allMatch(Character::isLetter))
        throw new IllegalArgumentException("Introduce una palabra formada sólo por letras.");
      String letra = new String(Character.toChars(p.codePointAt(0))).toUpperCase(Locale.ROOT);
      grupos.computeIfAbsent(letra, k -> new ArrayList<>()).add(p);
    }
    return grupos;
  }

  public static String invertir(String entrada) {
    String s = texto(entrada);
    Deque<Integer> pila = new ArrayDeque<>();
    s.codePoints().forEach(pila::push);
    StringBuilder r = new StringBuilder();
    while (!pila.isEmpty()) r.appendCodePoint(pila.pop());
    return r.toString();
  }

  public static boolean palindromo(String s) {
    String normal =
        texto(s)
            .toLowerCase(Locale.ROOT)
            .codePoints()
            .filter(Character::isLetterOrDigit)
            .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
            .toString();
    if (normal.isEmpty())
      throw new IllegalArgumentException("Introduce al menos una letra o número.");
    return normal.equals(invertir(normal));
  }

  private static Deque<Integer> digitos(String s) {
    String n = texto(s);
    if (!n.matches("[0-9]+"))
      throw new IllegalArgumentException(
          "Introducir sólo números enteros no negativos, sin signos ni separadores.");
    Deque<Integer> p = new ArrayDeque<>();
    for (char c : n.toCharArray()) p.push(c - '0');
    return p;
  }

  public static String sumarGrandes(String a, String b) {
    Deque<Integer> p = digitos(a), q = digitos(b), r = new ArrayDeque<>();
    int acarreo = 0;
    while (!p.isEmpty() || !q.isEmpty() || acarreo > 0) {
      int suma = acarreo + (p.isEmpty() ? 0 : p.pop()) + (q.isEmpty() ? 0 : q.pop());
      r.push(suma % 10);
      acarreo = suma / 10;
    }
    StringBuilder resultado = new StringBuilder();
    while (!r.isEmpty()) resultado.append(r.pop());
    return resultado.toString().replaceFirst("^0+(?!$)", "");
  }

  public static int Reemplazar(Deque<Integer> pila, int nuevo, int viejo) {
    Deque<Integer> auxiliar = new ArrayDeque<>();
    int cambios = 0;
    while (!pila.isEmpty()) {
      int valor = pila.pop();
      if (valor == viejo) {
        valor = nuevo;
        cambios++;
      }
      auxiliar.push(valor);
    }
    while (!auxiliar.isEmpty()) pila.push(auxiliar.pop());
    return cambios;
  }

  /** Cola acotada FIFO con operaciones y validaciones explícitas. */
  public static class Cola<T> {
    private final Deque<T> datos = new ArrayDeque<>();
    private final int capacidad;

    public Cola(int capacidad) {
      if (capacidad <= 0) throw new IllegalArgumentException("Capacidad inválida.");
      this.capacidad = capacidad;
    }

    public boolean ColaLlena() {
      return datos.size() >= capacidad;
    }

    public boolean ColaVacia() {
      return datos.isEmpty();
    }

    public void InsertaCola(T valor) {
      if (ColaLlena())
        throw new IllegalArgumentException("La cola está llena: no se permite sobreflujo.");
      datos.addLast(Objects.requireNonNull(valor));
    }

    public T EliminaCola() {
      if (ColaVacia()) throw new IllegalArgumentException("La cola está vacía.");
      return datos.removeFirst();
    }

    public T frente() {
      return datos.peekFirst();
    }

    public T fin() {
      return datos.peekLast();
    }

    public int size() {
      return datos.size();
    }

    public List<T> lista() {
      return new ArrayList<>(datos);
    }
  }

  public record Cliente(int turno, String nombre, String movimiento, Instant llegada) {}

  public record Atencion(Cliente cliente, long esperaSegundos) {}

  public static class Banco {
    public final Cola<Cliente> cola;
    private int turno;

    public Banco(int capacidad) {
      cola = new Cola<>(capacidad);
    }

    public Cliente llegar(String nombre, String movimiento, Instant ahora) {
      if (cola.ColaLlena())
        throw new IllegalArgumentException("La cola está llena: no se permite sobreflujo.");
      Cliente c = new Cliente(turno + 1, texto(nombre), texto(movimiento), ahora);
      cola.InsertaCola(c);
      turno++;
      return c;
    }

    public Atencion atender(Instant ahora) {
      Cliente c = cola.EliminaCola();
      return new Atencion(c, Math.max(0, Duration.between(c.llegada(), ahora).getSeconds()));
    }
  }

  public enum ColorAuto {
    ROJO,
    AZUL,
    VERDE,
    AMARILLO,
    MORADO
  }

  public record Coche(int numero, ColorAuto color) {}

  public static class Juego {
    public final Cola<Coche> cola = new Cola<>(5);
    public boolean activo;
    public int pintados, record, secuencia;
    public long inicio, fin, proximaLlegada, tiempoRecord;
    private final Random azar = new Random();

    public long intervalo() {
      return Math.max(2000, 20000 - (pintados / 3) * 2000L);
    }

    public void iniciar(long ahora) {
      while (!cola.ColaVacia()) cola.EliminaCola();
      pintados = 0;
      secuencia = 0;
      inicio = ahora;
      fin = ahora;
      activo = true;
      encolar();
      proximaLlegada = ahora + intervalo();
    }

    private void encolar() {
      cola.InsertaCola(
          new Coche(++secuencia, ColorAuto.values()[azar.nextInt(ColorAuto.values().length)]));
    }

    public void actualizar(long ahora) {
      while (activo && ahora >= proximaLlegada) {
        long llegada = proximaLlegada;
        encolar();
        if (cola.size() == 5) {
          activo = false;
          fin = llegada;
          guardarRecord(llegada);
        } else proximaLlegada += intervalo();
      }
    }

    public void pintar(ColorAuto color, long ahora) {
      actualizar(ahora);
      if (!activo)
        throw new IllegalArgumentException(
            "Inicia una partida; el juego termina al llegar a 5 carros.");
      if (cola.ColaVacia())
        throw new IllegalArgumentException("Espera a que llegue el siguiente coche.");
      if (cola.frente().color() != color)
        throw new IllegalArgumentException(
            "Color incorrecto. Atiende el color solicitado por el primer coche.");
      cola.EliminaCola();
      pintados++;
      if (pintados % 3 == 0) proximaLlegada = Math.min(proximaLlegada, ahora + intervalo());
      guardarRecord(ahora);
    }

    public long transcurrido(long ahora) {
      return Math.max(0, ((activo ? ahora : fin) - inicio) / 1000);
    }

    private void guardarRecord(long ahora) {
      if (pintados > record) {
        record = pintados;
        tiempoRecord = Math.max(0, (ahora - inicio) / 1000);
      } else if (!activo && pintados == record) tiempoRecord = Math.max(0, (fin - inicio) / 1000);
    }
  }

  public record Auto(String placas, String propietario, Instant entrada) {}

  public record Recibo(Auto auto, Instant salida, long segundos, BigDecimal costo) {}

  /** Cada auto es un nodo; el último enlaza al primero y viceversa. Sin cupo fijo. */
  public static class ColaCircularDoblementeLigada {
    private static class Nodo {
      Auto auto;
      Nodo anterior, siguiente;

      Nodo(Auto auto) {
        this.auto = auto;
      }
    }

    private Nodo frente;
    private int cantidad;

    public boolean ColaVacia() {
      return frente == null;
    }

    public int size() {
      return cantidad;
    }

    public List<Auto> lista() {
      List<Auto> r = new ArrayList<>();
      if (frente == null) return r;
      Nodo actual = frente;
      do {
        r.add(actual.auto);
        actual = actual.siguiente;
      } while (actual != frente);
      return r;
    }

    public void insertar(String placas, String propietario, Instant ahora) {
      String p = texto(placas).toUpperCase(Locale.ROOT);
      if (lista().stream().anyMatch(a -> a.placas().equals(p)))
        throw new IllegalArgumentException("Las placas ya están registradas.");
      Nodo n = new Nodo(new Auto(p, texto(propietario), ahora));
      if (frente == null) {
        n.anterior = n;
        n.siguiente = n;
        frente = n;
      } else {
        Nodo ultimo = frente.anterior;
        n.anterior = ultimo;
        n.siguiente = frente;
        ultimo.siguiente = n;
        frente.anterior = n;
      }
      cantidad++;
    }

    public Recibo salir(Instant ahora) {
      if (ColaVacia()) throw new IllegalArgumentException("El estacionamiento está vacío.");
      Nodo n = frente;
      if (cantidad == 1) frente = null;
      else {
        Nodo ultimo = frente.anterior;
        frente = frente.siguiente;
        ultimo.siguiente = frente;
        frente.anterior = ultimo;
      }
      cantidad--;
      long segundos = Math.max(0, Duration.between(n.auto.entrada(), ahora).getSeconds());
      return new Recibo(
          n.auto, ahora, segundos, BigDecimal.valueOf(segundos).multiply(BigDecimal.valueOf(2)));
    }

    public boolean enlacesValidos() {
      if (frente == null) return cantidad == 0;
      Nodo n = frente;
      int vistos = 0;
      do {
        if (n.siguiente.anterior != n || n.anterior.siguiente != n) return false;
        n = n.siguiente;
        vistos++;
        if (vistos > cantidad) return false;
      } while (n != frente);
      return vistos == cantidad;
    }
  }
}
