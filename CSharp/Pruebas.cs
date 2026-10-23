using System.Numerics;

namespace Practica;

public static class Pruebas
{
    public static int Ejecutar()
    {
        List<string> log = []; int n = 0;
        void Verificar(bool condicion, string nombre) { if (!condicion) throw new Exception(nombre); log.Add($"OK | {++n}. {nombre}"); }
        void Rechaza(Action accion, string nombre) { try { accion(); } catch (ArgumentException) { Verificar(true, nombre); return; } throw new Exception("Debió rechazar: " + nombre); }
        try
        {
            Almacen almacen = new(); for (int i = 0; i < 100; i++) almacen.Escanear();
            Verificar(almacen.Disponibles.Count == 100 && almacen.Disponibles.All(p => p.Cantidad is >= 1 and <= 20 && p.Precio is >= 1 and <= 500), "L1: productos aleatorios y rangos");
            almacen.Retirar("p2"); Verificar(almacen.Disponibles.Count == 99 && almacen.Retirados.Single().Clave == "P2", "L1: retiro e historial"); Rechaza(() => almacen.Retirar("P2"), "L1: retiro duplicado");
            var numeros = Algoritmos.Clasificar(500); Verificar(numeros.Original.Count == 500 && numeros.Pares.All(x => x % 2 == 0) && numeros.Impares.All(x => x % 2 != 0) && numeros.Original.Order().SequenceEqual(numeros.Pares.Concat(numeros.Impares).Order()), "L2: clasificación conserva todos los números"); Rechaza(() => Algoritmos.Clasificar(0), "L2: cantidad inválida");
            Grupo grupo = new(); grupo.Agregar("Ana", 7); grupo.Agregar("Luis", 6.99m); Verificar(grupo.Aprobados.Count == 1 && grupo.Reprobados.Count == 1, "L3: límite de aprobación en siete"); Rechaza(() => grupo.Agregar("X", 11), "L3: calificación inválida");
            Compra compra = new(); compra.Agregar("P1", "Zanahoria", 15.50m); compra.Agregar("P2", "Arroz", 32.75m); Verificar(compra.Total() == 48.25m && compra.Ordenados()[0].Nombre == "Arroz", "L4: orden y total decimal"); compra.Eliminar("p2"); Verificar(compra.Total() == 15.50m, "L4: eliminación por clave"); Rechaza(() => compra.Agregar("p1", "Otro", 1), "L4: clave duplicada");
            var letras = Algoritmos.Agrupar(["Fresa", "Fresca", "Oso", "árbol", "Águila"]); Verificar(letras.Count == 3 && letras["Á"].Count == 2, "L5: listas dinámicas y acentos"); Rechaza(() => Algoritmos.Agrupar(["dos palabras"]), "L5: valida palabra");
            Verificar(Algoritmos.Invertir("UTM") == "MTU" && Algoritmos.Invertir("a😀b") == "b😀a", "P1: inversión y Unicode");
            Verificar(Algoritmos.Palindromo("Anita lava la tina") && Algoritmos.Palindromo("12321") && !Algoritmos.Palindromo("casa"), "P2: frases, números y negativo"); Rechaza(() => Algoritmos.Palindromo("!!!"), "P2: signos sin letras");
            Verificar(Algoritmos.SumarGrandes(new string('9', 1000), "1") == "1" + new string('0', 1000) && Algoritmos.SumarGrandes("000", "0") == "0", "P3: acarreo de mil dígitos y cero");
            Random azar = new(2026); bool sumas = true;
            for (int i = 0; i < 200; i++) { byte[] a = new byte[512], b = new byte[512]; azar.NextBytes(a); azar.NextBytes(b); BigInteger x = new(a, true), y = new(b, true); sumas &= Algoritmos.SumarGrandes(x.ToString(), y.ToString()) == (x + y).ToString(); }
            Verificar(sumas, "P3: 200 sumas contra BigInteger usado sólo en pruebas"); Rechaza(() => Algoritmos.SumarGrandes("-1", "2"), "P3: rechaza negativos");
            Stack<int> pila = new([1, 2, 3, 2]); Verificar(Algoritmos.Reemplazar(pila, 9, 2) == 2 && pila.SequenceEqual([9, 3, 9, 1]), "P4: reemplaza y conserva orden"); Verificar(Algoritmos.Reemplazar(new Stack<int>(), 9, 2) == 0, "P4: pila vacía");
            DateTime t = new(2026, 10, 22, 12, 0, 0); Banco banco = new(2); Rechaza(() => banco.Atender(t), "C1: cola vacía"); banco.Llegar("Ana", "Depósito", t); banco.Llegar("Luis", "Retiro", t.AddSeconds(2)); Rechaza(() => banco.Llegar("Eva", "Retiro", t), "C1: sobreflujo"); Verificar(banco.Clientes.Frente().Turno == 1 && banco.Clientes.Final().Turno == 2 && banco.Atender(t.AddSeconds(18)).Segundos == 18, "C1: FIFO, frente, final y espera");
            Juego juego = new(); juego.Iniciar(0); juego.Actualizar(19999); Verificar(juego.Coches.Count == 1, "C2: no llega antes de veinte segundos"); juego.Actualizar(20000); Verificar(juego.Coches.Count == 2, "C2: llegada exacta a veinte segundos");
            var correcto = juego.Coches.Frente().Color; Rechaza(() => juego.Pintar((ColorAuto)(((int)correcto + 1) % 5), 20001), "C2: color incorrecto"); juego.Pintar(correcto, 20002); juego.Pintar(juego.Coches.Frente().Color, 20003); juego.Actualizar(40000); juego.Pintar(juego.Coches.Frente().Color, 40001); Verificar(juego.Intervalo == 18000 && juego.Record == 3 && juego.TiempoRecord == 40, "C2: aceleración y récord"); juego.Iniciar(0); juego.Actualizar(80000); Verificar(!juego.Activo && juego.Coches.Count == 5 && juego.Transcurrido(90000) == 80, "C2: fin con cinco coches y reloj detenido");
            ColaCircularDoblementeLigada parking = new(); Rechaza(() => parking.Salir(t), "C3: estacionamiento vacío"); parking.Insertar("abc", "Ana", t); parking.Insertar("xyz", "Luis", t); Rechaza(() => parking.Insertar("ABC", "Otra", t), "C3: placas únicas"); var recibo = parking.Salir(t.AddSeconds(30)); Verificar(recibo.Auto.Placas == "ABC" && recibo.Costo == 60 && parking.EnlacesValidos(), "C3: FIFO, cobro y enlaces"); parking.Salir(t);
            bool enlaces = true; for (int i = 0; i < 1000; i++) parking.Insertar($"P{i}", "Dueño", t); for (int i = 0; i < 1000; i++) enlaces &= parking.EnlacesValidos() && parking.Salir(t).Auto.Placas == $"P{i}"; Verificar(enlaces && parking.EnlacesValidos() && parking.Count == 0, "C3: mil nodos, circularidad y eliminación del último");
            Verificar(Validar.Decimal("8,5", 0, 10) == 8.5m, "Validación: coma decimal"); Rechaza(() => Validar.Entero("2.5"), "Validación: entero"); Rechaza(() => Validar.Texto(" "), "Validación: faltantes");
            using Ventana ventana = new(); Verificar(ventana.Modulos.Count == 12, "Interfaz: doce ejercicios");
            var modulo = ventana.Modulos[0]; modulo.Campos.Controls.OfType<Button>().First().PerformClick();
            // Los botones se ejecutan con el formulario visible para validar el flujo real.
            ventana.Show(); Application.DoEvents(); modulo.Campos.Controls.OfType<Button>().First().PerformClick(); Verificar(modulo.Resultado.Text.Contains("producto1"), "Interfaz L1: botón escanear"); ventana.Hide();
            ventana.GuardarEvidencias();
            foreach (var m in ventana.Modulos) Verificar(m.Resultado.Text.Length > 0 && m.Estado.ForeColor != Color.Firebrick, "Interfaz: flujo completo " + m.Text);
            log.Add($"TOTAL: {n} verificaciones correctas. Sin fallos.");
            File.WriteAllLines("pruebas-csharp.txt", log); return 0;
        }
        catch (Exception ex) { log.Add("FALLO: " + ex); File.WriteAllLines("pruebas-csharp.txt", log); return 1; }
    }
}
