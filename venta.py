import gi
import os
gi.require_version('Gtk', '3.0')
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, TableStyle, Table)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from gi.repository import Gtk
from sqlite3 import dbapi2

class Venta():
    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("./venta.glade")
        contWindow = builder.get_object("ventanaVenta")

        contWindow.show_all()

        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()

        """self.cursor.execute("create table facturas(numFactura text primary key ,codCliente text,codProducto text,cantidade integer)")"""

        self.entryNum = builder.get_object("entryNum")
        self.entryStock = builder.get_object("entryStock")
        self.entryCliente = builder.get_object("entryCliente")
        self.entryCantidad = builder.get_object("entryCantidad")
        self.comboBoxNumFactura = builder.get_object("comboBoxNumFactura")

        btnAñadir = builder.get_object("btnAñadir")
        btnVenta = builder.get_object("btnVenta")

        btnAñadir.connect("clicked", self.on_btnAñadir_clicked)
        btnVenta.connect("clicked", self.on_btnVenta_clicked)

        self.cursor.execute("select numFactura from facturas")
        n = 0
        for numFactura in self.cursor:
            self.comboBoxNumFactura.insert(n,"",str(numFactura[0]))
            n = n + 1


    def on_btnVenta_clicked(self, boton):


         self.numFactura = self.comboBoxNumFactura.get_active_text()

         self.creaFactura()


    def creaFactura(self):

        global cantidade,nombre,apellidos,direccion,descripcion,precio
        self.numFactura = self.numFactura
        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()

        detalleFactura = []
        facturas = []

        cursorConsultaDetalleFactura = self.cursor.execute(
            "select codCliente,codProducto,cantidade from facturas where numFactura = ?",(self.numFactura,))

        lconsultaDetalleFactura = []
        for elementoFactura in cursorConsultaDetalleFactura:
            codCliente=elementoFactura[0]
            codProducto=elementoFactura[1]
            cantidade =elementoFactura[2]
        lconsultaDetalleFactura.append([elementoFactura[0],elementoFactura[1],elementoFactura[2]])
        print(codCliente,codProducto,cantidade)

        cursorConsultaFactura = self.cursor.execute("select nombre,apellidos,direccion from clientes where dni = ?", (codCliente,))
        rexistroCliente = cursorConsultaFactura.fetchone()
        consultaFactura = []
        for rexistroCliente in cursorConsultaFactura:
            nombre=rexistroCliente[0]
            apellidos=rexistroCliente[1]
            direccion = rexistroCliente[2]
        consultaFactura.append([rexistroCliente[0],rexistroCliente[1],rexistroCliente[2]])
        print(rexistroCliente[0],rexistroCliente[1],rexistroCliente[2])

        detalleFactura.append(['Dni Cliente :', codCliente])
        detalleFactura.append(['Nombre :', rexistroCliente[0]])
        detalleFactura.append(['Apellidos :', rexistroCliente[1]])
        detalleFactura.append(['Direccion :', rexistroCliente[2]])
        detalleFactura.append(["Codigo producto :",codProducto, "Cantidade :",cantidade])


        """cursorConsultaProducto = self.cursor.execute("select descripcion,precio from productos where codproducto = ?",(codProducto,))
        elemento = cursorConsultaProducto.fetchone()
        consultaFacturaPrecio = []
        prezo = 0
        for elemento in cursorConsultaProducto:
            descripcion =elemento[0]
            precio= elemento[1]
            print(elementoFactura[1])
            prezo = elemento[1] * elementoFactura[2]
            print(elemento[1])
        detalleFactura.append(["Descripcion :",elemento[0],"Precio unitario:", elemento[1], prezo])
        consultaFacturaPrecio.append([elemento[0], elemento[1]])
        prezoTotal = 0
        prezoTotal = prezo"""
        print(detalleFactura)

        facturas.append(list(detalleFactura))
        detalleFactura.clear()

        self.cursor.close()
        self.bbdd.close()

        doc = SimpleDocTemplate("Facturas.pdf", pagesize=A4)
        guion = []

        for factura in facturas:
            taboa = Table(factura, colWidths=80, rowHeights=30)

            taboa.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, 2), colors.blue),

                ('TEXTCOLOR', (0, 4), (-1, -1), colors.green),

                ('BACKGROUND', (0, 4), (-1, -1), colors.lightcyan),

                ('ALIGN', (2, 5), (-1, -1), 'RIGHT'),

                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                ('BOX', (0, 0), (-1, 2), 1, colors.black),

                ('BOX', (0, 4), (-1, -2), 1, colors.black),

                ('INNERGRID', (0, 4), (-1, -2), 0.5, colors.grey),

            ]))
            guion.append(taboa)
            guion.append(Spacer(0, 20))
            guion.append(PageBreak())

        doc.build(guion)



    def on_btnAñadir_clicked(self, boton):

        self.cursor.execute(" insert into facturas values(?,?,?,?) ",
                            (int (self.entryNum.get_text()),
                             self.entryCliente.get_text(),
                             self.entryStock.get_text(),
                             self.entryCantidad.get_text(),


                             )
                            )

        self.bbdd.commit()

        self.entryNum.set_text(" ")
        self.entryStock.set_text(" ")
        self.entryCliente.set_text(" ")
        self.entryCantidad.set_text(" ")


if __name__ == "__main__":
    Venta()
    Gtk.main()