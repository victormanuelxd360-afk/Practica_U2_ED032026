using Microsoft.Extensions.Caching.Memory;
using Practica;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddMemoryCache(o => o.SizeLimit = 1000);
var app = builder.Build();
app.Use(async (context, next) => {
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    context.Response.Headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'";
    if (context.Request.Path.StartsWithSegments("/api")) context.Response.Headers.CacheControl = "no-store";
    await next();
});
app.UseDefaultFiles();
app.UseStaticFiles();

Estado Sesion(HttpContext context, IMemoryCache cache)
{
    string? id = context.Request.Cookies["practica-sesion"];
    if (id is null || !Guid.TryParseExact(id, "N", out _) || !cache.TryGetValue<Estado>(id, out var estado))
    {
        id = Guid.NewGuid().ToString("N");
        estado = new Estado();
        cache.Set(id, estado, new MemoryCacheEntryOptions { SlidingExpiration = TimeSpan.FromHours(2), Size = 1 });
        context.Response.Cookies.Append("practica-sesion", id, new CookieOptions { HttpOnly = true, SameSite = SameSiteMode.Strict, Secure = context.Request.IsHttps, IsEssential = true });
    }
    return estado!;
}

app.MapGet("/api/estado", (HttpContext context, IMemoryCache cache) => {
    var estado = Sesion(context, cache);
    lock (estado) return Results.Json(estado.Vista());
});
app.MapPost("/api/accion", (Solicitud solicitud, HttpContext context, IMemoryCache cache) => {
    if (context.Request.Headers["X-Practica"] != "1") return Results.BadRequest(new { error = "Solicitud no válida. Recarga la página." });
    if (solicitud.Valores is null || solicitud.Valores.Count > 10 || solicitud.Valores.Values.Any(s => s is null || s.Length > 20000)) return Results.BadRequest(new { error = "Los datos exceden el tamaño permitido." });
    var estado = Sesion(context, cache);
    lock (estado)
    {
        try { string mensaje = estado.Ejecutar(solicitud); return Results.Json(new { mensaje, estado = estado.Vista() }); }
        catch (ArgumentException ex) { return Results.BadRequest(new { error = ex.Message }); }
        catch (OverflowException) { return Results.BadRequest(new { error = "El número o total excede el rango permitido." }); }
    }
});
app.Run();

public record Solicitud(string Modulo, string Accion, Dictionary<string, string> Valores);
public sealed class Estado
{
    private readonly Almacen almacen = new();
    private readonly Grupo grupo = new();
    private readonly Compra compra = new();
    private readonly List<string> palabras = [];
    private Banco banco = new(5);
    private readonly Juego juego = new();
    private readonly ColaCircularDoblementeLigada parking = new();
    private readonly Dictionary<string, object> resultados = new();
    private static readonly string[] movimientos = ["Pago de servicio", "Depósito", "Retiro", "Compra de tiempo-aire", "Consulta de saldo"];
    public string Ejecutar(Solicitud s)
    {
        string V(string nombre) => s.Valores.TryGetValue(nombre, out string? valor) ? valor : "";
        switch ($"{s.Modulo}/{s.Accion}")
        {
            case "L1/escanear": almacen.Escanear(); break;
            case "L1/retirar": almacen.Retirar(V("clave")); break;
            case "L2/generar": var r = Algoritmos.Clasificar(Validar.Entero(V("cantidad"), 1, 500)); resultados["L2"] = new { r.Original, r.Pares, r.Impares }; break;
            case "L3/agregar": grupo.Agregar(V("nombre"), Validar.Decimal(V("nota"), 0, 10)); break;
            case "L4/agregar":
                decimal precio = Validar.Decimal(V("precio"), 0, decimal.MaxValue);
                if (compra.Total() > decimal.MaxValue - precio) throw new ArgumentException("El total excede el rango permitido.");
                compra.Agregar(V("clave"), V("nombre"), precio); break;
            case "L4/eliminar": compra.Eliminar(V("clave")); break;
            case "L5/agregar":
                string palabra = Validar.Texto(V("palabra")); Algoritmos.Agrupar([palabra]); palabras.Add(palabra); break;
            case "P1/invertir": resultados["P1"] = new { resultado = Algoritmos.Invertir(V("texto")) }; break;
            case "P2/comprobar": resultados["P2"] = new { resultado = Algoritmos.Palindromo(V("texto")) ? "Sí es palíndromo." : "No es palíndromo." }; break;
            case "P3/sumar": resultados["P3"] = new { resultado = Algoritmos.SumarGrandes(V("a"), V("b")) }; break;
            case "P4/reemplazar":
                Stack<int> pila = new(Validar.Texto(V("valores")).Split(',').Select(x => Validar.Entero(x)));
                int cambios = Algoritmos.Reemplazar(pila, Validar.Entero(V("nuevo")), Validar.Entero(V("viejo")));
                resultados["P4"] = new { pila = pila.ToArray(), cambios }; break;
            case "C1/configurar":
                if (!banco.Clientes.ColaVacia()) throw new ArgumentException("Configura la capacidad con la cola vacía.");
                banco = new Banco(Validar.Entero(V("capacidad"), 1, 1000)); break;
            case "C1/agregar":
                if (!movimientos.Contains(V("movimiento"))) throw new ArgumentException("Selecciona un movimiento válido.");
                banco.Llegar(V("nombre"), V("movimiento"), DateTime.Now); break;
            case "C1/atender": var at = banco.Atender(DateTime.Now); resultados["atencion"] = new { at.Cliente, at.Segundos }; break;
            case "C2/iniciar": juego.Iniciar(Environment.TickCount64); break;
            case "C2/pintar":
                if (!Enum.TryParse<ColorAuto>(V("color"), out var color) || !Enum.IsDefined(color)) throw new ArgumentException("Selecciona un color válido.");
                juego.Pintar(color, Environment.TickCount64); break;
            case "C3/entrar": parking.Insertar(V("placas"), V("propietario"), DateTime.Now); break;
            case "C3/salir": resultados["recibo"] = parking.Salir(DateTime.Now); break;
            default: throw new ArgumentException("Opción no encontrada.");
        }
        return "Operación realizada correctamente.";
    }
    public object Vista()
    {
        juego.Actualizar(Environment.TickCount64);
        return new {
            L1 = new { disponibles = almacen.Disponibles.ToArray(), retirados = almacen.Retirados.ToArray() },
            L2 = resultados.GetValueOrDefault("L2"),
            L3 = new { aprobados = grupo.Aprobados.ToArray(), reprobados = grupo.Reprobados.ToArray() },
            L4 = new { productos = compra.Ordenados(), total = compra.Total() },
            L5 = new { original = palabras.ToArray(), grupos = Algoritmos.Agrupar(palabras) },
            P1 = resultados.GetValueOrDefault("P1"), P2 = resultados.GetValueOrDefault("P2"), P3 = resultados.GetValueOrDefault("P3"), P4 = resultados.GetValueOrDefault("P4"),
            C1 = new { clientes = banco.Clientes.Lista(), capacidad = banco.Clientes.Capacidad, frente = banco.Clientes.ColaVacia() ? -1 : banco.Clientes.Frente().Turno, final = banco.Clientes.ColaVacia() ? -1 : banco.Clientes.Final().Turno, atencion = resultados.GetValueOrDefault("atencion") },
            C2 = new { coches = juego.Coches.Lista().Select(c => new { c.Numero, color = c.Color.ToString() }).ToArray(), juego.Activo, juego.Pintados, juego.Record, juego.TiempoRecord, segundos = juego.Transcurrido(Environment.TickCount64), intervalo = juego.Intervalo / 1000 },
            C3 = new { autos = parking.Lista(), recibo = resultados.GetValueOrDefault("recibo") }
        };
    }
}
