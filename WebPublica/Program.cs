using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.JSInterop;
using System.Text.Json;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<PracticaPublica.App>("#motor-csharp");
await builder.Build().RunAsync();

public static class MotorWeb
{
    private static readonly Estado datos = new();
    private static readonly JsonSerializerOptions opciones = new(JsonSerializerDefaults.Web);

    [JSInvokable]
    public static string Consultar() => JsonSerializer.Serialize(datos.Vista(), opciones);

    [JSInvokable]
    public static void RestaurarRecord(int coches, long segundos) => datos.RestaurarRecord(coches, segundos);

    [JSInvokable]
    public static string Ejecutar(string json)
    {
        try
        {
            var s = JsonSerializer.Deserialize<Solicitud>(json, opciones) ?? throw new ArgumentException("Solicitud vacía.");
            if (s.Valores is null || s.Valores.Count > 10 || s.Valores.Values.Any(s => s is null || s.Length > 20000)) throw new ArgumentException("Los datos exceden el tamaño permitido.");
            string mensaje = datos.Ejecutar(s);
            return JsonSerializer.Serialize(new { mensaje, estado = datos.Vista() }, opciones);
        }
        catch (ArgumentException ex) { return JsonSerializer.Serialize(new { error = ex.Message }); }
        catch (OverflowException) { return JsonSerializer.Serialize(new { error = "El número o total excede el rango permitido." }); }
    }
}
