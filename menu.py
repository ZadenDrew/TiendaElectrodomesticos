import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from stock import Stock
from cliente import Cliente
from venta import Venta

class Menu():
    def __init__(self):
        """
        :rtype: object
        """

        builder = Gtk.Builder()
        builder.add_from_file("./menu.glade")
        contAplWindow = builder.get_object("aplicacion")


        contAplWindow.show_all()
        btnstock=builder.get_object("btnstock")
        btncliente = builder.get_object("btncliente")
        btnventa = builder.get_object("btnventa")

        btnstock.connect("clicked", self.on_btnstock_clicked)
        btncliente.connect("clicked", self.on_btncliente_clicked)
        btnventa.connect("clicked", self.on_btnventa_clicked)

    def on_btnstock_clicked(self, boton):
        """
        Método que llama al apartado de clientes
        :param boton: Parametro que recibe el metodo
        :return: None
        """


        Stock()


    def on_btncliente_clicked(self, boton):
        """
        Método que llama al apartado de clientes
        :param boton: Parametro que recibe el metodo
        :return: None
        """


        Cliente()

    def on_btnventa_clicked(self, boton):
        """
        Método que llama al apartado de clientes
        :param boton: Parametro que recibe el metodo
        :return: None
        """

        Venta()


if __name__ == "__main__":
    Menu()
    Gtk.main()