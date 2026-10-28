namespace Practica;

public static partial class Algoritmos
{
    public static int Reemplazar(Stack<int> pila, int nuevo, int viejo)
    {
        Stack<int> auxiliar = new(); int cambios = 0;
        while (pila.Count > 0) { int n = pila.Pop(); if (n == viejo) { n = nuevo; cambios++; } auxiliar.Push(n); }
        while (auxiliar.Count > 0) pila.Push(auxiliar.Pop());
        return cambios;
    }
}
