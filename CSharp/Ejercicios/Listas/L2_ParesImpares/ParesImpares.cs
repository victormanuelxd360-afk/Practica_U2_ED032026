namespace Practica;

public static partial class Algoritmos
{
    public static (List<int> Original, List<int> Pares, List<int> Impares) Clasificar(int cantidad)
    {
        if (cantidad < 1 || cantidad > 500) throw new ArgumentException("Cantidad entre 1 y 500.");
        List<int> original = [], pares = [], impares = [];
        for (int i = 0; i < cantidad; i++) { int n = Random.Shared.Next(1000); original.Add(n); (n % 2 == 0 ? pares : impares).Add(n); }
        return (original, pares, impares);
    }
}
