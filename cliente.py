import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2

class Cliente():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("./cliente.glade")
        contWindow = builder.get_object("ventanaCliente")

        contWindow.show_all()

        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()


        """self.cursor.execute("create table clientes(dni text primary key,nombre text,apellidos text,nacimiento text,direccion text)")"""

        self.entryDni = builder.get_object("entryDni")
        self.entryNombre = builder.get_object("entryNombre")
        self.entryApellido = builder.get_object("entryApellido")
        self.entryNacimiento = builder.get_object("entryNacimiento")
        self.entryDireccion = builder.get_object("entryDireccion")

        self.comboBoxIdCliente = builder.get_object("comboBoxIdCliente")
        txtViewNombre =  builder.get_object("txtViewNombre")
        txtViewApellido =  builder.get_object("txtViewApellido")
        txtViewNacimiento = builder.get_object("txtViewNacimiento")
        txtViewDireccion =  builder.get_object("txtViewDireccion")

        comboBoxIdClienteBusca = builder.get_object("comboBoxIdClienteBusca")

        btnAñadir = builder.get_object("btnAñadir")
        btnBuscar = builder.get_object("btnBuscar")

        btnAñadir.connect("clicked", self.on_btnAñadir_cliked)

        cursorConsultaClientes = self.cursor.execute("select dni from clientes")
        listaClientes = list()

        for dni in cursorConsultaClientes:
            n = 0
            if dni[n] not in listaClientes:
                listaClientes.append(str(dni[n]))
                n = n + 1
        print(listaClientes)

        self.cursor.execute("select dni from clientes")
        n = 0
        for dni in self.cursor:
            self.comboBoxIdCliente.insert(n, "", str(dni[0]))
            n = n + 1

        self.comboBoxIdCliente.connect("changed", self.on_seleccion_changed)

    def on_btnAñadir_cliked(self, boton):

        self.cursor.execute(" insert into clientes values(?,?,?,?,?) ",
                            (self.entryDni.get_text(),
                             self.entryNombre.get_text(),
                             self.entryApellido.get_text(),
                             self.entryNacimiento.get_text(),
                             self.entryDireccion.get_text()

                             )
                            )

        self.bbdd.commit()
        self.entryDni.set_text(" ")
        self.entryNombre.set_text(" ")
        self.entryApellido.set_text(" ")
        self.entryNacimiento.set_text(" ")
        self.entryDireccion.set_text(" ")

    def on_seleccion_changed(self, boton):
        self.cursor.execute("select nombre,apellidos,nacimiento,direccion from clientes where dni ='" +
                            str(self.comoBoxIdCliente.get_active_text()) + "'")
        self.lista = Gtk.ListStore(str, str, str, str)

        datos = self.cursor.fetchone()
        print(datos)

        nombre = datos[0]
        self.txtViewTipo.set_text(datos[0])
        apellidos = datos[1]
        nacimiento = datos[2]
        direccion = datos[3]
        self.datos.append([nombre,apellidos,nacimiento,direccion])
        print(self.datos)
        self.vista.set_lista(self.lista)

if __name__ == "__main__":
    Cliente()
    Gtk.main()