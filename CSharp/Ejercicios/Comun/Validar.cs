using System.Globalization;

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
