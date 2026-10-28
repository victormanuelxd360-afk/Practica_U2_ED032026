namespace Practica;

public record Alumno(string Nombre, decimal Calificacion);
public sealed class Grupo
{
    public List<Alumno> Aprobados { get; } = [];
    public List<Alumno> Reprobados { get; } = [];
    public void Agregar(string nombre, decimal nota)
    {
        if (nota < 0 || nota > 10) throw new ArgumentException("Calificación entre 0 y 10.");
        Aprobados.Add(new Alumno(Validar.Texto(nombre), nota));
        foreach (var a in Aprobados.Where(a => a.Calificacion < 7).ToList())
        { Aprobados.Remove(a); Reprobados.Add(a); }
    }
}
