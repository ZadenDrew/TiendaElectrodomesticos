import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class TablaCliente(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title="TablaStock")

        boxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(boxV)

        self.lista = Gtk.ListStore(str,str, str, str, str)

        self.vista = Gtk.TreeView(model=self.lista)
        boxV.pack_start(self.vista, True, True, 0)

        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()

        self.cursor.execute("select dni,nombre,apellidos,nacimiento,direccion from clientes ")
        self.personas=[]
        for row in self.cursor:
            print(row[0],row[1],row[2],row[3],row[4])
            self.personas.append([row[0],row[1],row[2],row[3],row[4]])

        for row in self.personas:
            self.lista.append([row[0], row[1], row[2], row[3], row[4]])

        celdaText = Gtk.CellRendererText(xalign=1)
        columnaDni = Gtk.TreeViewColumn('dni', celdaText, text=0)
        self.vista.append_column(columnaDni)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaNombre = Gtk.TreeViewColumn('nombre', celdaText2, text=1)
        self.vista.append_column(columnaNombre)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaApellidos = Gtk.TreeViewColumn('apellidos', celdaText3, text=2)
        self.vista.append_column(columnaApellidos)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaNacimiento = Gtk.TreeViewColumn('nacimiento', celdaText4, text=3)
        self.vista.append_column(columnaNacimiento)

        celdaText5 = Gtk.CellRendererText(xalign=1)
        columnaDireccion = Gtk.TreeViewColumn('direccion', celdaText5, text=4)
        self.vista.append_column(columnaDireccion)

        boxV.pack_start(self.vista, True, True, 0)

        self.show_all()


if __name__ == "__main__":
    TablaCliente()
    Gtk.main()