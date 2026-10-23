using System.Globalization;
using System.Text;

namespace Practica;

public static class Validar
{
    public static string Texto(string valor) => string.IsNullOrWhiteSpace(valor)
        ? throw new ArgumentException("Hay datos faltantes.") : valor.Trim();
    public static int Entero(string valor, int min = int.MinValue, int max = int.MaxValue)
    {
        if (!int.TryParse(Texto(valor), out int n)) throw new ArgumentException("Introducir sólo números enteros.");
        if (n < min || n > max) throw new ArgumentException($"Introducir un entero entre {min} y {max}.");
        return n;
    }
    public static decimal Decimal(string valor, decimal min, decimal max)
    {
        if (!decimal.TryParse(Texto(valor).Replace(',', '.'), NumberStyles.AllowDecimalPoint | NumberStyles.AllowLeadingSign,
            CultureInfo.InvariantCulture, out decimal n)) throw new ArgumentException("Introducir sólo números decimales.");
        if (n < min || n > max) throw new ArgumentException($"Número fuera de rango: {min} a {max}.");
        return n;
    }
}

public record Producto(string Clave, string Nombre, int Cantidad, decimal Precio);
public record Alumno(string Nombre, decimal Calificacion);
public sealed class Almacen
{
    public List<Producto> Disponibles { get; } = [];
    public List<Producto> Retirados { get; } = [];
    private int secuencia;
    public Producto Escanear()
    {
        int n = ++secuencia;
        var p = new Producto($"P{n}", $"producto{n}", Random.Shared.Next(1, 21), Random.Shared.Next(100, 50001) / 100m);
        Disponibles.Add(p);
        return p;
    }
    public void Retirar(string clave)
    {
        string k = Validar.Texto(clave);
        var p = Disponibles.Find(p => p.Clave.Equals(k, StringComparison.OrdinalIgnoreCase))
            ?? throw new ArgumentException("Clave no encontrada entre disponibles.");
        Disponibles.Remove(p);
        Retirados.Add(p);
    }
}
public sealed class Grupo
{
    public List<Alumno> Aprobados { get; } = [];
    public List<Alumno> Reprobados { get; } = [];
    public void Agregar(string nombre, decimal nota)
    {
        if (nota < 0 || nota > 10) throw new ArgumentException("Calificación entre 0 y 10.");
        Aprobados.Add(new Alumno(Validar.Texto(nombre), nota));
        foreach (var a in Aprobados.Where(a => a.Calificacion < 7).ToList())
        { Aprobados.Remove(a); Reprobados.Add(a); }
    }
}
public sealed class Compra
{
    public List<Producto> Productos { get; } = [];
    public void Agregar(string clave, string nombre, decimal precio)
    {
        string k = Validar.Texto(clave);
        if (Productos.Any(p => p.Clave.Equals(k, StringComparison.OrdinalIgnoreCase))) throw new ArgumentException("La clave ya existe.");
        if (precio < 0) throw new ArgumentException("El precio no puede ser negativo.");
        Productos.Add(new Producto(k, Validar.Texto(nombre), 1, precio));
    }
    public void Eliminar(string clave)
    {
        string k = Validar.Texto(clave);
        if (Productos.RemoveAll(p => p.Clave.Equals(k, StringComparison.OrdinalIgnoreCase)) == 0) throw new ArgumentException("Clave no encontrada.");
    }
    public List<Producto> Ordenados() => Productos.OrderBy(p => p.Nombre, StringComparer.Create(new CultureInfo("es-MX"), true)).ToList();
    public decimal Total() => Productos.Sum(p => p.Precio);
}
public static class Algoritmos
{
    public static (List<int> Original, List<int> Pares, List<int> Impares) Clasificar(int cantidad)
    {
        if (cantidad < 1 || cantidad > 500) throw new ArgumentException("Cantidad entre 1 y 500.");
        List<int> original = [], pares = [], impares = [];
        for (int i = 0; i < cantidad; i++) { int n = Random.Shared.Next(1000); original.Add(n); (n % 2 == 0 ? pares : impares).Add(n); }
        return (original, pares, impares);
    }
    public static SortedDictionary<string, List<string>> Agrupar(IEnumerable<string> palabras)
    {
        SortedDictionary<string, List<string>> grupos = new(StringComparer.Create(new CultureInfo("es-MX"), true));
        foreach (string entrada in palabras)
        {
            string p = Validar.Texto(entrada);
            if (!p.EnumerateRunes().All(Rune.IsLetter)) throw new ArgumentException("Introduce palabras formadas sólo por letras.");
            string inicial = p.EnumerateRunes().First().ToString().ToUpperInvariant();
            if (!grupos.ContainsKey(inicial)) grupos[inicial] = [];
            grupos[inicial].Add(p);
        }
        return grupos;
    }
    public static string Invertir(string entrada)
    {
        Stack<Rune> pila = new(Validar.Texto(entrada).EnumerateRunes());
        StringBuilder r = new();
        while (pila.Count > 0) r.Append(pila.Pop().ToString());
        return r.ToString();
    }
    public static bool Palindromo(string entrada)
    {
        string normal = string.Concat(Validar.Texto(entrada).ToLowerInvariant().EnumerateRunes().Where(Rune.IsLetterOrDigit).Select(r => r.ToString()));
        if (normal.Length == 0) throw new ArgumentException("Introduce al menos una letra o número.");
        return normal == Invertir(normal);
    }
    private static Stack<int> Digitos(string entrada)
    {
        string s = Validar.Texto(entrada);
        if (s.Any(c => c < '0' || c > '9')) throw new ArgumentException("Introducir enteros no negativos, sin signos ni separadores.");
        return new Stack<int>(s.Select(c => c - '0'));
    }
    public static string SumarGrandes(string a, string b)
    {
        var p = Digitos(a); var q = Digitos(b); Stack<int> resultado = new(); int acarreo = 0;
        while (p.Count > 0 || q.Count > 0 || acarreo > 0)
        { int n = acarreo + (p.Count > 0 ? p.Pop() : 0) + (q.Count > 0 ? q.Pop() : 0); resultado.Push(n % 10); acarreo = n / 10; }
        string s = string.Concat(resultado).TrimStart('0');
        return s.Length == 0 ? "0" : s;
    }
    public static int Reemplazar(Stack<int> pila, int nuevo, int viejo)
    {
        Stack<int> auxiliar = new(); int cambios = 0;
        while (pila.Count > 0) { int n = pila.Pop(); if (n == viejo) { n = nuevo; cambios++; } auxiliar.Push(n); }
        while (auxiliar.Count > 0) pila.Push(auxiliar.Pop());
        return cambios;
    }
}
public sealed class Cola<T>(int capacidad)
{
    private readonly Queue<T> datos = new();
    public int Capacidad { get; } = capacidad > 0 ? capacidad : throw new ArgumentException("Capacidad inválida.");
    public int Count => datos.Count;
    public bool ColaLlena() => Count >= Capacidad;
    public bool ColaVacia() => Count == 0;
    public IReadOnlyList<T> Lista() => datos.ToArray();
    public T Frente() => !ColaVacia() ? datos.Peek() : throw new ArgumentException("La cola está vacía.");
    public T Final() => !ColaVacia() ? datos.Last() : throw new ArgumentException("La cola está vacía.");
    public void InsertaCola(T valor) { if (ColaLlena()) throw new ArgumentException("La cola está llena."); datos.Enqueue(valor); }
    public T EliminaCola() => !ColaVacia() ? datos.Dequeue() : throw new ArgumentException("La cola está vacía.");
}
public record Cliente(int Turno, string Nombre, string Movimiento, DateTime Llegada);
public sealed class Banco(int capacidad)
{
    public Cola<Cliente> Clientes { get; } = new(capacidad);
    private int turno;
    public Cliente Llegar(string nombre, string movimiento, DateTime ahora)
    {
        if (Clientes.ColaLlena()) throw new ArgumentException("La cola está llena.");
        var c = new Cliente(turno + 1, Validar.Texto(nombre), Validar.Texto(movimiento), ahora);
        Clientes.InsertaCola(c); turno++; return c;
    }
    public (Cliente Cliente, long Segundos) Atender(DateTime ahora)
    { var c = Clientes.EliminaCola(); return (c, Math.Max(0, (long)(ahora - c.Llegada).TotalSeconds)); }
}
public record Auto(string Placas, string Propietario, DateTime Entrada);
public record Recibo(Auto Auto, DateTime Salida, long Segundos, decimal Costo);
public sealed class ColaCircularDoblementeLigada
{
    private sealed class Nodo(Auto auto) { public Auto Auto = auto; public Nodo Anterior = null!, Siguiente = null!; }
    private Nodo? frente;
    public int Count { get; private set; }
    public bool ColaVacia() => frente is null;
    public List<Auto> Lista()
    {
        List<Auto> lista = []; if (frente is null) return lista;
        Nodo n = frente; do { lista.Add(n.Auto); n = n.Siguiente; } while (n != frente); return lista;
    }
    public void Insertar(string placas, string propietario, DateTime ahora)
    {
        string p = Validar.Texto(placas).ToUpperInvariant();
        if (Lista().Any(a => a.Placas == p)) throw new ArgumentException("Las placas ya están registradas.");
        Nodo n = new(new Auto(p, Validar.Texto(propietario), ahora));
        if (frente is null) { n.Anterior = n.Siguiente = n; frente = n; }
        else { Nodo ultimo = frente.Anterior; n.Anterior = ultimo; n.Siguiente = frente; ultimo.Siguiente = n; frente.Anterior = n; }
        Count++;
    }
    public Recibo Salir(DateTime ahora)
    {
        Nodo n = frente ?? throw new ArgumentException("El estacionamiento está vacío.");
        if (Count == 1) frente = null;
        else { frente = n.Siguiente; frente.Anterior = n.Anterior; n.Anterior.Siguiente = frente; }
        Count--; long segundos = Math.Max(0, (long)(ahora - n.Auto.Entrada).TotalSeconds);
        return new Recibo(n.Auto, ahora, segundos, segundos * 2m);
    }
    public bool EnlacesValidos()
    {
        if (frente is null) return Count == 0;
        Nodo n = frente; int vistos = 0;
        do { if (n.Siguiente.Anterior != n || n.Anterior.Siguiente != n || ++vistos > Count) return false; n = n.Siguiente; } while (n != frente);
        return vistos == Count;
    }
}
public enum ColorAuto { Rojo, Azul, Verde, Amarillo, Naranja }
public record Coche(int Numero, ColorAuto Color);
public sealed class Juego
{
    public Cola<Coche> Coches { get; } = new(5);
    public bool Activo { get; private set; }
    public int Pintados { get; private set; }
    public int Record { get; set; }
    public long TiempoRecord { get; set; }
    public long Inicio, Fin, ProximaLlegada;
    private int secuencia;
    public long Intervalo => Math.Max(2000, 20000 - Pintados * 2000L);
    private void Encolar() => Coches.InsertaCola(new Coche(++secuencia, (ColorAuto)Random.Shared.Next(5)));
    public void Iniciar(long ahora)
    { while (!Coches.ColaVacia()) Coches.EliminaCola(); Pintados = secuencia = 0; Inicio = Fin = ahora; Activo = true; Encolar(); ProximaLlegada = ahora + Intervalo; }
    public void Actualizar(long ahora)
    {
        while (Activo && ahora >= ProximaLlegada)
        {
            long llegada = ProximaLlegada; Encolar();
            if (Coches.Count == 5) { Activo = false; Fin = llegada; GuardarRecord(llegada); }
            else ProximaLlegada += Intervalo;
        }
    }
    public void Pintar(ColorAuto color, long ahora)
    {
        Actualizar(ahora);
        if (!Activo) throw new ArgumentException("Inicia una partida. El juego termina con cinco coches.");
        if (Coches.ColaVacia()) throw new ArgumentException("Espera al siguiente coche.");
        if (Coches.Frente().Color != color) throw new ArgumentException("Color incorrecto: pinta el primer coche de la cola.");
        Coches.EliminaCola(); Pintados++;
        ProximaLlegada = Math.Min(ProximaLlegada, ahora + Intervalo);
        GuardarRecord(ahora);
    }
    public long Transcurrido(long ahora) => Math.Max(0, ((Activo ? ahora : Fin) - Inicio) / 1000);
    private void GuardarRecord(long ahora)
    {
        if (Pintados > Record) { Record = Pintados; TiempoRecord = Math.Max(0, (ahora - Inicio) / 1000); }
        else if (!Activo && Pintados == Record) TiempoRecord = Math.Max(0, (Fin - Inicio) / 1000);
    }
}
