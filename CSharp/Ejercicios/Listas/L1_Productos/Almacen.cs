namespace Practica;

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
