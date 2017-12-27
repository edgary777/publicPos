import sqlite3


class Db(object):
    """Database communication class."""

    def __init__(self):
        """Init."""
        self.database = "database.db"
        # self.initializer()

    def sConn(self):
        """Start connection."""
        return sqlite3.connect(self.database)

    def eConn(self, connection):
        """End connection."""
        connection.commit()
        connection.close()

    def recordTicket(self, data):
        """Add order to database."""
        connection = sqlite3.connect(self.database)

        connection.commit()
        connection.close()

    def getFolio(self):
        """Return the next ticket number."""
        connection = sqlite3.connect(self.database)

        cursor = connection.cursor()

        query = """SELECT MAX(folio) FROM tickets"""
        cursor.execute(query)
        folio = cursor.fetchone()

        connection.commit()
        connection.close()

        return folio[0]

    def getProduct(self, product):
        """Return the product data."""
        connection = sqlite3.connect(self.database)

        cursor = connection.cursor()

        query = "SELECT * FROM tickets WHERE id = {}".format(product)
        cursor.execute(query)
        product = cursor.fetchone()

        connection.commit()
        connection.close()
        return product

    def getProducts(self, cat):
        """Return products list with metadata from the category passed."""
        connection = sqlite3.connect(self.database)

        cursor = connection.cursor()

        cat = "'" + cat + "'"  # formatting category for sql query

        query = "SELECT * FROM productos WHERE categoria = {}".format(cat)
        cursor.execute(query)
        products = cursor.fetchall()

        connection.commit()
        connection.close()

        return products

    def getCategories(self):
        """Return a list of categories and their color."""
        connection = sqlite3.connect(self.database)

        cursor = connection.cursor()

        query = """SELECT * FROM categorias"""
        cursor.execute(query)
        category = cursor.fetchall()

        connection.commit()
        connection.close()

        return category

    def initializer(self):
        """If table not exists create it."""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS tickets(folio INTEGER PRIMARY KEY,
                    nombre TEXT, llevar INT, sexo INT, edad INT, notas TEXT,
                    factura INT, subtotal FLOAT, iva FLOAT, descuentoa INT,
                    descuentop INT, cupon TEXT, total FLOAT, fecha DATE
                    hora TIME, cancelado INT);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ticketProducts(folio INTEGER PRIMARY KEY,
         producto TEXT, precio FLOAT, cantidad INT);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS productos(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT, precio FLOAT, categoria TEXT);"""
        cursor.execute(query)

        query = """INSERT INTO productos('producto', 'precio', 'categoria') VALUES('ADOBADA', '70', 'LONCHES');"""
        cursor.execute(query)

        query = """INSERT INTO productos('producto', 'precio', 'categoria') VALUES('PIERNA', '48', 'LONCHES');"""
        cursor.execute(query)

        query = """INSERT INTO productos('producto', 'precio', 'categoria') VALUES('COCA-COLA', '14', 'BEBIDAS');"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS cupones(codigo TEXT PRIMARY KEY,
                    tipo int, descuento float, usos int, caducidad date);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS categorias(categoria TEXT,
                    color VARCHAR);"""
        cursor.execute(query)

        query = """INSERT INTO categorias VALUES('LONCHES', '255, 0, 0');"""
        cursor.execute(query)
        query = """INSERT INTO categorias VALUES('BEBIDAS', '0, 255, 0');"""
        cursor.execute(query)

        connection.commit()
        connection.close()


# db = Db()
