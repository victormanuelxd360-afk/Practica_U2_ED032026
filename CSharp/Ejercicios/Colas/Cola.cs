namespace Practica;

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
