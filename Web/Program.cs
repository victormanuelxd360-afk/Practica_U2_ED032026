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
