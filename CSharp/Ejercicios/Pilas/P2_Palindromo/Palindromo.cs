using System.Text;

namespace Practica;

public static partial class Algoritmos
{
    public static bool Palindromo(string entrada)
    {
        string normal = string.Concat(Validar.Texto(entrada).ToLowerInvariant().EnumerateRunes().Where(Rune.IsLetterOrDigit).Select(r => r.ToString()));
        if (normal.Length == 0) throw new ArgumentException("Introduce al menos una letra o número.");
        return normal == Invertir(normal);
    }
}
