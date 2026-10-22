import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.math.BigDecimal;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.List;
import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;

/** Interfaz Swing. Cada módulo conserva su estado al cambiar de opción. */
public class PracticaApp {
  static final Color AZUL = new Color(26, 52, 87),
      FONDO = new Color(242, 246, 251),
      VERDE = new Color(16, 112, 87);
  static final DateTimeFormatter FECHA =
      DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss").withZone(ZoneId.systemDefault());
  static boolean pruebas;
  static final List<Modulo> MODULOS = new ArrayList<>();

  static void configurar() {
    UIManager.put("Label.font", new Font("SansSerif", Font.PLAIN, 14));
    UIManager.put("Button.font", new Font("SansSerif", Font.BOLD, 13));
    UIManager.put("TextField.font", new Font("SansSerif", Font.PLAIN, 14));
    UIManager.put("ComboBox.font", new Font("SansSerif", Font.PLAIN, 14));
    UIManager.put("Table.font", new Font("SansSerif", Font.PLAIN, 13));
    UIManager.put("TableHeader.font", new Font("SansSerif", Font.BOLD, 13));
  }

  public static void main(String[] args) {
    SwingUtilities.invokeLater(
        () -> {
          configurar();
          String categoria = args.length == 0 ? "Todas" : args[0];
          JFrame frame = new JFrame("Unidad II | " + categoria + " | Estructuras de datos");
          frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
          frame.setContentPane(construir(categoria));
          frame.setSize(1180, 800);
          frame.setMinimumSize(new Dimension(1180, 800));
          frame.setLocationRelativeTo(null);
          frame.setVisible(true);
        });
  }

  public static JPanel construir(String categoria) {
    MODULOS.clear();
    JPanel raiz = new JPanel(new BorderLayout());
    raiz.setBackground(FONDO);
    JLabel titulo = new JLabel("  UNIDAD II   /   " + categoria.toUpperCase(Locale.ROOT));
    titulo.setFont(new Font("SansSerif", Font.BOLD, 23));
    titulo.setOpaque(true);
    titulo.setBackground(AZUL);
    titulo.setForeground(Color.WHITE);
    titulo.setPreferredSize(new Dimension(1100, 66));
    raiz.add(titulo, BorderLayout.NORTH);
    JPanel tarjetas = new JPanel(new CardLayout());
    DefaultListModel<String> opciones = new DefaultListModel<>();
    if (categoria.equals("Todas") || categoria.equals("Listas")) {
      agregar(opciones, tarjetas, new ProductosPanel());
      agregar(opciones, tarjetas, new ParesPanel());
      agregar(opciones, tarjetas, new AlumnosPanel());
      agregar(opciones, tarjetas, new CompraPanel());
      agregar(opciones, tarjetas, new PalabrasPanel());
    }
    if (categoria.equals("Todas") || categoria.equals("Pilas")) {
      agregar(opciones, tarjetas, new InvertirPanel());
      agregar(opciones, tarjetas, new PalindromoPanel());
      agregar(opciones, tarjetas, new SumaPanel());
      agregar(opciones, tarjetas, new ReemplazoPanel());
    }
    if (categoria.equals("Todas") || categoria.equals("Colas")) {
      agregar(opciones, tarjetas, new BancoPanel());
      agregar(opciones, tarjetas, new JuegoPanel());
      agregar(opciones, tarjetas, new ParkingPanel());
    }
    JList<String> menu = new JList<>(opciones);
    menu.setFont(new Font("SansSerif", Font.PLAIN, 14));
    menu.setFixedCellHeight(49);
    menu.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
    menu.setBackground(new Color(228, 236, 246));
    menu.setSelectionBackground(AZUL);
    menu.setSelectionForeground(Color.WHITE);
    menu.addListSelectionListener(
        e -> {
          if (!e.getValueIsAdjusting() && menu.getSelectedValue() != null)
            ((CardLayout) tarjetas.getLayout()).show(tarjetas, menu.getSelectedValue());
        });
    JPanel lateral = new JPanel(new BorderLayout());
    lateral.setPreferredSize(new Dimension(270, 600));
    lateral.add(new JScrollPane(menu));
    JButton salir = new JButton("Salir");
    salir.addActionListener(
        e -> {
          for (Modulo m : MODULOS) if (m instanceof JuegoPanel j) j.timer.stop();
          Window w = SwingUtilities.getWindowAncestor(raiz);
          if (w != null) w.dispose();
        });
    lateral.add(salir, BorderLayout.SOUTH);
    raiz.add(lateral, BorderLayout.WEST);
    raiz.add(tarjetas);
    if (!opciones.isEmpty()) menu.setSelectedIndex(0);
    return raiz;
  }

  static void agregar(DefaultListModel<String> opciones, JPanel tarjetas, Modulo m) {
    String nombre = (opciones.size() + 1) + ". " + m.nombre;
    opciones.addElement(nombre);
    tarjetas.add(m, nombre);
    MODULOS.add(m);
  }

  abstract static class Modulo extends JPanel {
    final String nombre, clave;
    final JPanel campos = new JPanel(), centro = new JPanel(new BorderLayout(10, 10));
    final JLabel estado = new JLabel("Listo. Introduce los datos y elige una acción.");

    Modulo(String clave, String nombre, String ayuda) {
      super(new BorderLayout(10, 14));
      this.nombre = nombre;
      this.clave = clave;
      setBackground(FONDO);
      setBorder(BorderFactory.createEmptyBorder(22, 22, 18, 22));
      JPanel cabecera = new JPanel(new BorderLayout(0, 12));
      cabecera.setOpaque(false);
      JLabel t = new JLabel(nombre);
      t.setFont(new Font("SansSerif", Font.BOLD, 25));
      t.setForeground(AZUL);
      JLabel subtitulo = new JLabel("<html>" + ayuda + "</html>");
      subtitulo.setForeground(new Color(70, 83, 100));
      JPanel encabezado = new JPanel(new BorderLayout(0, 8));
      encabezado.setOpaque(false);
      encabezado.add(t, BorderLayout.NORTH);
      encabezado.add(subtitulo);
      cabecera.add(encabezado, BorderLayout.NORTH);
      campos.setLayout(new BoxLayout(campos, BoxLayout.Y_AXIS));
      campos.setOpaque(false);
      cabecera.add(campos);
      add(cabecera, BorderLayout.NORTH);
      centro.setOpaque(false);
      add(centro);
      estado.setOpaque(true);
      estado.setBackground(new Color(221, 235, 247));
      estado.setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
      estado.setPreferredSize(new Dimension(700, 76));
      add(estado, BorderLayout.SOUTH);
    }

    JPanel fila() {
      JPanel p = new JPanel(new FlowLayout(FlowLayout.LEFT, 9, 6));
      p.setOpaque(false);
      campos.add(p);
      return p;
    }

    JTextField campo(JPanel p, String etiqueta, int ancho) {
      p.add(new JLabel(etiqueta));
      JTextField f = new JTextField(ancho);
      p.add(f);
      return f;
    }

    JButton boton(JPanel p, String etiqueta, Runnable tarea) {
      JButton b = new JButton(etiqueta);
      b.setBackground(AZUL);
      b.setForeground(Color.WHITE);
      b.setFocusPainted(false);
      p.add(b);
      b.addActionListener(
          e -> {
            try {
              tarea.run();
            } catch (IllegalArgumentException | IllegalStateException ex) {
              mensaje(ex.getMessage(), true);
            }
          });
      return b;
    }

    void mensaje(String s, boolean error) {
      estado.setForeground(error ? new Color(157, 31, 42) : VERDE);
      estado.setText("<html>" + escapar(s) + "</html>");
    }

    void aviso(String s) {
      mensaje(s, false);
      if (!pruebas) JOptionPane.showMessageDialog(this, s, nombre, JOptionPane.INFORMATION_MESSAGE);
    }

    JTextArea salida() {
      JTextArea a = new JTextArea();
      a.setEditable(false);
      a.setFont(new Font("Monospaced", Font.PLAIN, 15));
      a.setLineWrap(true);
      a.setWrapStyleWord(true);
      a.setMargin(new Insets(18, 18, 18, 18));
      centro.add(new JScrollPane(a));
      return a;
    }

    JTable tabla(String... columnas) {
      JTable t =
          new JTable(
              new DefaultTableModel(columnas, 0) {
                public boolean isCellEditable(int r, int c) {
                  return false;
                }
              });
      t.setRowHeight(31);
      t.setFillsViewportHeight(true);
      t.getTableHeader().setReorderingAllowed(false);
      JScrollPane scroll = new JScrollPane(t);
      scroll.setColumnHeaderView(t.getTableHeader());
      centro.add(scroll);
      return t;
    }

    void filas(JTable t, List<Object[]> filas) {
      DefaultTableModel m = (DefaultTableModel) t.getModel();
      m.setRowCount(0);
      for (Object[] f : filas) m.addRow(f);
    }

    abstract void demostrar();
  }

  static String escapar(String s) {
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>");
  }

  static BigDecimal precio(String s) {
    return Estructuras.decimal(s, BigDecimal.ZERO, new BigDecimal("999999999.99"))
        .setScale(2, java.math.RoundingMode.HALF_UP);
  }

  static class ProductosPanel extends Modulo {
    final Estructuras.Almacen modelo = new Estructuras.Almacen();
    final JTable tabla;
    final JTextField clave;
    final JLabel conteo = new JLabel();
    final JButton escanear, retirar;

    ProductosPanel() {
      super(
          "L1",
          "Productos disponibles y retirados",
          "Lista de objetos Producto. El escáner genera cantidad y precio aleatorios; retirar mueve"
              + " el producto a otra lista.");
      JPanel p = fila();
      escanear =
          boton(
              p,
              "Escanear producto",
              () -> {
                Estructuras.Producto x = modelo.escanear();
                actualizar();
                mensaje("Registrado " + x.nombre() + ".", false);
              });
      p = fila();
      clave = campo(p, "Clave:", 7);
      retirar =
          boton(
              p,
              "Retirar producto",
              () -> {
                modelo.retirar(clave.getText());
                actualizar();
                mensaje("Producto retirado y conservado en el historial.", false);
              });
      fila().add(conteo);
      tabla = tabla("Estado", "Clave", "Nombre", "Cantidad", "Precio unitario");
      actualizar();
    }

    void actualizar() {
      List<Object[]> f = new ArrayList<>();
      for (Estructuras.Producto p : modelo.disponibles)
        f.add(
            new Object[] {
              "Disponible", p.clave(), p.nombre(), p.cantidad(), Estructuras.dinero(p.precio())
            });
      for (Estructuras.Producto p : modelo.retirados)
        f.add(
            new Object[] {
              "Retirado", p.clave(), p.nombre(), p.cantidad(), Estructuras.dinero(p.precio())
            });
      filas(tabla, f);
      conteo.setText(
          "Productos disponibles: "
              + modelo.disponibles.size()
              + "  |  Retirados: "
              + modelo.retirados.size());
    }

    void demostrar() {
      for (int i = 0; i < 4; i++) escanear.doClick();
      clave.setText("P2");
      retirar.doClick();
    }
  }

  static class ParesPanel extends Modulo {
    final JTextField cantidad;
    JTextArea resultado;
    final JButton generar;

    ParesPanel() {
      super(
          "L2",
          "Pares e impares",
          "Genera entre 1 y 500 enteros aleatorios de 0 a 999 y los distribuye en dos listas.");
      JPanel p = fila();
      cantidad = campo(p, "Cantidad:", 8);
      generar =
          boton(
              p,
              "Generar y clasificar",
              () -> {
                int n = Estructuras.entero(cantidad.getText(), 1, 500);
                var listas = Estructuras.generarNumeros(n, new Random());
                resultado.setText(
                    "LISTA ORIGINAL ("
                        + n
                        + ")\n"
                        + listas.original()
                        + "\n\nPARES ("
                        + listas.pares().size()
                        + ")\n"
                        + listas.pares()
                        + "\n\nIMPARES ("
                        + listas.impares().size()
                        + ")\n"
                        + listas.impares());
                mensaje(
                    "Clasificación completa. Cada número pertenece a una de las dos listas.",
                    false);
              });
      resultado = salida();
    }

    void demostrar() {
      cantidad.setText("15");
      generar.doClick();
    }
  }

  static class AlumnosPanel extends Modulo {
    final Estructuras.Grupo grupo = new Estructuras.Grupo();
    final JTextField nombre, nota;
    final JTable tabla;
    final JButton agregar;

    AlumnosPanel() {
      super(
          "L3",
          "Aprobados y reprobados",
          "Las calificaciones van de 0 a 10. Los alumnos con menos de 7 se extraen de aprobados y"
              + " se trasladan a reprobados.");
      JPanel p = fila();
      nombre = campo(p, "Alumno:", 18);
      nota = campo(p, "Nota:", 6);
      agregar =
          boton(
              fila(),
              "Registrar alumno",
              () -> {
                grupo.agregar(
                    nombre.getText(),
                    Estructuras.decimal(nota.getText(), BigDecimal.ZERO, BigDecimal.TEN));
                actualizar();
                mensaje(
                    "Alumno registrado. Aprobados: "
                        + grupo.aprobados.size()
                        + " | Reprobados: "
                        + grupo.reprobados.size(),
                    false);
              });
      tabla = tabla("Lista", "Alumno", "Calificación");
    }

    void actualizar() {
      List<Object[]> f = new ArrayList<>();
      for (var a : grupo.aprobados) f.add(new Object[] {"Aprobados", a.nombre(), a.calificacion()});
      for (var a : grupo.reprobados)
        f.add(new Object[] {"Reprobados", a.nombre(), a.calificacion()});
      filas(tabla, f);
    }

    void demostrar() {
      String[][] datos = {{"Ana López", "9.5"}, {"Luis Pérez", "6.9"}, {"María Díaz", "7"}};
      for (String[] d : datos) {
        nombre.setText(d[0]);
        nota.setText(d[1]);
        agregar.doClick();
      }
    }
  }

  static class CompraPanel extends Modulo {
    final Estructuras.Compra compra = new Estructuras.Compra();
    final JTextField clave, nombre, precio, eliminarClave;
    final JTable tabla;
    final JLabel total = new JLabel();
    final JButton agregar, eliminar;

    CompraPanel() {
      super(
          "L4",
          "Eliminar y ordenar productos",
          "Cada clave debe ser única. La tabla se ordena por nombre y el total se recalcula después"
              + " de agregar o eliminar.");
      JPanel p = fila();
      clave = campo(p, "Clave:", 6);
      nombre = campo(p, "Producto:", 13);
      precio = campo(p, "Precio:", 7);
      agregar =
          boton(
              fila(),
              "Agregar producto",
              () -> {
                compra.agregar(clave.getText(), nombre.getText(), precio(precio.getText()));
                actualizar();
                mensaje("Producto agregado; lista ordenada por nombre.", false);
              });
      p = fila();
      eliminarClave = campo(p, "Clave a eliminar:", 8);
      eliminar =
          boton(
              p,
              "Eliminar por clave",
              () -> {
                compra.eliminar(eliminarClave.getText());
                actualizar();
                mensaje("Producto eliminado; total actualizado.", false);
              });
      fila().add(total);
      tabla = tabla("Clave", "Nombre (A-Z)", "Precio");
      actualizar();
    }

    void actualizar() {
      List<Object[]> f = new ArrayList<>();
      for (var x : compra.ordenados())
        f.add(new Object[] {x.clave(), x.nombre(), Estructuras.dinero(x.precio())});
      filas(tabla, f);
      total.setText("Costo total de compra: " + Estructuras.dinero(compra.total()));
    }

    void demostrar() {
      String[][] d = {
        {"P1", "Zanahoria", "15.50"},
        {"P2", "Arroz", "32.75"},
        {"P3", "Leche", "26.25"},
        {"P4", "Pan", "20"}
      };
      for (String[] x : d) {
        clave.setText(x[0]);
        nombre.setText(x[1]);
        precio.setText(x[2]);
        agregar.doClick();
      }
      eliminarClave.setText("P4");
      eliminar.doClick();
    }
  }

  static class PalabrasPanel extends Modulo {
    final List<String> palabras = new ArrayList<>();
    final JTextField palabra;
    JTextArea resultado;
    final JButton agregar;

    PalabrasPanel() {
      super(
          "L5",
          "Listar palabras por letra",
          "Agrega una palabra por vez. Cada inicial nueva crea automáticamente una lista; se"
              + " conserva la lista original.");
      JPanel p = fila();
      palabra = campo(p, "Palabra:", 21);
      agregar =
          boton(
              p,
              "Agregar y agrupar",
              () -> {
                String s = Estructuras.texto(palabra.getText());
                Estructuras.agrupar(List.of(s));
                palabras.add(s);
                StringBuilder r = new StringBuilder("LISTA ORIGINAL\n" + palabras + "\n\n");
                Estructuras.agrupar(palabras)
                    .forEach(
                        (k, v) ->
                            r.append("LETRA ").append(k).append(": ").append(v).append("\n\n"));
                resultado.setText(r.toString());
                mensaje("Listas por inicial: " + Estructuras.agrupar(palabras).size(), false);
              });
      resultado = salida();
    }

    void demostrar() {
      for (String s : List.of("Fresa", "Fresca", "Orilla", "Oso", "Peso", "Pez", "Árbol")) {
        palabra.setText(s);
        agregar.doClick();
      }
    }
  }

  static class InvertirPanel extends Modulo {
    final JTextField palabra;
    JTextArea resultado;
    final JButton invertir;

    InvertirPanel() {
      super(
          "P1",
          "Invertir palabra",
          "Se apilan los caracteres y se extraen en orden LIFO: último en entrar, primero en"
              + " salir.");
      JPanel p = fila();
      palabra = campo(p, "Palabra:", 24);
      invertir =
          boton(
              p,
              "Invertir",
              () -> {
                String s = Estructuras.texto(palabra.getText());
                resultado.setText(
                    "ENTRADA\n"
                        + s
                        + "\n\nEXTRACCIÓN DE LA PILA\n"
                        + Estructuras.invertir(s)
                        + "\n\nCada carácter se obtiene con pop().");
                mensaje("Inversión realizada mediante una pila.", false);
              });
      resultado = salida();
    }

    void demostrar() {
      palabra.setText("UTM");
      invertir.doClick();
    }
  }

  static class PalindromoPanel extends Modulo {
    final JTextField palabra;
    JTextArea resultado;
    final JButton comprobar;

    PalindromoPanel() {
      super(
          "P2",
          "Palíndromo",
          "Compara la entrada con su inversión mediante pila. Ignora mayúsculas, espacios y signos;"
              + " conserva los acentos.");
      JPanel p = fila();
      palabra = campo(p, "Texto o número:", 25);
      comprobar =
          boton(
              fila(),
              "Comprobar palíndromo",
              () -> {
                boolean si = Estructuras.palindromo(palabra.getText());
                resultado.setText(
                    "ENTRADA\n"
                        + palabra.getText()
                        + "\n\nRESULTADO\n"
                        + (si ? "SÍ es un palíndromo." : "NO es un palíndromo.")
                        + "\n\n"
                        + "Se compara la secuencia normalizada con los valores extraídos de la"
                        + " pila.");
                mensaje("Análisis terminado.", false);
              });
      resultado = salida();
    }

    void demostrar() {
      palabra.setText("Anita lava la tina");
      comprobar.doClick();
    }
  }

  static class SumaPanel extends Modulo {
    final JTextField a, b;
    JTextArea resultado;
    final JButton sumar;

    SumaPanel() {
      super(
          "P3",
          "Suma de números grandes",
          "Enteros no negativos de cualquier longitud práctica. Cada dígito se apila; la suma usa"
              + " acarreo, sin convertir los operandos a int o BigInteger.");
      a = campo(fila(), "Primer entero:", 39);
      b = campo(fila(), "Segundo entero:", 37);
      sumar =
          boton(
              fila(),
              "Sumar con pilas",
              () -> {
                String r = Estructuras.sumarGrandes(a.getText(), b.getText());
                resultado.setText(
                    "PRIMER NÚMERO\n"
                        + a.getText()
                        + "\n\nSEGUNDO NÚMERO\n"
                        + b.getText()
                        + "\n\nSUMA\n"
                        + r);
                mensaje("Resultado calculado dígito a dígito mediante tres pilas.", false);
              });
      resultado = salida();
    }

    void demostrar() {
      a.setText("999999999999999999999999999999");
      b.setText("1");
      sumar.doClick();
    }
  }

  static class ReemplazoPanel extends Modulo {
    final Deque<Integer> pila = new ArrayDeque<>();
    final JTextField valor, viejo, nuevo;
    JTextArea resultado;
    final JButton apilar, reemplazar;

    ReemplazoPanel() {
      super(
          "P4",
          "Reemplazar valor en pila",
          "Reemplazar(pila, nuevo, viejo) sustituye todas las apariciones de viejo por nuevo y"
              + " conserva el orden de los demás elementos.");
      JPanel p = fila();
      valor = campo(p, "Entero:", 9);
      apilar =
          boton(
              p,
              "Apilar",
              () -> {
                pila.push(
                    Estructuras.entero(valor.getText(), Integer.MIN_VALUE, Integer.MAX_VALUE));
                mostrar();
                mensaje("Elemento insertado en la cima.", false);
              });
      boton(
          p,
          "Desapilar",
          () -> {
            if (pila.isEmpty()) throw new IllegalArgumentException("La pila está vacía.");
            int x = pila.pop();
            mostrar();
            mensaje("Extraído: " + x, false);
          });
      p = fila();
      viejo = campo(p, "Viejo:", 8);
      nuevo = campo(p, "Nuevo:", 8);
      reemplazar =
          boton(
              p,
              "Reemplazar",
              () -> {
                int v = Estructuras.entero(viejo.getText(), Integer.MIN_VALUE, Integer.MAX_VALUE),
                    n = Estructuras.entero(nuevo.getText(), Integer.MIN_VALUE, Integer.MAX_VALUE);
                int cambios = Estructuras.Reemplazar(pila, n, v);
                mostrar();
                mensaje("Reemplazos realizados: " + cambios, false);
              });
      resultado = salida();
      mostrar();
    }

    void mostrar() {
      StringBuilder r = new StringBuilder("PILA: CIMA → BASE\n\n");
      if (pila.isEmpty()) r.append("(vacía)");
      else for (int x : pila) r.append("    [ ").append(x).append(" ]\n");
      resultado.setText(r.toString());
    }

    void demostrar() {
      for (int x : new int[] {1, 2, 3, 2}) {
        valor.setText("" + x);
        apilar.doClick();
      }
      viejo.setText("2");
      nuevo.setText("9");
      reemplazar.doClick();
    }
  }

  static class BancoPanel extends Modulo {
    Estructuras.Banco banco = new Estructuras.Banco(5);
    final JTextField nombre, capacidad;
    final JComboBox<String> movimiento;
    final JTable tabla;
    final JLabel extremos = new JLabel();
    final JButton agregar, atender, configurar;

    BancoPanel() {
      super(
          "C1",
          "Ventanilla de un banco",
          "Cola FIFO acotada. El turno y la hora de llegada se asignan automáticamente; se valida"
              + " cola llena y vacía.");
      JPanel p = fila();
      capacidad = campo(p, "Capacidad:", 5);
      capacidad.setText("5");
      configurar =
          boton(
              p,
              "Configurar (cola vacía)",
              () -> {
                if (!banco.cola.ColaVacia())
                  throw new IllegalArgumentException(
                      "Atiende todos los clientes antes de cambiar la capacidad.");
                banco = new Estructuras.Banco(Estructuras.entero(capacidad.getText(), 1, 1000));
                actualizar();
                mensaje("Capacidad configurada.", false);
              });
      p = fila();
      nombre = campo(p, "Cliente:", 23);
      movimiento =
          new JComboBox<>(
              new String[] {
                "Pago de servicio",
                "Depósito",
                "Retiro",
                "Compra de tiempo-aire",
                "Consulta de saldo"
              });
      p = fila();
      p.add(new JLabel("Movimiento:"));
      p.add(movimiento);
      p = fila();
      agregar =
          boton(
              p,
              "Agregar a la cola",
              () -> {
                var c =
                    banco.llegar(
                        nombre.getText(),
                        Objects.toString(movimiento.getSelectedItem()),
                        Instant.now());
                actualizar();
                aviso(
                    "Cliente formado al final de la cola. Turno "
                        + c.turno()
                        + ": "
                        + c.nombre()
                        + "\nMovimiento: "
                        + c.movimiento()
                        + "\nLlegada: "
                        + FECHA.format(c.llegada()));
              });
      atender =
          boton(
              p,
              "Atender en ventanilla",
              () -> {
                var a = banco.atender(Instant.now());
                actualizar();
                aviso(
                    "Cliente atendido: "
                        + a.cliente().nombre()
                        + "\nTurno: "
                        + a.cliente().turno()
                        + " | Tiempo de espera: "
                        + a.esperaSegundos()
                        + " segundos.");
              });
      fila().add(extremos);
      tabla = tabla("Turno", "Cliente", "Movimiento", "Hora de llegada");
      actualizar();
    }

    void actualizar() {
      List<Object[]> f = new ArrayList<>();
      for (var c : banco.cola.lista())
        f.add(new Object[] {c.turno(), c.nombre(), c.movimiento(), FECHA.format(c.llegada())});
      filas(tabla, f);
      extremos.setText(
          "Frente: "
              + (banco.cola.ColaVacia() ? "-1" : banco.cola.frente().turno())
              + "  |  Final: "
              + (banco.cola.ColaVacia() ? "-1" : banco.cola.fin().turno())
              + "  |  En espera: "
              + banco.cola.size());
    }

    void demostrar() {
      for (String n : List.of("Ana López", "Luis Pérez", "María Díaz")) {
        nombre.setText(n);
        agregar.doClick();
      }
      atender.doClick();
    }
  }

  static Color color(Estructuras.ColorAuto c) {
    return switch (c) {
      case ROJO -> new Color(205, 54, 67);
      case AZUL -> new Color(51, 120, 205);
      case VERDE -> new Color(33, 150, 99);
      case AMARILLO -> new Color(233, 177, 32);
      case MORADO -> new Color(138, 83, 186);
    };
  }

  static class JuegoPanel extends Modulo {
    final Estructuras.Juego juego = new Estructuras.Juego();
    final JLabel marcador = new JLabel(), reloj = new JLabel();
    final LienzoAutos lienzo = new LienzoAutos(juego);
    final JButton iniciar;
    final javax.swing.Timer timer;

    JuegoPanel() {
      super(
          "C2",
          "Juego: pintar coches",
          "Selecciona el color pedido por el primer coche. Llega uno cada 20 s; el intervalo baja 2"
              + " s por cada 3 aciertos (mínimo 2 s). Pierdes al acumular 5.");
      JPanel p = fila();
      iniciar =
          boton(
              p,
              "Iniciar / Reiniciar",
              () -> {
                juego.iniciar(System.currentTimeMillis());
                refrescar();
                mensaje("Partida iniciada. Atiende sólo el primer coche de la fila.", false);
              });
      p.add(marcador);
      fila().add(reloj);
      p = fila();
      for (var c : Estructuras.ColorAuto.values()) {
        JButton b =
            boton(
                p,
                c.name(),
                () -> {
                  juego.pintar(c, System.currentTimeMillis());
                  if (!pruebas) guardar();
                  refrescar();
                  mensaje("Coche pintado correctamente.", false);
                });
        b.setBackground(color(c));
        b.setForeground(c == Estructuras.ColorAuto.AMARILLO ? Color.BLACK : Color.WHITE);
      }
      centro.add(lienzo);
      timer =
          new javax.swing.Timer(
              100,
              e -> {
                boolean antes = juego.activo;
                juego.actualizar(System.currentTimeMillis());
                refrescar();
                if (antes && !juego.activo) {
                  guardar();
                  mensaje(
                      "Fin del juego: 5 coches en espera. Pintados: "
                          + juego.pintados
                          + " | Tiempo total: "
                          + juego.transcurrido(System.currentTimeMillis())
                          + " s.",
                      false);
                }
              });
      if (!pruebas) {
        cargar();
        timer.start();
      }
      refrescar();
    }

    java.nio.file.Path archivoRecord() {
      return java.nio.file.Path.of(
          System.getProperty("user.home"), ".practica-u2", "record.properties");
    }

    void cargar() {
      try {
        Properties p = new Properties();
        try (var in = java.nio.file.Files.newInputStream(archivoRecord())) {
          p.load(in);
        }
        juego.record = Integer.parseInt(p.getProperty("coches", "0"));
        juego.tiempoRecord = Long.parseLong(p.getProperty("segundos", "0"));
      } catch (Exception e) {
        /* Primera partida: no existe récord previo. */
      }
    }

    void guardar() {
      try {
        java.nio.file.Path path = archivoRecord();
        java.nio.file.Files.createDirectories(path.getParent());
        Properties p = new Properties();
        p.setProperty("coches", "" + juego.record);
        p.setProperty("segundos", "" + juego.tiempoRecord);
        try (var out = java.nio.file.Files.newOutputStream(path)) {
          p.store(out, "Record del juego de coches");
        }
      } catch (IOException e) {
        mensaje("Partida terminada. No se pudo guardar el récord en disco.", true);
      }
    }

    void refrescar() {
      long ahora = System.currentTimeMillis();
      marcador.setText("Pintados: " + juego.pintados + " | En fila: " + juego.cola.size() + "/5");
      reloj.setText(
          "Tiempo: "
              + juego.transcurrido(ahora)
              + " s | Intervalo: "
              + (juego.intervalo() / 1000)
              + " s | Próximo: "
              + (juego.activo ? Math.max(0, (juego.proximaLlegada - ahora + 999) / 1000) : 0)
              + " s | Récord: "
              + juego.record
              + " coches / "
              + juego.tiempoRecord
              + " s");
      lienzo.repaint();
    }

    void demostrar() {
      long ahora = System.currentTimeMillis();
      juego.iniciar(ahora - 40000);
      juego.actualizar(ahora);
      refrescar();
      mensaje("Demostración: 3 coches en cola; sólo el primero puede pintarse.", false);
    }
  }

  /** Ilustraciones originales vectoriales, pintadas por Swing sin recursos externos. */
  static class LienzoAutos extends JPanel {
    final Estructuras.Juego juego;

    LienzoAutos(Estructuras.Juego j) {
      juego = j;
      setBackground(Color.WHITE);
      setPreferredSize(new Dimension(790, 320));
    }

    protected void paintComponent(Graphics g) {
      super.paintComponent(g);
      Graphics2D d = (Graphics2D) g.create();
      d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
      int y = 125;
      d.setColor(new Color(225, 231, 239));
      d.fillRoundRect(12, y + 45, getWidth() - 24, 65, 18, 18);
      int i = 0;
      for (var c : juego.cola.lista()) {
        int x = 24 + i * 145;
        d.setColor(i == 0 ? new Color(211, 239, 226) : new Color(240, 243, 248));
        d.fillRoundRect(x - 4, 40, 139, 245, 18, 18);
        d.setColor(AZUL);
        d.setFont(new Font("SansSerif", Font.BOLD, 13));
        d.drawString(i == 0 ? "FRENTE / ATENDER" : "TURNO " + c.numero(), x + 5, 67);
        d.setColor(new Color(157, 170, 187));
        d.fillRoundRect(x + 2, y, 123, 40, 13, 13);
        d.fillRoundRect(x + 26, y - 26, 70, 43, 13, 13);
        d.setColor(new Color(207, 231, 250));
        d.fillRoundRect(x + 35, y - 20, 50, 20, 7, 7);
        d.setColor(new Color(44, 55, 70));
        d.fillOval(x + 17, y + 27, 26, 26);
        d.fillOval(x + 86, y + 27, 26, 26);
        d.setColor(color(c.color()));
        d.fillRoundRect(x + 8, y + 83, 111, 40, 12, 12);
        d.setColor(c.color() == Estructuras.ColorAuto.AMARILLO ? Color.BLACK : Color.WHITE);
        d.drawString(c.color().name(), x + 22, y + 108);
        i++;
      }
      if (i == 0) {
        d.setColor(AZUL);
        d.setFont(new Font("SansSerif", Font.BOLD, 20));
        d.drawString(
            juego.activo ? "Sin coches: espera la siguiente llegada." : "Pulsa Iniciar para jugar.",
            25,
            90);
      }
      d.dispose();
    }
  }

  static class ParkingPanel extends Modulo {
    final Estructuras.ColaCircularDoblementeLigada cola =
        new Estructuras.ColaCircularDoblementeLigada();
    final JTextField placas, propietario;
    final JTable tabla;
    final JLabel contador = new JLabel();
    final JButton entrada, salida;

    ParkingPanel() {
      super(
          "C3",
          "Estacionamiento para autos",
          "Cola circular doblemente ligada sin cupo fijo. Entrada por el final y salida por el"
              + " frente. Tarifa: $2.00 por segundo completo.");
      JPanel p = fila();
      placas = campo(p, "Placas:", 10);
      propietario = campo(p, "Propietario:", 20);
      p = fila();
      entrada =
          boton(
              p,
              "1. Entrada de auto",
              () -> {
                cola.insertar(placas.getText(), propietario.getText(), Instant.now());
                actualizar();
                aviso(
                    "Entrada confirmada: "
                        + placas.getText().trim().toUpperCase(Locale.ROOT)
                        + "\nHora registrada automáticamente.");
              });
      salida =
          boton(
              p,
              "2. Salida de auto",
              () -> {
                var r = cola.salir(Instant.now());
                actualizar();
                aviso(
                    "RECIBO | "
                        + r.auto().placas()
                        + " | "
                        + r.auto().propietario()
                        + "\nEntrada: "
                        + FECHA.format(r.auto().entrada())
                        + "\nSalida: "
                        + FECHA.format(r.salida())
                        + "\nTiempo: "
                        + r.segundos()
                        + " segundos | Total: "
                        + Estructuras.dinero(r.costo()));
              });
      fila().add(contador);
      tabla = tabla("Orden FIFO", "Placas", "Propietario", "Hora de entrada");
      actualizar();
    }

    void actualizar() {
      List<Object[]> f = new ArrayList<>();
      int n = 0;
      for (var a : cola.lista())
        f.add(new Object[] {++n, a.placas(), a.propietario(), FECHA.format(a.entrada())});
      filas(tabla, f);
      contador.setText(
          "Autos dentro: "
              + cola.size()
              + " | Frente: "
              + (cola.ColaVacia() ? "vacío" : cola.lista().get(0).placas())
              + " | Enlaces circulares: "
              + (cola.enlacesValidos() ? "correctos" : "ERROR"));
    }

    void demostrar() {
      Instant ahora = Instant.now();
      cola.insertar("ABC-123", "Ana López", ahora.minusSeconds(30));
      cola.insertar("XYZ-987", "Luis Pérez", ahora.minusSeconds(15));
      actualizar();
      salida.doClick();
      placas.setText("MEX-456");
      propietario.setText("María Díaz");
      entrada.doClick();
      mensaje(
          "Salida verificada de ABC-123 / Ana López: 30 segundos × $2.00 = $60.00. Los restantes"
              + " conservan el orden FIFO.",
          false);
    }
  }

  /** Evidencias reales: ejecuta controles y pinta los mismos paneles de la aplicación. */
  public static void generarEvidencias(File carpeta) throws Exception {
    pruebas = true;
    configurar();
    JPanel raiz = construir("Todas");
    carpeta.mkdirs();
    for (Modulo m : MODULOS) {
      m.demostrar();
      capturar(m, new File(carpeta, m.clave + "_resultado.png"));
    }
    raiz.setSize(1300, 860);
    layoutRecursivo(raiz);
    BufferedImage menu = new BufferedImage(1300, 860, BufferedImage.TYPE_INT_RGB);
    Graphics2D gm = menu.createGraphics();
    raiz.printAll(gm);
    gm.dispose();
    ImageIO.write(menu, "png", new File(carpeta, "menu_general.png"));
    SumaPanel suma = (SumaPanel) MODULOS.get(7);
    suma.a.setText("12x");
    suma.sumar.doClick();
    capturar(suma, new File(carpeta, "validacion_numeros.png"));
    BancoPanel banco = (BancoPanel) MODULOS.get(9);
    while (!banco.banco.cola.ColaVacia()) banco.atender.doClick();
    banco.atender.doClick();
    capturar(banco, new File(carpeta, "validacion_cola_vacia.png"));
    banco.capacidad.setText("1");
    banco.configurar.doClick();
    banco.nombre.setText("Cliente de prueba");
    banco.agregar.doClick();
    banco.agregar.doClick();
    capturar(banco, new File(carpeta, "validacion_cola_llena.png"));
    CompraPanel compra = (CompraPanel) MODULOS.get(3);
    compra.nombre.setText("");
    compra.clave.setText("P5");
    compra.agregar.doClick();
    capturar(compra, new File(carpeta, "validacion_faltantes.png"));
    AlumnosPanel alumnos = (AlumnosPanel) MODULOS.get(2);
    alumnos.nota.setText("11");
    alumnos.agregar.doClick();
    capturar(alumnos, new File(carpeta, "validacion_rango.png"));
    JuegoPanel juego = (JuegoPanel) MODULOS.get(10);
    long ahora = System.currentTimeMillis();
    juego.juego.iniciar(ahora - 80000);
    juego.juego.actualizar(ahora);
    juego.refrescar();
    juego.mensaje("Fin del juego: 5 coches en espera. Tiempo total: 80 segundos.", false);
    capturar(juego, new File(carpeta, "juego_fin.png"));
    juego.juego.iniciar(ahora - 40002);
    for (int i = 0; i < 3; i++) {
      if (juego.juego.cola.ColaVacia()) juego.juego.actualizar(juego.juego.proximaLlegada);
      long instante = ahora - 40001 + i * 20000L;
      juego.juego.pintar(juego.juego.cola.frente().color(), instante);
    }
    juego.refrescar();
    juego.mensaje("Tres coches pintados: el intervalo pasa de 20 a 18 segundos.", false);
    capturar(juego, new File(carpeta, "juego_aceleracion.png"));
  }

  static void layoutRecursivo(Container c) {
    c.doLayout();
    for (Component x : c.getComponents()) if (x instanceof Container k) layoutRecursivo(k);
  }

  static void capturar(Modulo m, File archivo) throws IOException {
    m.setSize(1060, 720);
    layoutRecursivo(m);
    BufferedImage imagen = new BufferedImage(1060, 720, BufferedImage.TYPE_INT_RGB);
    Graphics2D g = imagen.createGraphics();
    m.printAll(g);
    g.dispose();
    ImageIO.write(imagen, "png", archivo);
  }
}
