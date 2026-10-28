namespace Practica;

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
