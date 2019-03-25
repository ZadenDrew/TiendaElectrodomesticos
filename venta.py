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

        """self.cursor.execute("create table facturas(numFactura integer primary key AUTOINCREMENT,codCliente text,codProducto text,cantidade integer)")"""

        self.entryNum = builder.get_object("entryNum")
        self.entryStock = builder.get_object("entryStock")
        self.entryCliente = builder.get_object("entryCliente")
        self.entryCantidad = builder.get_object("entryCantidad")

        btnAñadir = builder.get_object("btnAñadir")
        btnVenta = builder.get_object("btnVenta")

        btnAñadir.connect("clicked", self.on_btnAñadir_cliked)
        btnVenta.connect("clicked", self.on_btnVenta_cliked)

    def on_btnVenta_cliked(self, boton):
        detalleFactura = []
        facturas = []

        cursorConsultaFacturas = self.cursor.execute("select numFactura from facturas")
        listaFacturas = list()

        for numFactura in cursorConsultaFacturas:
            if numFactura[0] not in listaFacturas:
                listaFacturas.append(numFactura[0])

        print(listaFacturas)

        for numFactura in listaFacturas:
            codigoCliente = None
            consultaFactura = None
            cursorConsultaFactura = self.cursor.execute("select codCliente from facturas where numFactura = ?", (int(numFactura),))
            codigoCliente = cursorConsultaFactura.fetchone()[0]

            detalleFactura.append(['Cod Cliente: ', codigoCliente, '', 'Num Factura: ', numFactura])

            cursorConsultaFactura = self.cursor.execute("select nombre,direccion from clientes where dni = ?", (codigoCliente,))
            rexistroCliente = cursorConsultaFactura.fetchone()

            detalleFactura.append(['Nome', rexistroCliente[0], '', '', ''])
            detalleFactura.append(['Direccion', rexistroCliente[1], '', '', ''])

            cursorConsultaDetalleFactura = self.cursor.execute("select codProducto,cantidade from facturas where numFactura = ?",
                                                  (numFactura,))
            lconsultaDetalleFactura = []
            for elementoFactura in cursorConsultaDetalleFactura:
                lconsultaDetalleFactura.append([elementoFactura[0], elementoFactura[1]])
            detalleFactura.append(["","","","",""])
            detalleFactura.append(["Codigo producto", "Descripcion", "Cantidade", "Prezo unitario", "prezo"])
            prezoTotal = 0
            for elemento in lconsultaDetalleFactura:
                cursorConsultaProducto = self.cursor.execute("select descripcion,precio from productos where codProducto = ?",
                                                (elemento[0]))
                rexistroProducto = cursorConsultaProducto.fetchone()
                prezo = elemento[1] * rexistroProducto[1]
                detalleFactura.append(
                    [elemento[0], rexistroProducto[0], elemento[1], rexistroProducto[1], prezo])

                prezoTotal = prezoTotal + prezo
    #print(detalleFactura)

            detalleFactura.append(["","","","Prezo total:",prezoTotal])
            facturas.append(list(detalleFactura))
            detalleFactura.clear()

            self.cursor.close()
            self.bbdd.close()

            doc = SimpleDocTemplate("exemploFacturas.pdf", pagesize=A4)
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



    def on_btnAñadir_cliked(self, boton):

        self.cursor.execute(" insert into facturas values(?,?,?,?) ",
                            (int (self.entryNum.get_text()),
                             self.entryStock.get_text(),
                             self.entryCliente.get_text(),
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