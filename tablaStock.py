import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class TablaStock(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title="TablaStock")

        boxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(boxV)

        self.lista = Gtk.ListStore(str,str, str, int, int)

        self.vista = Gtk.TreeView(model=self.lista)
        boxV.pack_start(self.vista, True, True, 0)

        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()

        self.cursor.execute("select codproducto,descripcion,modelo,precio,unidades from productos ")
        self.productos=[]
        for row in self.cursor:
            print(row[0],row[1],row[2],row[3],row[4])
            self.productos.append([row[0],row[1],row[2],row[3],row[4]])

        for row in self.productos:
            self.lista.append([row[0], row[1], row[2], row[3], row[4]])

        celdaText = Gtk.CellRendererText(xalign=1)
        columnaCodigo = Gtk.TreeViewColumn('codproducto', celdaText, text=0)
        self.vista.append_column(columnaCodigo)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaDescripcion = Gtk.TreeViewColumn('descripcion', celdaText2, text=1)
        self.vista.append_column(columnaDescripcion)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaModelo = Gtk.TreeViewColumn('modelo', celdaText3, text=2)
        self.vista.append_column(columnaModelo)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaPrecio = Gtk.TreeViewColumn('precio', celdaText4, text=3)
        self.vista.append_column(columnaPrecio)

        celdaText5 = Gtk.CellRendererText(xalign=1)
        columnaUnidades = Gtk.TreeViewColumn('unidades', celdaText5, text=4)
        self.vista.append_column(columnaUnidades)

        boxV.pack_start(self.vista, True, True, 0)

        self.show_all()


if __name__ == "__main__":
    TablaStock()
    Gtk.main()