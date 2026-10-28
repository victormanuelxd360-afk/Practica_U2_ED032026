using System.Text;

namespace Practica;

public static partial class Algoritmos
{
    public static string Invertir(string entrada)
    {
        Stack<Rune> pila = new(Validar.Texto(entrada).EnumerateRunes());
        StringBuilder r = new();
        while (pila.Count > 0) r.Append(pila.Pop().ToString());
        return r.ToString();
    }
}
