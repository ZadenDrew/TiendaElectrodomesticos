import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, TableStyle, Table)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from tablaCliente import TablaCliente
from sqlite3 import dbapi2

class Cliente():
    def __init__(self):
        """
        :rtype: object
        """

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
        btnInformeCliente = builder.get_object("btnInformeCliente")

        btnAñadir.connect("clicked", self.on_btnAñadir_clicked)
        btnBuscar.connect("clicked", self.on_btnBuscar_clicked)
        btnInformeCliente.connect("clicked", self.on_btnInformeCliente_clicked)

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

        self.cursor.execute("select descripcion,modelo,precio,unidades from productos where codproducto = ?",
                            (str(self.comboBoxIdCliente.get_active_text()),))

        self.lista = Gtk.ListStore(str, str, str, str)
        self.vista = Gtk.TreeView()

    def on_btnAñadir_clicked(self, boton):

        """
       Método que recoge valores introducidos en los entry para almacenarlos en la tabla clientes
       de nuestra base de datos sqlite
       :param boton: Parametro que recibe el metodo
       :return: None
       """

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

        """
        Método que selecciona de la tabla productos sus valores para almacenarlos en una Gtk.ListStore
        :param boton: Parametro que recibe el metodo
        :return: None
        """

        self.cursor.execute("select nombre,apellidos,nacimiento,direccion from clientes where dni = ?",(str(self.comboBoxIdCliente.get_active_text()),))

        self.lista = Gtk.ListStore(str, str, str, str)

        datos = self.cursor.fetchone()


        nombre = datos[0]
        apellidos = datos[1]
        nacimiento = datos[2]
        direccion = datos[3]
        self.lista.append([nombre,apellidos,nacimiento,direccion])
        print(datos)
        #self.vista.set_model(self.lista)

    def on_btnInformeCliente_clicked(self, boton):

        """
        Método que recoge valores de nuestra base de datos sqlite
        para realizar un informe Clientes.pdf
        :param boton: Parametro que recibe el metodo
        :return: None
        """

        global dni,nombre,apellidos,nacimiento,direccion
        dni = self.comboBoxIdCliente.get_active_text()
        print(dni)
        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()

        detalleCliente = []
        cursorConsultaCliente = self.cursor.execute("select nombre,apellidos,nacimiento,direccion from clientes where dni = ?",
                                                    (dni,))
        rexistroCliente = cursorConsultaCliente.fetchone()
        consultaCliente = []
        listaclientes = []
        for rexistroCliente in cursorConsultaCliente:
            nombre = rexistroCliente[0]
            apellidos = rexistroCliente[1]
            nacimiento = rexistroCliente[2]
            direccion = rexistroCliente[3]

        consultaCliente.append([rexistroCliente[0], rexistroCliente[1], rexistroCliente[2], rexistroCliente[3]])
        print(dni,rexistroCliente[0], rexistroCliente[1], rexistroCliente[2],rexistroCliente[3])



        detalleCliente.append(['Nombre :', rexistroCliente[0]])
        detalleCliente.append(['Apellidos :', rexistroCliente[1]])
        detalleCliente.append(['Nacemento :', rexistroCliente[2]])
        detalleCliente.append(['Direccion :', rexistroCliente[3]])

        listaclientes.append(list(detalleCliente))
        consultaCliente.clear()

        self.cursor.close()
        self.bbdd.close()

        doc = SimpleDocTemplate("Clientes.pdf", pagesize=A4)
        guion = []

        for clientes in listaclientes:
            taboa = Table(clientes, colWidths=80, rowHeights=30)

            taboa.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 3), colors.blue),

            ('TEXTCOLOR', (0, 4), (-1, -1), colors.green),

            ('BACKGROUND', (0, 4), (-1, -1), colors.lightcyan),

            ('ALIGN', (2, 5), (-1, -1), 'RIGHT'),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('BOX', (0, 0), (-1, 4), 2, colors.black),

            ('BOX', (0, 3), (-1, -4), 1, colors.black),

            ('INNERGRID', (0, 4), (-1, -2), 0.5, colors.grey),

        ]))
        guion.append(taboa)
        guion.append(Spacer(0, 20))
        guion.append(PageBreak())

        doc.build(guion)



    def on_btnBuscar_clicked(self, boton):
        """
        Método que llama al apartado de clientes
        :param boton: Parametro que recibe el metodo
        :return: None
        """

        TablaCliente()

if __name__ == "__main__":
    Cliente()
    Gtk.main()