using System.Globalization;
using System.Text;

namespace Practica;

public static partial class Algoritmos
{
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
}
