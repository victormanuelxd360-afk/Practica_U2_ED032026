using System.Globalization;

namespace Practica;

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
