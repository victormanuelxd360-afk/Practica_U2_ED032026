namespace Practica;

public static partial class Algoritmos
{
    private static Stack<int> Digitos(string entrada)
    {
        string s = Validar.Texto(entrada);
        if (s.Any(c => c < '0' || c > '9')) throw new ArgumentException("Introducir enteros no negativos, sin signos ni separadores.");
        return new Stack<int>(s.Select(c => c - '0'));
    }
    public static string SumarGrandes(string a, string b)
    {
        var p = Digitos(a); var q = Digitos(b); Stack<int> resultado = new(); int acarreo = 0;
        while (p.Count > 0 || q.Count > 0 || acarreo > 0)
        { int n = acarreo + (p.Count > 0 ? p.Pop() : 0) + (q.Count > 0 ? q.Pop() : 0); resultado.Push(n % 10); acarreo = n / 10; }
        string s = string.Concat(resultado).TrimStart('0');
        return s.Length == 0 ? "0" : s;
    }
}
