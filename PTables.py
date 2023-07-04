from faker import Faker
from datetime import datetime, date
import mysql.connector

fake = Faker(locale='es_ES')

# Connection setting
config = {
    'user': 'root',
    'password': 'proyectoccm',
    'host': '192.168.100.163',
    'port': 33060,
    'database': 'FarmaciasCCM',
}


def create_product(num_product, cursor):
    for i in range(1, num_product + 1):
        product_name = fake.random_element(elements=("Loratadina", "Claritin", "Alavert", "Wal-itin",
                                                     "Hidroxicloroquina", "Plaquenil", "Quineprox", "Dolquine",
                                                     "Ibuprofeno", "Advil", "Motrin", "Nuprin", "Naproxeno",
                                                     "Aleve", "Naprosyn", "Anaprox", "Aspirina", "Bayer", "Ecotrin",
                                                     "Bufferin", "Simvastatina", "Zocor", "Simcor", "Lipex",
                                                     "Atorvastatina", "Lipitor", "Torvast", "Sortis", "Lisinopril",
                                                     "Prinivil", "Zestril", "Metformina", "Glucophage", "Fortamet",
                                                     "Riomet", "Omeprazol", "Prilosec", "Losec", "Zegerid",
                                                     "Pantoprazol", "Protonix", "Pantoloc", "Panto IV",
                                                     "Ranitidina", "Zantac", "Tritec", "Pepcid", "Citalopram",
                                                     "Celexa", "Seropram", "Cipramil", "Escitalopram",
                                                     "Lexapro", "Cipralex"))
        product_description = fake.random_element(elements=("Analgésico y antifebril",
                                                             "Medicamento para aliviar alergias",
                                                             "Antidepresivo para trastornos del estado de ánimo",
                                                             "Antiinflamatorio para dolores articulares",
                                                             "Antihistamínico para síntomas de alergia",
                                                             "Antiácido para acidez estomacal e indigestión",
                                                             "Antibiótico para infecciones bacterianas",
                                                             "Antipsicótico para trastornos de salud mental",
                                                             "Broncodilatador para afecciones respiratorias",
                                                             "Anticoagulante para prevenir coágulos sanguíneos",
                                                             "Estatina para reducir el colesterol",
                                                             "Diurético para controlar la retención de líquidos",
                                                             "Antiviral para infecciones virales",
                                                             "Antifúngico para infecciones por hongos",
                                                             "Anticoagulante para prevenir coágulos",
                                                             "Antihipertensivo para reducir la presión arterial",
                                                             "Medicamento antidiabético para el control de la diabetes",
                                                             "Ansiolítico para trastornos de ansiedad",
                                                             "Antiemético para prevenir náuseas y vómitos",
                                                             "Suplemento vitamínico y mineral",
                                                             "Antiinflamatorio para tratar el dolor",
                                                             "Antipirético para reducir la fiebre"))

        query = "INSERT INTO Producto (ID_Producto, Nombre, Descripcion, Precio) VALUES (%s, %s, %s, %s)"
        values = (i, product_name, product_description, fake.random_int(min=10, max=100))
        cursor.execute(query, values)


def create_sale(num_sales, cursor):
    start_date = date(2021, 1, 1)
    end_date = date(2023, 12, 31)

    # Get existing store_ids from the Sucursal table
    cursor.execute("SELECT ID_Sucursal FROM Sucursal")
    store_ids = [row[0] for row in cursor.fetchall()]

    for i in range(1, num_sales + 1):
        store_id = fake.random_element(elements=store_ids)
        employee_id = fake.random_int(min=1, max=100)
        date_quantity = fake.date_between(start_date=start_date, end_date=end_date)
        total = fake.random_int(min=10, max=100)

        query = "INSERT INTO Venta (ID_Venta, ID_Sucursal, ID_Empleado, Fecha, Total) VALUES (%s, %s, %s, %s, %s)"
        values = (i, store_id, employee_id, date_quantity, total)
        cursor.execute(query, values)


def create_store(num_store, cursor):
    for i in range(1, num_store + 1):
        store_name = fake.random_element(elements=("Farmacia San Martín", "Farmacia Esperanza",
                                                   "Farmacia del Sol", "Farmacia Santa Cruz",
                                                   "Farmacia Nueva Vida", "Farmacia San Rafael",
                                                   "Farmacia El Faro", "Farmacia Santa Clara",
                                                   "Farmacia La Paz", "Farmacia San José"))
        store_address = fake.street_address()
        store_city = fake.city()
        store_phone = fake.phone_number()

        query = "INSERT INTO Sucursal (ID_Sucursal, Nombre, Direccion, Ciudad, Telefono) VALUES (%s, %s, %s, %s, %s)"
        values = (i, store_name, store_address, store_city, store_phone)
        cursor.execute(query, values)


def create_inv(num_inv, cursor):
    for i in range(1, num_inv + 1):
        store_id = fake.random_int(min=1, max=4)
        product_id = fake.random_int(min=1, max=100)
        inv_quant = fake.random_int(min=1, max=100)

        query = "INSERT INTO Inventario (ID_Inventario, ID_Sucursal, ID_Producto, Cantidad) VALUES (%s, %s, %s, %s)"
        values = (i, store_id, product_id, inv_quant)
        cursor.execute(query, values)


def create_employee(num_employee, cursor):
    for i in range(1, num_employee + 1):
        employee_name = fake.first_name()
        employee_surname = fake.last_name()
        employee_address = fake.address()
        employee_city = fake.city()
        store_id = fake.random_int(min=1, max=4)

        query = "INSERT INTO Empleado (ID_Empleado, Nombre, Apellido, Direccion, Telefono, ID_Sucursal) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (i, employee_name, employee_surname, employee_address, employee_city, store_id)
        cursor.execute(query, values)


def import_data_to_mysql():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Create and import stores
    create_store(num_store=10, cursor=cursor)

    # Create and import products
    create_product(num_product=100, cursor=cursor)

    # Create and import employees
    create_employee(num_employee=100, cursor=cursor)

    # Create and import inventory
    create_inv(num_inv=100, cursor=cursor)

    # Create and import sales
    create_sale(num_sales=100, cursor=cursor)

    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    import_data_to_mysql()
