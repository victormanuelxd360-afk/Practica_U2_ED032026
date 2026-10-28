namespace Practica;

public enum ColorAuto { Rojo, Azul, Verde, Amarillo, Naranja }
public record Coche(int Numero, ColorAuto Color);
public sealed class Juego
{
    public Cola<Coche> Coches { get; } = new(5);
    public bool Activo { get; private set; }
    public int Pintados { get; private set; }
    public int Record { get; set; }
    public long TiempoRecord { get; set; }
    public long Inicio, Fin, ProximaLlegada;
    private int secuencia;
    // Dificultad por niveles: los cinco primeros aciertos son fáciles,
    // los tres siguientes son intermedios y después comienza el modo mega difícil.
    public long Intervalo => Pintados < 5 ? 20000 : Pintados < 8 ? 10000 : 2000;
    public string Dificultad => Pintados < 5 ? "Fácil" : Pintados < 8 ? "Media" : "Mega difícil";
    private void Encolar() => Coches.InsertaCola(new Coche(++secuencia, (ColorAuto)Random.Shared.Next(5)));
    public void Iniciar(long ahora)
    { while (!Coches.ColaVacia()) Coches.EliminaCola(); Pintados = secuencia = 0; Inicio = Fin = ahora; Activo = true; Encolar(); ProximaLlegada = ahora + Intervalo; }
    public void Actualizar(long ahora)
    {
        while (Activo && ahora >= ProximaLlegada)
        {
            long llegada = ProximaLlegada; Encolar();
            if (Coches.Count == 5) { Activo = false; Fin = llegada; GuardarRecord(llegada); }
            else ProximaLlegada += Intervalo;
        }
    }
    public void Pintar(ColorAuto color, long ahora)
    {
        Actualizar(ahora);
        if (!Activo) throw new ArgumentException("Inicia una partida. El juego termina con cinco coches.");
        if (Coches.ColaVacia()) throw new ArgumentException("Espera al siguiente coche.");
        if (Coches.Frente().Color != color) throw new ArgumentException("Color incorrecto: pinta el primer coche de la cola.");
        Coches.EliminaCola(); Pintados++;
        ProximaLlegada = Math.Min(ProximaLlegada, ahora + Intervalo);
        GuardarRecord(ahora);
    }
    public long Transcurrido(long ahora) => Math.Max(0, ((Activo ? ahora : Fin) - Inicio) / 1000);
    private void GuardarRecord(long ahora)
    {
        if (Pintados > Record) { Record = Pintados; TiempoRecord = Math.Max(0, (ahora - Inicio) / 1000); }
        else if (!Activo && Pintados == Record) TiempoRecord = Math.Max(0, (Fin - Inicio) / 1000);
    }
}
