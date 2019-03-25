import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2

class Stock():
    def __init__(self):
        """

        :rtype: object
        """
        builder = Gtk.Builder()
        builder.add_from_file("./stock.glade")
        contWindow = builder.get_object("ventanaStock")

        contWindow.show_all()

        self.bbdd = dbapi2.connect("TiendaElectrodomesticos.bd")
        self.cursor = self.bbdd.cursor()

        """
        self.cursor.execute("create table facturas(numFactura integer primary key AUTOINCREMENT,codCliente text,codProducto text,cantidade integer)")
        self.cursor.execute("create table productos(codproducto text primary key,descripcion text,modelo text,precio integer,unidades integer)") """


        boxStock = builder.get_object("boxStock")
        self.entryId = builder.get_object("entryId")
        self.entryTipo = builder.get_object("entryTipo")
        self.entryModelo = builder.get_object("entryModelo")
        self.entryPrecio = builder.get_object("entryPrecio")
        self.entryUnidades = builder.get_object("entryUnidades")

        self.comboBoxId = builder.get_object("comboBoxId")
        self.txtViewTipo =  builder.get_object("txtViewTipo")
        self.txtViewModelo =  builder.get_object("txtViewModelo")
        self.txtViewPrecio =  builder.get_object("txtViewPrecio")
        self.txtViewUnidades = builder.get_object("txtViewUnidades")

        self.comboBoxIdBusca = builder.get_object("comboBoxIdBusca")
        vista = builder.get_object("treeVista")

        btnAñadir = builder.get_object("btnAñadir")
        btnBuscar = builder.get_object("btnBuscar")

        btnAñadir.connect("clicked",self.on_btnAñadir_cliked)


        cursorConsultaProductos = self.cursor.execute("select codproducto from productos")
        listaProductos = list()

        for codproducto in cursorConsultaProductos:
            n=0
            if codproducto[n] not in listaProductos:
                listaProductos.append(str(codproducto[n]))
                n=n+1
        print(listaProductos)

        self.cursor.execute("select codproducto from productos")
        n=0
        for codproducto in self.cursor:
            self.comboBoxId.insert(n,"",str(codproducto[0]))
            n = n+1

        self.comboBoxId.connect("changed",self.on_seleccion_changed)




        celdaText = Gtk.CellRendererText()
        columnaDescripcion = Gtk.TreeViewColumn('Descripcion', celdaText, text=0)
        vista.append_column(columnaDescripcion)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaModelo = Gtk.TreeViewColumn('Modelo', celdaText2, text=1)
        vista.append_column(columnaModelo)

        celdaText3 = Gtk.CellRendererText()
        columnaPrecio = Gtk.TreeViewColumn('Precio', celdaText3, text=2)
        vista.append_column(columnaPrecio)

        celdaText4 = Gtk.CellRendererText()
        columnaUnidades = Gtk.TreeViewColumn('Unidades', celdaText4, text=3)
        vista.append_column(columnaUnidades)

        boxStock.pack_start(vista,True,True,0)

    def on_btnAñadir_cliked(self,boton):

        self.cursor.execute(" insert into productos values(?,?,?,?,?) ",
                            (self.entryId.get_text(),
                            self.entryTipo.get_text(),
                            self.entryModelo.get_text(),
                            self.entryPrecio.get_text(),
                            int(self.entryUnidades.get_text())

                                )
                                )



        self.bbdd.commit()
        self.entryId.set_text(" ")
        self.entryTipo.set_text(" ")
        self.entryModelo.set_text(" ")
        self.entryPrecio.set_text(" ")
        self.entryUnidades.set_text(" ")


    def on_seleccion_changed(self,boton):
        self.cursor.execute("select descripcion,modelo,precio,unidades from productos where codproducto ='" +
                            str(self.comoBoxId.get_active_text()) +"'")
        self.lista =Gtk.ListStore(str,str,int,int)

        datos = self.cursor.fetchone()
        print(datos)

        descripcion = datos[0]
        self.txtViewTipo.set_text(datos[0])
        modelo = datos[1]
        precio = datos[2]
        unidades = datos[3]
        self.datos.append([descripcion,modelo,precio,unidades])
        print(self.datos)
        self.vista.set_lista(self.lista)

if __name__ == "__main__":
    Stock()
    Gtk.main()