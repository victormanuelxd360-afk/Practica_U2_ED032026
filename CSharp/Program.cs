namespace Practica;

internal static class Program
{
    [STAThread]
    private static int Main(string[] args)
    {
        ApplicationConfiguration.Initialize();
        if (args.Contains("--probar")) return Pruebas.Ejecutar();
        string categoria = args.FirstOrDefault() ?? System.Reflection.Assembly.GetExecutingAssembly().GetName().Name ?? "Todas";
        using var ventana = new Ventana(categoria);
        if (args.Contains("--evidencias")) { ventana.GuardarEvidencias(); return 0; }
        Application.Run(ventana);
        return 0;
    }
}

public sealed class Modulo : TabPage
{
    public FlowLayoutPanel Campos { get; } = new() { Dock = DockStyle.Top, AutoSize = true, WrapContents = true, Padding = new Padding(10) };
    public TextBox Resultado { get; } = new() { Dock = DockStyle.Fill, Multiline = true, ReadOnly = true, ScrollBars = ScrollBars.Both, Font = new Font("Consolas", 11) };
    public Label Estado { get; } = new() { Dock = DockStyle.Bottom, Height = 65, Padding = new Padding(10), ForeColor = Color.DarkGreen };
    public DataGridView Tabla { get; } = new() { Dock = DockStyle.Top, Height = 230, ReadOnly = true, AllowUserToAddRows = false, AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill, RowHeadersVisible = false };
    public Modulo(string titulo, string descripcion) : base(titulo)
    {
        BackColor = Color.FromArgb(242, 246, 250);
        Controls.Add(Resultado); Controls.Add(Tabla); Controls.Add(Campos); Controls.Add(Estado);
        Tabla.Visible = false; Estado.Text = descripcion;
    }
    public TextBox Campo(string etiqueta, string valor = "")
    {
        Campos.Controls.Add(new Label { Text = etiqueta, AutoSize = true, Margin = new Padding(8, 9, 3, 3) });
        TextBox t = new() { Text = valor, Width = 150 }; Campos.Controls.Add(t); return t;
    }
    public Button Boton(string nombre, Action accion)
    {
        Button b = new() { Text = nombre, AutoSize = true, BackColor = Color.FromArgb(27, 52, 87), ForeColor = Color.White, FlatStyle = FlatStyle.Flat };
        b.Click += (_, _) => Ejecutar(accion); Campos.Controls.Add(b); return b;
    }
    public void Ejecutar(Action accion)
    {
        try { accion(); Estado.ForeColor = Color.DarkGreen; }
        catch (Exception ex) when (ex is ArgumentException or OverflowException or IOException or UnauthorizedAccessException)
        { Estado.Text = ex is OverflowException ? "El número o total excede el rango permitido." : ex.Message; Estado.ForeColor = Color.Firebrick; }
    }
    public void Mostrar<T>(IEnumerable<T> lista) { Tabla.Visible = true; Tabla.DataSource = lista.ToList(); }
}

public sealed class Ventana : Form
{
    private readonly TabControl pestanas = new() { Dock = DockStyle.Fill, Multiline = true };
    private readonly System.Windows.Forms.Timer reloj = new() { Interval = 200 };
    private readonly Juego juego = new();
    private readonly Panel dibujo = new() { Dock = DockStyle.Top, Height = 150, BackColor = Color.White };
    private readonly string archivoRecord = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Practica_U2_CSharp", "record.txt");
    private readonly string categoria;
    public List<Modulo> Modulos { get; } = [];
    private static long Ahora => Environment.TickCount64;
    public Ventana(string categoria = "Todas")
    {
        this.categoria = categoria;
        Text = "Práctica Unidad II — C# — Listas, Pilas y Colas";
        Size = new Size(1240, 780); MinimumSize = new Size(1000, 650); StartPosition = FormStartPosition.CenterScreen;
        Font = new Font("Segoe UI", 10);
        Controls.Add(pestanas);
        MenuStrip menu = new();
        foreach (string c in new[] { "Todas", "Listas", "Pilas", "Colas" })
        {
            string seleccion = c;
            menu.Items.Add(c, null, (_, _) => { foreach (var m in Modulos) if (seleccion == "Todas" || m.Tag?.ToString() == seleccion) { pestanas.SelectedTab = m; break; } });
        }
        menu.Items.Add("Salir", null, (_, _) => Close()); Controls.Add(menu); MainMenuStrip = menu;
        CrearListas(); CrearPilas(); CrearColas();
        FormClosed += (_, _) => reloj.Dispose();
    }
    private Modulo Crear(string estructura, string titulo, string descripcion)
    {
        Modulo m = new(titulo, descripcion) { Tag = estructura };
        Modulos.Add(m);
        if (categoria.Equals(estructura, StringComparison.OrdinalIgnoreCase) || !new[] { "Listas", "Pilas", "Colas" }.Contains(categoria)) pestanas.TabPages.Add(m);
        return m;
    }
    private static string Productos(IEnumerable<Producto> lista) => string.Join(Environment.NewLine, lista.Select(p => $"{p.Clave,-8} {p.Nombre,-25} Cantidad: {p.Cantidad,3}  Precio: ${p.Precio:F2}"));
    private void CrearListas()
    {
        Almacen almacen = new();
        var m = Crear("Listas", "L1. Productos disponibles y retirados", "Escanea productos con cantidad y precio aleatorios. Retira por clave.");
        var clave = m.Campo("Clave:");
        void Refrescar() { m.Resultado.Text = $"DISPONIBLES ({almacen.Disponibles.Count})\r\n{Productos(almacen.Disponibles)}\r\n\r\nRETIRADOS ({almacen.Retirados.Count})\r\n{Productos(almacen.Retirados)}"; }
        m.Boton("Escanear producto", () => { var p = almacen.Escanear(); Refrescar(); m.Estado.Text = $"Se agregó {p.Nombre}."; });
        m.Boton("Retirar producto", () => { almacen.Retirar(clave.Text); Refrescar(); m.Estado.Text = "Producto retirado."; });

        var pares = Crear("Listas", "L2. Pares e impares", "Genera de 1 a 500 números aleatorios entre 0 y 999.");
        var cantidad = pares.Campo("Cantidad:", "20");
        pares.Boton("Generar y separar", () => { var r = Algoritmos.Clasificar(Validar.Entero(cantidad.Text, 1, 500)); pares.Resultado.Text = $"ORIGINAL\r\n{string.Join(", ", r.Original)}\r\n\r\nPARES\r\n{string.Join(", ", r.Pares)}\r\n\r\nIMPARES\r\n{string.Join(", ", r.Impares)}"; pares.Estado.Text = "Números clasificados."; });

        Grupo grupo = new();
        var alumnos = Crear("Listas", "L3. Aprobados y reprobados", "Calificaciones decimales de 0 a 10. Se aprueba desde 7.");
        var nombre = alumnos.Campo("Alumno:"); var nota = alumnos.Campo("Calificación:");
        alumnos.Boton("Agregar y clasificar", () => { grupo.Agregar(nombre.Text, Validar.Decimal(nota.Text, 0, 10)); alumnos.Resultado.Text = "APROBADOS\r\n" + string.Join("\r\n", grupo.Aprobados.Select(a => $"{a.Nombre}: {a.Calificacion}")) + "\r\n\r\nREPROBADOS\r\n" + string.Join("\r\n", grupo.Reprobados.Select(a => $"{a.Nombre}: {a.Calificacion}")); alumnos.Estado.Text = "Alumno registrado."; });

        Compra compra = new();
        var compras = Crear("Listas", "L4. Eliminar y ordenar productos", "Claves únicas; productos ordenados por nombre y total decimal exacto.");
        var k = compras.Campo("Clave:"); var producto = compras.Campo("Producto:"); var precio = compras.Campo("Precio:");
        void ActualizarCompra() { compras.Mostrar(compra.Ordenados()); compras.Resultado.Text = $"TOTAL DE COMPRA: ${compra.Total():F2}"; }
        compras.Boton("Agregar", () => { decimal p = Validar.Decimal(precio.Text, 0, decimal.MaxValue); if (compra.Total() > decimal.MaxValue - p) throw new ArgumentException("El total excede el rango permitido."); compra.Agregar(k.Text, producto.Text, p); ActualizarCompra(); compras.Estado.Text = "Producto agregado."; });
        compras.Boton("Eliminar por clave", () => { compra.Eliminar(k.Text); ActualizarCompra(); compras.Estado.Text = "Producto eliminado."; });

        List<string> palabras = [];
        var letras = Crear("Listas", "L5. Palabras por letra", "Cada inicial genera su propia lista. Introduce una palabra a la vez.");
        var palabra = letras.Campo("Palabra:");
        letras.Boton("Agregar palabra", () => { string p = Validar.Texto(palabra.Text); Algoritmos.Agrupar([p]); palabras.Add(p); letras.Resultado.Text = "ORIGINAL: " + string.Join(", ", palabras) + "\r\n\r\n" + string.Join("\r\n", Algoritmos.Agrupar(palabras).Select(g => $"{g.Key}: {string.Join(", ", g.Value)}")); letras.Estado.Text = "Palabra clasificada."; });
    }
    private void CrearPilas()
    {
        var invertir = Crear("Pilas", "P1. Invertir palabra", "Invierte mediante Stack<Rune>, conservando caracteres Unicode completos.");
        var palabra = invertir.Campo("Palabra:"); invertir.Boton("Invertir", () => { invertir.Resultado.Text = Algoritmos.Invertir(palabra.Text); invertir.Estado.Text = "Orden invertido con una pila."; });
        var palindromo = Crear("Pilas", "P2. Palíndromo", "Ignora espacios, signos y mayúsculas. Conserva acentos.");
        var frase = palindromo.Campo("Palabra o frase:"); palindromo.Boton("Comprobar", () => { palindromo.Resultado.Text = Algoritmos.Palindromo(frase.Text) ? "Sí es palíndromo." : "No es palíndromo."; palindromo.Estado.Text = "Comparación completada."; });
        var suma = Crear("Pilas", "P3. Suma de números grandes", "Enteros no negativos, sin límite fijo de dígitos. La solución usa pilas, sin BigInteger.");
        var a = suma.Campo("Primer número:"); a.Width = 320; var b = suma.Campo("Segundo número:"); b.Width = 320;
        suma.Boton("Sumar", () => { suma.Resultado.Text = Algoritmos.SumarGrandes(a.Text, b.Text); suma.Estado.Text = "Suma realizada mediante pilas y acarreo."; });
        var reemplazo = Crear("Pilas", "P4. Reemplazar valor", "Valores separados por comas. Se apilan de izquierda a derecha; se muestra primero la cima.");
        var valores = reemplazo.Campo("Valores:", "1,2,3,2"); var viejo = reemplazo.Campo("Viejo:", "2"); var nuevo = reemplazo.Campo("Nuevo:", "9");
        reemplazo.Boton("Reemplazar", () => { Stack<int> pila = new(Validar.Texto(valores.Text).Split(',').Select(s => Validar.Entero(s))); int n = Algoritmos.Reemplazar(pila, Validar.Entero(nuevo.Text), Validar.Entero(viejo.Text)); reemplazo.Resultado.Text = "CIMA → " + string.Join(", ", pila) + $"\r\nReemplazos: {n}"; reemplazo.Estado.Text = "Se conservó el orden de la pila."; });
    }
    private void CrearColas()
    {
        Banco banco = new(5);
        var ventanilla = Crear("Colas", "C1. Ventanilla de banco", "Cola FIFO con capacidad 5. Valida sobreflujo y cola vacía.");
        var capacidad = ventanilla.Campo("Capacidad:", "5");
        void RefrescarBanco() { ventanilla.Mostrar(banco.Clientes.Lista()); ventanilla.Resultado.Text = banco.Clientes.ColaVacia() ? "Frente: -1 | Final: -1" : $"Frente: {banco.Clientes.Frente().Turno} | Final: {banco.Clientes.Final().Turno}"; }
        ventanilla.Boton("Configurar", () => { if (!banco.Clientes.ColaVacia()) throw new ArgumentException("Configura la capacidad con la cola vacía."); banco = new Banco(Validar.Entero(capacidad.Text, 1, 1000)); RefrescarBanco(); ventanilla.Estado.Text = "Capacidad configurada."; });
        var cliente = ventanilla.Campo("Cliente:");
        ComboBox movimiento = new() { DropDownStyle = ComboBoxStyle.DropDownList, Width = 190 };
        movimiento.Items.AddRange(["Pago de servicio", "Depósito", "Retiro", "Compra de tiempo-aire", "Consulta de saldo"]); movimiento.SelectedIndex = 0; ventanilla.Campos.Controls.Add(movimiento);
        ventanilla.Boton("Agregar a la cola", () => { var c = banco.Llegar(cliente.Text, movimiento.Text, DateTime.Now); RefrescarBanco(); ventanilla.Estado.Text = $"Cliente {c.Nombre} formado al final. Turno {c.Turno}, llegada {c.Llegada:HH:mm:ss}."; });
        ventanilla.Boton("Atender en ventanilla", () => { var at = banco.Atender(DateTime.Now); RefrescarBanco(); ventanilla.Estado.Text = $"Atendido: {at.Cliente.Nombre}. Tiempo de espera: {at.Segundos} segundos."; }); RefrescarBanco();

        var coches = Crear("Colas", "C2. Juego de pintar coches", "Pinta el primer coche con el color solicitado. El juego termina al acumular cinco coches.");
        coches.Controls.Add(dibujo); coches.Controls.SetChildIndex(dibujo, 1);
        dibujo.Paint += (_, e) => {
            int x = 15;
            foreach (var c in juego.Coches.Lista())
            {
                e.Graphics.FillRectangle(Brushes.LightSlateGray, x, 45, 140, 40); e.Graphics.FillRectangle(Brushes.LightSlateGray, x + 25, 22, 80, 35);
                e.Graphics.FillRectangle(Brushes.LightBlue, x + 35, 27, 60, 20);
                e.Graphics.FillEllipse(Brushes.Black, x + 15, 70, 28, 28); e.Graphics.FillEllipse(Brushes.Black, x + 100, 70, 28, 28);
                e.Graphics.DrawString($"#{c.Numero}: {c.Color}", Font, Brushes.Black, x, 108); x += 180;
            }
        };
        try { string[] r = File.ReadAllLines(archivoRecord); juego.Record = Validar.Entero(r[0], 0); juego.TiempoRecord = long.Parse(r[1]); }
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException or ArgumentException or FormatException or IndexOutOfRangeException or OverflowException) { juego.Record = 0; juego.TiempoRecord = 0; }
        void GuardarRecord() { Directory.CreateDirectory(Path.GetDirectoryName(archivoRecord)!); File.WriteAllLines(archivoRecord, [juego.Record.ToString(), juego.TiempoRecord.ToString()]); }
        void RefrescarJuego() { coches.Resultado.Text = $"Pintados: {juego.Pintados} | En cola: {juego.Coches.Count}/5\r\nDificultad: {juego.Dificultad} | Tiempo total: {juego.Transcurrido(Ahora)} s | Intervalo: {juego.Intervalo / 1000} s\r\nRécord: {juego.Record} coches en {juego.TiempoRecord} s\r\n" + (juego.Activo ? "Pinta el coche de la izquierda." : "Inicia una nueva partida."); dibujo.Invalidate(); }
        coches.Boton("Iniciar partida", () => { juego.Iniciar(Ahora); reloj.Start(); RefrescarJuego(); coches.Estado.Text = "Partida iniciada."; });
        foreach (ColorAuto color in Enum.GetValues<ColorAuto>()) { ColorAuto c = color; coches.Boton(c.ToString(), () => { juego.Pintar(c, Ahora); GuardarRecord(); RefrescarJuego(); coches.Estado.Text = "Coche pintado correctamente."; }); }
        reloj.Tick += (_, _) => coches.Ejecutar(() => { bool activo = juego.Activo; juego.Actualizar(Ahora); if (activo && !juego.Activo) { reloj.Stop(); GuardarRecord(); coches.Estado.Text = $"Fin del juego. {juego.Pintados} coches pintados; {juego.Transcurrido(Ahora)} segundos."; } RefrescarJuego(); }); RefrescarJuego();

        ColaCircularDoblementeLigada parking = new();
        var estacionamiento = Crear("Colas", "C3. Estacionamiento", "Cola circular doblemente ligada sin cupo fijo. Salida FIFO. Tarifa: $2.00 por segundo completo.");
        var placas = estacionamiento.Campo("Placas:"); var propietario = estacionamiento.Campo("Propietario:");
        estacionamiento.Boton("Entrada de auto", () => { parking.Insertar(placas.Text, propietario.Text, DateTime.Now); estacionamiento.Mostrar(parking.Lista()); estacionamiento.Estado.Text = $"Entrada confirmada. Autos: {parking.Count}."; });
        estacionamiento.Boton("Salida de auto", () => { var r = parking.Salir(DateTime.Now); estacionamiento.Mostrar(parking.Lista()); estacionamiento.Resultado.Text = $"RECIBO\r\nPlacas: {r.Auto.Placas}\r\nPropietario: {r.Auto.Propietario}\r\nEntrada: {r.Auto.Entrada:dd/MM/yyyy HH:mm:ss}\r\nSalida: {r.Salida:dd/MM/yyyy HH:mm:ss}\r\nTiempo: {r.Segundos} segundos\r\nTotal: ${r.Costo:F2}"; estacionamiento.Estado.Text = $"Salida registrada. Autos: {parking.Count}."; });
    }
    public void GuardarEvidencias()
    {
        string carpeta = Path.Combine(Environment.CurrentDirectory, "evidencias-csharp"); Directory.CreateDirectory(carpeta);
        Show();
        foreach (TabPage pagina in pestanas.TabPages)
        {
            pestanas.SelectedTab = pagina; Application.DoEvents();
            Modulo m = (Modulo)pagina;
            TextBox[] campos = m.Campos.Controls.OfType<TextBox>().ToArray();
            void Datos(params string[] valores) { for (int i = 0; i < valores.Length; i++) campos[i].Text = valores[i]; }
            void Pulsar(string texto) { m.Campos.Controls.OfType<Button>().First(b => b.Text == texto).PerformClick(); Application.DoEvents(); }
            switch (pagina.Text[..2])
            {
                case "L1": Pulsar("Escanear producto"); Pulsar("Escanear producto"); Datos("P1"); Pulsar("Retirar producto"); break;
                case "L2": Datos("20"); Pulsar("Generar y separar"); break;
                case "L3": Datos("Ana", "8.5"); Pulsar("Agregar y clasificar"); Datos("Luis", "6.5"); Pulsar("Agregar y clasificar"); break;
                case "L4": Datos("P1", "Arroz", "32.75"); Pulsar("Agregar"); Datos("P2", "Leche", "26.25"); Pulsar("Agregar"); break;
                case "L5": foreach (string p in new[] { "Fresa", "Fresca", "Oso", "Orilla", "Pez" }) { Datos(p); Pulsar("Agregar palabra"); } break;
                case "P1": Datos("UTM"); Pulsar("Invertir"); break;
                case "P2": Datos("Anita lava la tina"); Pulsar("Comprobar"); break;
                case "P3": Datos("999999999999999999999999999999", "1"); Pulsar("Sumar"); break;
                case "P4": Pulsar("Reemplazar"); break;
                case "C1": campos[1].Text = "Ana"; Pulsar("Agregar a la cola"); campos[1].Text = "Luis"; Pulsar("Agregar a la cola"); Pulsar("Atender en ventanilla"); break;
                case "C2": Pulsar("Iniciar partida"); reloj.Stop(); break;
                case "C3": Datos("ABC-123", "Ana"); Pulsar("Entrada de auto"); Datos("XYZ-987", "Luis"); Pulsar("Entrada de auto"); Pulsar("Salida de auto"); break;
            }
            if (m.Estado.ForeColor == Color.Firebrick) throw new InvalidOperationException($"{m.Text}: {m.Estado.Text}");
            using Bitmap imagen = new(Width, Height); DrawToBitmap(imagen, new Rectangle(0, 0, Width, Height));
            imagen.Save(Path.Combine(carpeta, pagina.Text[..2] + ".png"));
        }
        Hide();
    }
}
