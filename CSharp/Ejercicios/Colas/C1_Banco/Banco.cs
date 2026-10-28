namespace Practica;

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
