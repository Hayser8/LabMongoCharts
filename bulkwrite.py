from pymongo import MongoClient, InsertOne
from pymongo.errors import BulkWriteError
import csv
import json
from datetime import datetime

# ================================
# 1. Conexión a MongoDB Atlas
# ================================
uri = "mongodb+srv://garciasalasperezjulio:1234@lab1.ka8t9.mongodb.net/?retryWrites=true&w=majority&appName=Lab1"
client = MongoClient(uri)
# Usamos el nombre de base de datos, por ejemplo "lab1"
db = client["Resaurante"]

# ================================
# Función Genérica para Bulk Insert desde CSV
# ================================
def bulk_insert_from_csv(filename, transform_func, collection):
    operations = []
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = transform_func(row)
                operations.append(InsertOne(doc))
    except Exception as e:
        print(f"Error leyendo el archivo {filename}: {e}")
        return

    if operations:
        try:
            result = collection.bulk_write(operations)
            print(f"Inserted {result.inserted_count} documents into '{collection.name}' collection from {filename}.")
        except BulkWriteError as bwe:
            print("Bulk write error:", bwe.details)
    else:
        print(f"No operations to execute for {filename}")

# ================================
# 2. Funciones de Transformación para Cada Colección
# ================================

# (a) Restaurantes:
def transform_restaurante(row):
    # Se espera que el CSV tenga: id, nombre, direccion, lat, lng, telefono, email, horario (este último en formato JSON)
    return {
        "nombre": row["nombre"],
        "direccion": row["direccion"],
        "ubicacion": {
            "lat": float(row["lat"]),
            "lng": float(row["lng"])
        },
        "telefono": row["telefono"],
        "email": row["email"],
        "horario": json.loads(row["horario"])
    }

# (b) Usuarios:
def transform_usuario(row):
    # Se espera: id, nombre, apellido, email, telefono, direccion, nit, fechaRegistro, password, rol
    return {
        "nombre": row["nombre"],
        "apellido": row["apellido"],
        "email": row["email"],
        "telefono": row["telefono"],
        "direccion": row["direccion"],
        "nit": row["nit"],
        "fechaRegistro": datetime.strptime(row["fechaRegistro"], "%Y-%m-%d"),
        "password": row["password"],
        "rol": row["rol"]
    }

# (c) Artículos del Menú:
def transform_articulo(row):
    # Se espera: id, nombre, descripcion, precio, categoria, imagen
    return {
        "nombre": row["nombre"],
        "descripcion": row["descripcion"],
        "precio": float(row["precio"]),
        "categoria": row["categoria"],
        "imagen": row["imagen"]
    }

# (d) Órdenes:
def transform_orden(row):
    # Se espera: id, usuarioId, restauranteId, fecha, estado, total, articulos (cadena JSON)
    return {
        "usuarioId": row["usuarioId"],
        "restauranteId": row["restauranteId"],
        "fecha": datetime.strptime(row["fecha"], "%Y-%m-%d %H:%M:%S"),
        "estado": row["estado"],
        "total": float(row["total"]),
        "articulos": json.loads(row["articulos"])
    }

# (e) Reseñas:
def transform_resena(row):
    # Se espera: id, usuarioId, restauranteId, ordenId, calificacion, comentario, fecha
    # Si ordenId es cadena vacía, se omite.
    doc = {
        "usuarioId": row["usuarioId"],
        "restauranteId": row["restauranteId"],
        "calificacion": int(row["calificacion"]),
        "comentario": row["comentario"],
        "fecha": datetime.strptime(row["fecha"], "%Y-%m-%d")
    }
    if row["ordenId"].strip():
        doc["ordenId"] = row["ordenId"]
    return doc

# ================================
# 3. Colecciones de MongoDB
# ================================
restaurantes_collection = db["restaurantes"]
usuarios_collection      = db["usuarios"]
articulos_collection     = db["articulos_menu"]
ordenes_collection       = db["ordenes"]
resenas_collection       = db["resenas"]

# ================================
# 4. Bulk Writes desde los CSVs
# ================================
bulk_insert_from_csv("restaurantes.csv", transform_restaurante, restaurantes_collection)
bulk_insert_from_csv("usuarios.csv", transform_usuario, usuarios_collection)
bulk_insert_from_csv("articulos_menu.csv", transform_articulo, articulos_collection)
bulk_insert_from_csv("ordenes.csv", transform_orden, ordenes_collection)
bulk_insert_from_csv("resenas.csv", transform_resena, resenas_collection)
