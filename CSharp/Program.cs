using System.Drawing.Drawing2D;

namespace Practica;

internal static class Program
{
    [STAThread]
    private static int Main(string[] args)
    {
        ApplicationConfiguration.Initialize();
        if (args.Contains("--probar")) return Pruebas.Ejecutar();
        string categoria = args.FirstOrDefault() ?? System.Reflection.Assembly.GetExecutingAssembly().GetName().Name ?? "Todas";
        using var frm = new frmPractica(categoria);
        if (args.Contains("--evidencias")) { frm.GuardarEvidencias(); return 0; }
        Application.Run(frm);
        return 0;
    }
}

// Cada ejercicio es una pestaña; sus controles se nombran con prefijo y el código del ejercicio (txtResultadoL1, btnRetirar...).
public sealed class Modulo : TabPage
{
    public string Codigo { get; }
    public FlowLayoutPanel Campos { get; } = new() { Dock = DockStyle.Top, AutoSize = true, WrapContents = true, Padding = new Padding(10) };
    public TextBox Resultado { get; } = new() { Dock = DockStyle.Fill, Multiline = true, ReadOnly = true, ScrollBars = ScrollBars.Both, Font = new Font("Consolas", 11) };
    public Label Estado { get; } = new() { Dock = DockStyle.Bottom, Height = 65, Padding = new Padding(10), ForeColor = Color.DarkGreen };
    public DataGridView Tabla { get; } = new() { Dock = DockStyle.Top, Height = 230, ReadOnly = true, AllowUserToAddRows = false, AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill, RowHeadersVisible = false };
    public Modulo(string codigo, string titulo, string descripcion) : base($"{codigo}. {titulo}")
    {
        Codigo = codigo; Name = "tab" + codigo;
        Campos.Name = "flpCampos" + codigo; Resultado.Name = "txtResultado" + codigo; Estado.Name = "lblEstado" + codigo; Tabla.Name = "dgvTabla" + codigo;
        BackColor = Color.FromArgb(242, 246, 250);
        Controls.Add(Resultado); Controls.Add(Tabla); Controls.Add(Campos); Controls.Add(Estado);
        Tabla.Visible = false; Estado.Text = descripcion;
    }
    public TextBox Campo(string nombre, string etiqueta, string valor = "")
    {
        Etiqueta(nombre, etiqueta);
        TextBox t = new() { Name = "txt" + nombre, Text = valor, Width = 150 }; Campos.Controls.Add(t); return t;
    }
    public Label Etiqueta(string nombre, string texto)
    {
        Label l = new() { Name = "lbl" + nombre, Text = texto, AutoSize = true, Margin = new Padding(8, 9, 3, 3) }; Campos.Controls.Add(l); return l;
    }
    public Button Boton(string nombre, string texto, Action accion)
    {
        Button b = new() { Name = "btn" + nombre, Text = texto, AutoSize = true, BackColor = Color.FromArgb(27, 52, 87), ForeColor = Color.White, FlatStyle = FlatStyle.Flat };
        b.Click += (_, _) => Ejecutar(accion); Campos.Controls.Add(b); return b;
    }
    public T Control<T>(string nombre) where T : Control => (T)Controls.Find(nombre, true).Single();
    public void Ejecutar(Action accion)
    {
        try { accion(); Estado.ForeColor = Color.DarkGreen; }
        catch (Exception ex) when (ex is ArgumentException or OverflowException or IOException or UnauthorizedAccessException)
        { Estado.Text = ex is OverflowException ? "El número o total excede el rango permitido." : ex.Message; Estado.ForeColor = Color.Firebrick; }
    }
    public void Mostrar<T>(IEnumerable<T> lista) { Tabla.Visible = true; Tabla.DataSource = lista.ToList(); }
}

public sealed class frmPractica : Form
{
    private sealed class Lienzo : Panel { public Lienzo() => DoubleBuffered = true; }
    private readonly TabControl tabEjercicios = new() { Name = "tabEjercicios", Dock = DockStyle.Fill, Multiline = true, ImageList = new ImageList { ColorDepth = ColorDepth.Depth32Bit } };
    private readonly System.Windows.Forms.Timer tmrJuego = new() { Interval = 200 };
    private readonly Juego juego = new();
    private readonly Lienzo pnlCoches = new() { Name = "pnlCoches", Dock = DockStyle.Top, Height = 140, BackColor = Color.White };
    private readonly string archivoRecord = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Practica_U2_CSharp", "record.txt");
    private readonly string categoria;
    public List<Modulo> Modulos { get; } = [];
    // En modo automático (pruebas y capturas) los mensajes se registran sin abrir ventanas modales.
    [System.ComponentModel.DesignerSerializationVisibility(System.ComponentModel.DesignerSerializationVisibility.Hidden)]
    public bool Automatico { get; set; }
    public List<string> Mensajes { get; } = [];
    private static long Ahora => Environment.TickCount64;
    private static readonly string[] Estructuras = ["Listas", "Pilas", "Colas"];
    public frmPractica(string categoria = "Todas")
    {
        this.categoria = categoria;
        Name = "frmPractica";
        Text = "Práctica Unidad II — C# — Listas, Pilas y Colas";
        Size = new Size(1240, 780); MinimumSize = new Size(1000, 650); StartPosition = FormStartPosition.CenterScreen;
        Font = new Font("Segoe UI", 10);
        foreach (string e in Estructuras) tabEjercicios.ImageList!.Images.Add(Icono(e));
        Controls.Add(tabEjercicios);
        MenuStrip mnuPrincipal = new() { Name = "mnuPrincipal" };
        foreach (string c in new[] { "Todas", "Listas", "Pilas", "Colas" })
        {
            string seleccion = c;
            mnuPrincipal.Items.Add(new ToolStripMenuItem(c, null, (_, _) => { foreach (var m in Modulos) if (seleccion == "Todas" || m.Tag?.ToString() == seleccion) { tabEjercicios.SelectedTab = m; break; } }) { Name = "mnu" + c });
        }
        mnuPrincipal.Items.Add(new ToolStripMenuItem("Salir", null, (_, _) => Close()) { Name = "mnuSalir" });
        Controls.Add(mnuPrincipal); MainMenuStrip = mnuPrincipal;
        CrearListas(); CrearPilas(); CrearColas();
        FormClosed += (_, _) => tmrJuego.Dispose();
    }
    private void Mensaje(string titulo, string texto)
    {
        Mensajes.Add($"{titulo}: {texto}");
        if (!Automatico) MessageBox.Show(this, texto, titulo, MessageBoxButtons.OK, MessageBoxIcon.Information);
    }
    private static Bitmap Icono(string estructura)
    {
        Bitmap b = new(16, 16);
        using Graphics g = Graphics.FromImage(b); using SolidBrush azul = new(Color.FromArgb(27, 52, 87));
        for (int i = 0; i < 3; i++)
        {
            if (estructura == "Listas") { g.FillRectangle(azul, 1, 2 + i * 5, 3, 3); g.FillRectangle(azul, 6, 3 + i * 5, 9, 1); }
            else if (estructura == "Pilas") g.FillRectangle(azul, 3, 1 + i * 5, 10, 4);
            else g.FillRectangle(azul, 1 + i * 5, 5, 4, 6);
        }
        return b;
    }
    private Modulo Crear(string estructura, string codigo, string titulo, string descripcion)
    {
        Modulo m = new(codigo, titulo, descripcion) { Tag = estructura, ImageIndex = Array.IndexOf(Estructuras, estructura) };
        Modulos.Add(m);
        if (categoria.Equals(estructura, StringComparison.OrdinalIgnoreCase) || !Estructuras.Contains(categoria)) tabEjercicios.TabPages.Add(m);
        return m;
    }
    private static string Productos(IEnumerable<Producto> lista) => string.Join(Environment.NewLine, lista.Select(p => $"{p.Clave,-8} {p.Nombre,-25} Cantidad: {p.Cantidad,3}  Precio: ${p.Precio:F2}"));
    private void CrearListas()
    {
        Almacen almacen = new();
        var tabL1 = Crear("Listas", "L1", "Productos disponibles y retirados", "Escanea productos con cantidad y precio aleatorios. Retira por clave.");
        var txtClaveRetiro = tabL1.Campo("ClaveRetiro", "Clave:");
        void Refrescar() { tabL1.Resultado.Text = $"DISPONIBLES ({almacen.Disponibles.Count})\r\n{Productos(almacen.Disponibles)}\r\n\r\nRETIRADOS ({almacen.Retirados.Count})\r\n{Productos(almacen.Retirados)}"; }
        tabL1.Boton("Escanear", "Escanear producto", () => { var p = almacen.Escanear(); Refrescar(); tabL1.Estado.Text = $"Se agregó {p.Nombre}."; });
        tabL1.Boton("Retirar", "Retirar producto", () => { almacen.Retirar(txtClaveRetiro.Text); Refrescar(); tabL1.Estado.Text = "Producto retirado."; });

        var tabL2 = Crear("Listas", "L2", "Pares e impares", "Genera de 1 a 500 números aleatorios entre 0 y 999.");
        var txtCantidad = tabL2.Campo("Cantidad", "Cantidad:", "20");
        tabL2.Boton("Separar", "Generar y separar", () => { var r = Algoritmos.Clasificar(Validar.Entero(txtCantidad.Text, 1, 500)); tabL2.Resultado.Text = $"ORIGINAL\r\n{string.Join(", ", r.Original)}\r\n\r\nPARES\r\n{string.Join(", ", r.Pares)}\r\n\r\nIMPARES\r\n{string.Join(", ", r.Impares)}"; tabL2.Estado.Text = "Números clasificados."; });

        Grupo grupo = new();
        var tabL3 = Crear("Listas", "L3", "Aprobados y reprobados", "Calificaciones decimales de 0 a 10. Se aprueba desde 7.");
        var txtAlumno = tabL3.Campo("Alumno", "Alumno:"); var txtCalificacion = tabL3.Campo("Calificacion", "Calificación:");
        tabL3.Boton("Clasificar", "Agregar y clasificar", () => { grupo.Agregar(txtAlumno.Text, Validar.Decimal(txtCalificacion.Text, 0, 10)); tabL3.Resultado.Text = "APROBADOS\r\n" + string.Join("\r\n", grupo.Aprobados.Select(a => $"{a.Nombre}: {a.Calificacion}")) + "\r\n\r\nREPROBADOS\r\n" + string.Join("\r\n", grupo.Reprobados.Select(a => $"{a.Nombre}: {a.Calificacion}")); tabL3.Estado.Text = "Alumno registrado."; });

        Compra compra = new();
        var tabL4 = Crear("Listas", "L4", "Eliminar y ordenar productos", "Claves únicas; productos ordenados por nombre y total decimal exacto.");
        var txtClaveCompra = tabL4.Campo("ClaveCompra", "Clave:"); var txtProducto = tabL4.Campo("Producto", "Producto:"); var txtPrecio = tabL4.Campo("Precio", "Precio:");
        void ActualizarCompra() { tabL4.Mostrar(compra.Ordenados()); tabL4.Resultado.Text = $"TOTAL DE COMPRA: ${compra.Total():F2}"; }
        tabL4.Boton("Agregar", "Agregar", () => { decimal p = Validar.Decimal(txtPrecio.Text, 0, decimal.MaxValue); if (compra.Total() > decimal.MaxValue - p) throw new ArgumentException("El total excede el rango permitido."); compra.Agregar(txtClaveCompra.Text, txtProducto.Text, p); ActualizarCompra(); tabL4.Estado.Text = "Producto agregado."; });
        tabL4.Boton("Eliminar", "Eliminar por clave", () => { compra.Eliminar(txtClaveCompra.Text); ActualizarCompra(); tabL4.Estado.Text = "Producto eliminado."; });

        List<string> palabras = [];
        var tabL5 = Crear("Listas", "L5", "Palabras por letra", "Cada inicial genera su propia lista. Introduce una palabra a la vez.");
        var txtPalabraLista = tabL5.Campo("PalabraLista", "Palabra:");
        tabL5.Boton("AgregarPalabra", "Agregar palabra", () => { string p = Validar.Texto(txtPalabraLista.Text); Algoritmos.Agrupar([p]); palabras.Add(p); tabL5.Resultado.Text = "ORIGINAL: " + string.Join(", ", palabras) + "\r\n\r\n" + string.Join("\r\n", Algoritmos.Agrupar(palabras).Select(g => $"{g.Key}: {string.Join(", ", g.Value)}")); tabL5.Estado.Text = "Palabra clasificada."; });
    }
    private void CrearPilas()
    {
        var tabP1 = Crear("Pilas", "P1", "Invertir palabra", "Invierte mediante Stack<Rune>, conservando caracteres Unicode completos.");
        var txtPalabraInvertir = tabP1.Campo("PalabraInvertir", "Palabra:");
        tabP1.Boton("Invertir", "Invertir", () => { tabP1.Resultado.Text = Algoritmos.Invertir(txtPalabraInvertir.Text); tabP1.Estado.Text = "Orden invertido con una pila."; });

        var tabP2 = Crear("Pilas", "P2", "Palíndromo", "Ignora espacios, signos y mayúsculas. Conserva acentos.");
        var txtFrase = tabP2.Campo("Frase", "Palabra o frase:");
        tabP2.Boton("Comprobar", "Comprobar", () => { tabP2.Resultado.Text = Algoritmos.Palindromo(txtFrase.Text) ? "Sí es palíndromo." : "No es palíndromo."; tabP2.Estado.Text = "Comparación completada."; });

        var tabP3 = Crear("Pilas", "P3", "Suma de números grandes", "Enteros no negativos, sin límite fijo de dígitos. La solución usa pilas, sin BigInteger.");
        var txtPrimerNumero = tabP3.Campo("PrimerNumero", "Primer número:"); txtPrimerNumero.Width = 320;
        var txtSegundoNumero = tabP3.Campo("SegundoNumero", "Segundo número:"); txtSegundoNumero.Width = 320;
        tabP3.Boton("Sumar", "Sumar", () => { tabP3.Resultado.Text = Algoritmos.SumarGrandes(txtPrimerNumero.Text, txtSegundoNumero.Text); tabP3.Estado.Text = "Suma realizada mediante pilas y acarreo."; });

        var tabP4 = Crear("Pilas", "P4", "Reemplazar valor", "Valores separados por comas. Se apilan de izquierda a derecha; se muestra primero la cima.");
        var txtValores = tabP4.Campo("Valores", "Valores:", "1,2,3,2"); var txtViejo = tabP4.Campo("Viejo", "Viejo:", "2"); var txtNuevo = tabP4.Campo("Nuevo", "Nuevo:", "9");
        tabP4.Boton("Reemplazar", "Reemplazar", () => { Stack<int> pila = new(Validar.Texto(txtValores.Text).Split(',').Select(s => Validar.Entero(s))); int n = Algoritmos.Reemplazar(pila, Validar.Entero(txtNuevo.Text), Validar.Entero(txtViejo.Text)); tabP4.Resultado.Text = "CIMA → " + string.Join(", ", pila) + $"\r\nReemplazos: {n}"; tabP4.Estado.Text = "Se conservó el orden de la pila."; });
    }
    private static Color ColorDe(ColorAuto c) => c switch
    {
        ColorAuto.Rojo => Color.FromArgb(220, 38, 38),
        ColorAuto.Azul => Color.FromArgb(37, 99, 235),
        ColorAuto.Verde => Color.FromArgb(22, 163, 74),
        ColorAuto.Amarillo => Color.FromArgb(250, 204, 21),
        _ => Color.FromArgb(249, 115, 22),
    };
    private static Color TextoSobre(ColorAuto c) => c is ColorAuto.Amarillo or ColorAuto.Naranja ? Color.Black : Color.White;
    private static void DibujarCoche(Graphics g, int x, int y, Color carroceria, string etiqueta, Color fondoEtiqueta, Color textoEtiqueta, Font fuente)
    {
        using Pen contorno = new(Color.FromArgb(60, 60, 60), 2);
        using SolidBrush pintura = new(carroceria), fondo = new(fondoEtiqueta), texto = new(textoEtiqueta);
        Point[] cabina = [new(x + 28, y + 30), new(x + 42, y + 8), new(x + 92, y + 8), new(x + 110, y + 30)];
        g.FillPolygon(pintura, cabina); g.DrawPolygon(contorno, cabina);
        Rectangle chasis = new(x + 5, y + 30, 125, 32);
        g.FillRectangle(pintura, chasis); g.DrawRectangle(contorno, chasis);
        g.FillPolygon(Brushes.LightSkyBlue, [new(x + 36, y + 28), new(x + 46, y + 13), new(x + 65, y + 13), new(x + 65, y + 28)]);
        g.FillPolygon(Brushes.LightSkyBlue, [new(x + 70, y + 28), new(x + 70, y + 13), new(x + 89, y + 13), new(x + 103, y + 28)]);
        foreach (int r in new[] { x + 18, x + 90 }) { g.FillEllipse(Brushes.Black, r, y + 50, 26, 26); g.FillEllipse(Brushes.Silver, r + 8, y + 58, 10, 10); }
        Rectangle marco = new(x + 10, y + 86, 115, 26);
        g.FillRectangle(fondo, marco); g.DrawRectangle(Pens.Black, marco);
        using StringFormat centro = new() { Alignment = StringAlignment.Center, LineAlignment = StringAlignment.Center };
        g.DrawString(etiqueta, fuente, texto, marco, centro);
    }
    private void CrearColas()
    {
        Banco banco = new(5);
        var tabC1 = Crear("Colas", "C1", "Ventanilla de banco", "Cola FIFO con capacidad 5. Valida sobreflujo y cola vacía.");
        var txtCapacidad = tabC1.Campo("Capacidad", "Capacidad:", "5");
        var txtTurno = tabC1.Campo("Turno", "No. Turno:"); txtTurno.ReadOnly = true; txtTurno.Width = 60;
        void RefrescarBanco() { tabC1.Mostrar(banco.Clientes.Lista()); txtTurno.Text = banco.SiguienteTurno.ToString(); tabC1.Resultado.Text = banco.Clientes.ColaVacia() ? "Frente: -1 | Final: -1" : $"Frente: {banco.Clientes.Frente().Turno} | Final: {banco.Clientes.Final().Turno}"; }
        tabC1.Boton("Configurar", "Configurar", () => { if (!banco.Clientes.ColaVacia()) throw new ArgumentException("Configura la capacidad con la cola vacía."); banco = new Banco(Validar.Entero(txtCapacidad.Text, 1, 1000)); RefrescarBanco(); tabC1.Estado.Text = "Capacidad configurada."; });
        var txtCliente = tabC1.Campo("Cliente", "Cliente:");
        tabC1.Etiqueta("Movimiento", "Movimiento:");
        ComboBox cboMovimiento = new() { Name = "cboMovimiento", DropDownStyle = ComboBoxStyle.DropDownList, Width = 190 };
        cboMovimiento.Items.AddRange(["Pago de servicio", "Depósito", "Retiro", "Compra de tiempo-aire", "Consulta de saldo"]); cboMovimiento.SelectedIndex = 0; tabC1.Campos.Controls.Add(cboMovimiento);
        tabC1.Boton("AgregarCola", "Agregar a la cola", () =>
        {
            var c = banco.Llegar(txtCliente.Text, cboMovimiento.Text, DateTime.Now); RefrescarBanco();
            tabC1.Estado.Text = $"Cliente {c.Nombre} formado al final. Turno {c.Turno}, llegada {c.Llegada:HH:mm:ss}.";
            Mensaje("SE AGREGA UN CLIENTE AL FINAL DE LA COLA", $"Cliente formado en la Cola:\r\n\r\nNo Turno: {c.Turno}\r\nNombre: {c.Nombre}\r\nTipo de Movimiento: {c.Movimiento}\r\nHora de llegada: {c.Llegada:dd/MM/yyyy hh:mm:ss tt}");
        });
        tabC1.Boton("Atender", "Atender en ventanilla", () =>
        {
            var at = banco.Atender(DateTime.Now); RefrescarBanco();
            tabC1.Estado.Text = $"Atendido: {at.Cliente.Nombre}. Tiempo de espera: {at.Segundos} segundos.";
            Mensaje("TIEMPO DE ESPERA EN LA COLA", $"Cliente atendido: {at.Cliente.Nombre}\r\n\r\nTiempo de espera en la cola: {at.Segundos} segundos");
        });
        tabC1.Boton("SalidaSistema", "Salida del sistema", Close);
        RefrescarBanco();

        var tabC2 = Crear("Colas", "C2", "Juego de pintar coches", "Pinta el primer coche con el color de su etiqueta. El juego termina al acumular cinco coches.");
        tabC2.Controls.Add(pnlCoches); tabC2.Controls.SetChildIndex(pnlCoches, 1);
        pnlCoches.Paint += (_, e) =>
        {
            e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
            if (juego.Atendido is { } atendido) DibujarCoche(e.Graphics, 15, 12, ColorDe(atendido.Color), "Atendido", Color.White, Color.Black, Font);
            int x = 175;
            foreach (var c in juego.Coches.Lista()) { DibujarCoche(e.Graphics, x, 12, Color.WhiteSmoke, $"#{c.Numero} {c.Color}", ColorDe(c.Color), TextoSobre(c.Color), Font); x += 160; }
        };
        try { string[] r = File.ReadAllLines(archivoRecord); juego.Record = Validar.Entero(r[0], 0); juego.TiempoRecord = long.Parse(r[1]); }
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException or ArgumentException or FormatException or IndexOutOfRangeException or OverflowException) { juego.Record = 0; juego.TiempoRecord = 0; }
        void GuardarRecord() { if (Automatico) return; Directory.CreateDirectory(Path.GetDirectoryName(archivoRecord)!); File.WriteAllLines(archivoRecord, [juego.Record.ToString(), juego.TiempoRecord.ToString()]); }
        void RefrescarJuego()
        {
            string siguiente = juego.Activo ? $"Siguiente coche en {Math.Max(0, (juego.ProximaLlegada - Ahora + 999) / 1000)} s. Pinta el primer coche de la cola." : "Inicia una nueva partida.";
            tabC2.Resultado.Text = $"Pintados: {juego.Pintados} | En cola: {juego.Coches.Count}/5\r\nTiempo total: {juego.Transcurrido(Ahora)} s | Intervalo: {juego.Intervalo / 1000} s\r\nRécord: {juego.Record} coches en {juego.TiempoRecord} s\r\n{siguiente}";
            pnlCoches.Invalidate();
        }
        tabC2.Boton("Iniciar", "Iniciar partida", () => { juego.Iniciar(Ahora); tmrJuego.Start(); RefrescarJuego(); tabC2.Estado.Text = "Partida iniciada."; });
        tabC2.Etiqueta("Paleta", "Paleta de colores:");
        foreach (ColorAuto color in Enum.GetValues<ColorAuto>())
        {
            ColorAuto c = color;
            var btnPintar = tabC2.Boton("Pintar" + c, c.ToString(), () => { juego.Pintar(c, Ahora); GuardarRecord(); RefrescarJuego(); tabC2.Estado.Text = "Coche pintado correctamente."; });
            btnPintar.BackColor = ColorDe(c); btnPintar.ForeColor = TextoSobre(c); btnPintar.MinimumSize = new Size(90, 0);
        }
        tmrJuego.Tick += (_, _) => tabC2.Ejecutar(() => { bool activo = juego.Activo; juego.Actualizar(Ahora); if (activo && !juego.Activo) { tmrJuego.Stop(); GuardarRecord(); tabC2.Estado.Text = $"Fin del juego. {juego.Pintados} coches pintados; {juego.Transcurrido(Ahora)} segundos."; } RefrescarJuego(); });
        RefrescarJuego();

        ColaCircularDoblementeLigada parking = new();
        var tabC3 = Crear("Colas", "C3", "Estacionamiento", "Cola circular doblemente ligada sin cupo fijo. Salida FIFO. Tarifa: $2.00 por segundo completo.");
        var txtPlacas = tabC3.Campo("Placas", "Placas:"); var txtPropietario = tabC3.Campo("Propietario", "Propietario:");
        tabC3.Boton("EntradaAuto", "1. Entrada de auto", () =>
        {
            var a = parking.Insertar(txtPlacas.Text, txtPropietario.Text, DateTime.Now); tabC3.Mostrar(parking.Lista());
            tabC3.Estado.Text = $"Entrada confirmada. Autos: {parking.Count}.";
            Mensaje("ENTRADA DE AUTO", $"Entrada confirmada:\r\n\r\nPlacas: {a.Placas}\r\nPropietario: {a.Propietario}\r\nHora de entrada: {a.Entrada:dd/MM/yyyy HH:mm:ss}");
        });
        tabC3.Boton("SalidaAuto", "2. Salida de autos", () =>
        {
            var r = parking.Salir(DateTime.Now); tabC3.Mostrar(parking.Lista());
            string recibo = $"Placas: {r.Auto.Placas}\r\nPropietario: {r.Auto.Propietario}\r\nEntrada: {r.Auto.Entrada:dd/MM/yyyy HH:mm:ss}\r\nSalida: {r.Salida:dd/MM/yyyy HH:mm:ss}\r\nTiempo: {r.Segundos} segundos\r\nTotal: ${r.Costo:F2}";
            tabC3.Resultado.Text = "RECIBO\r\n" + recibo; tabC3.Estado.Text = $"Salida registrada. Autos: {parking.Count}.";
            Mensaje("SALIDA DE AUTO", recibo);
        });
    }
    public void GuardarEvidencias()
    {
        Automatico = true;
        string carpeta = Path.Combine(Environment.CurrentDirectory, "evidencias-csharp"); Directory.CreateDirectory(carpeta);
        Show();
        foreach (Modulo m in tabEjercicios.TabPages)
        {
            tabEjercicios.SelectedTab = m; Application.DoEvents();
            void Escribir(string nombre, string valor) => m.Control<TextBox>("txt" + nombre).Text = valor;
            void Pulsar(string nombre) { m.Control<Button>("btn" + nombre).PerformClick(); Application.DoEvents(); }
            switch (m.Codigo)
            {
                case "L1": Pulsar("Escanear"); Pulsar("Escanear"); Escribir("ClaveRetiro", "P1"); Pulsar("Retirar"); break;
                case "L2": Escribir("Cantidad", "20"); Pulsar("Separar"); break;
                case "L3": Escribir("Alumno", "Ana"); Escribir("Calificacion", "8.5"); Pulsar("Clasificar"); Escribir("Alumno", "Luis"); Escribir("Calificacion", "6.5"); Pulsar("Clasificar"); break;
                case "L4": Escribir("ClaveCompra", "P1"); Escribir("Producto", "Arroz"); Escribir("Precio", "32.75"); Pulsar("Agregar"); Escribir("ClaveCompra", "P2"); Escribir("Producto", "Leche"); Escribir("Precio", "26.25"); Pulsar("Agregar"); break;
                case "L5": foreach (string p in new[] { "Fresa", "Fresca", "Oso", "Orilla", "Pez" }) { Escribir("PalabraLista", p); Pulsar("AgregarPalabra"); } break;
                case "P1": Escribir("PalabraInvertir", "UTM"); Pulsar("Invertir"); break;
                case "P2": Escribir("Frase", "Anita lava la tina"); Pulsar("Comprobar"); break;
                case "P3": Escribir("PrimerNumero", "999999999999999999999999999999"); Escribir("SegundoNumero", "1"); Pulsar("Sumar"); break;
                case "P4": Pulsar("Reemplazar"); break;
                case "C1": Escribir("Cliente", "Ana"); Pulsar("AgregarCola"); Escribir("Cliente", "Luis"); Pulsar("AgregarCola"); Pulsar("Atender"); break;
                case "C2":
                    // Simula 45 segundos de partida: tres coches en cola y el primero se pinta con su color.
                    Pulsar("Iniciar"); tmrJuego.Stop(); juego.Iniciar(Ahora - 45000); juego.Actualizar(Ahora);
                    Pulsar("Pintar" + juego.Coches.Frente().Color); break;
                case "C3": Escribir("Placas", "ABC-123"); Escribir("Propietario", "Ana"); Pulsar("EntradaAuto"); Escribir("Placas", "XYZ-987"); Escribir("Propietario", "Luis"); Pulsar("EntradaAuto"); Pulsar("SalidaAuto"); break;
            }
            if (m.Estado.ForeColor == Color.Firebrick) throw new InvalidOperationException($"{m.Text}: {m.Estado.Text}");
            using Bitmap imagen = new(Width, Height); DrawToBitmap(imagen, new Rectangle(0, 0, Width, Height));
            imagen.Save(Path.Combine(carpeta, m.Codigo + ".png"));
        }
        Hide();
    }
}
