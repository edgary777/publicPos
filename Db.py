import sqlite3


class Db(object):
    """Database communication class."""

    def __init__(self):
        """Init."""
        self.database = "database.db"
        self.initializer()

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
        cat = self.getCategories()
        connection = sqlite3.connect(self.database)

        cursor = connection.cursor()

        query = "SELECT * FROM categorias WHERE categoria = {}".format(cat)
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
        """Si las tablas no existen este metodo las crea."""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS tickets(folio INTEGER PRIMARY KEY,
                    nombre TEXT, llevar INT, sexo INT, edad INT, notas TEXT,
                    factura INT, subtotal FLOAT, iva FLOAT, descuentoa INT,
                    descuentop INT, cupon TEXT, total FLOAT, fecha DATE
                    hora TIME, cancelado INT);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS pticket(folio INTEGER PRIMARY KEY,
         producto TEXT, precio FLOAT, cantidad INT);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS productos(ID INT PRIMARY KEY AUTOINCREMENT,
                    producto TEXT, precio FLOAT, categoria TEXT);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS cupones(codigo TEXT PRIMARY KEY,
                    tipo int, descuento float, usos int, caducidad date);"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS categorias(categoria TEXT,
                    color VARCHAR);"""
        cursor.execute(query)

        connection.commit()
        connection.close()


db = Db()

print(db.getCategories())