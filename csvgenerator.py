import csv
import json
import random
from datetime import datetime, timedelta

# ================================
# Función para escribir CSV
# ================================
def write_csv(filename, fieldnames, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for registro in data:
            writer.writerow(registro)
    print(f"Archivo '{filename}' creado exitosamente con {len(data)} registros.")

# ================================
# 1. Generar datos para "restaurantes"
# ================================
num_restaurantes = 10
restaurantes = []
# Horario fijo para todos (se almacena como JSON en el CSV)
horario_template = [
    {"dia": "Lunes", "apertura": "09:00", "cierre": "18:00"},
    {"dia": "Martes", "apertura": "09:00", "cierre": "18:00"},
    {"dia": "Miércoles", "apertura": "09:00", "cierre": "18:00"},
    {"dia": "Jueves", "apertura": "09:00", "cierre": "18:00"},
    {"dia": "Viernes", "apertura": "09:00", "cierre": "18:00"}
]
for i in range(1, num_restaurantes+1):
    restaurante = {
        "id": f"r{i}",
        "nombre": f"Restaurante {i}",
        "direccion": f"Calle {i}, No. {i*10}, Ciudad XYZ",
        # Simulación de coordenadas: incrementan levemente para cada uno.
        "lat": round(10.0 + i * 0.1, 6),
        "lng": round(-74.0 - i * 0.1, 6),
        "telefono": f"555-10{i:03d}",
        "email": f"contacto{i}@restaurante.com",
        # Convertir la lista de horario a cadena JSON.
        "horario": json.dumps(horario_template, ensure_ascii=False)
    }
    restaurantes.append(restaurante)

# ================================
# 2. Generar datos para "usuarios"
# ================================
num_usuarios = 20
usuarios = []
for i in range(1, num_usuarios+1):
    # Para la fecha de registro, sumamos días al 1 de enero de 2023.
    fecha_registro = (datetime(2023, 1, 1) + timedelta(days=i)).strftime("%Y-%m-%d")
    usuario = {
        "id": f"u{i}",
        "nombre": f"Nombre{i}",
        "apellido": f"Apellido{i}",
        "email": f"usuario{i}@mail.com",
        "telefono": f"555-200{i:03d}",
        "direccion": f"Avenida {i} # {i*3}",
        "nit": f"NIT{i:03d}",
        "fechaRegistro": fecha_registro,
        "password": f"pass{i}",
        # El primer usuario se marca como admin, el resto como user.
        "rol": "admin" if i == 1 else "user"
    }
    usuarios.append(usuario)

# ================================
# 3. Generar datos para "articulos_menu"
# ================================
num_articulos = 10
categorias = ["Entrada", "Plato Principal", "Postre", "Bebida"]
articulos_menu = []
for i in range(1, num_articulos+1):
    articulo = {
        "id": f"m{i}",
        "nombre": f"Platillo {i}",
        "descripcion": f"Delicioso platillo {i} con ingredientes frescos.",
        # Precio aleatorio entre 5 y 50, redondeado a dos decimales.
        "precio": round(random.uniform(5, 50), 2),
        "categoria": random.choice(categorias),
        "imagen": f"http://example.com/platillo{i}.jpg"
    }
    articulos_menu.append(articulo)

# ================================
# 4. Generar datos para "ordenes"
# ================================
num_ordenes = 30
estados = ["pendiente", "completado", "cancelado"]
ordenes = []
for i in range(1, num_ordenes+1):
    # Seleccionar un usuario y un restaurante al azar
    usuario_id = random.choice(usuarios)["id"]
    restaurante_id = random.choice(restaurantes)["id"]
    # Fecha y hora de la orden: fecha aleatoria en febrero de 2023
    fecha_orden = datetime(2023, 2, random.randint(1, 28), random.randint(10, 20), random.randint(0, 59))
    fecha_str = fecha_orden.strftime("%Y-%m-%d %H:%M:%S")
    estado = random.choice(estados)
    
    # Generar de 1 a 3 artículos para la orden
    num_items = random.randint(1,3)
    articulos = []
    total = 0.0
    for _ in range(num_items):
        articulo_elegido = random.choice(articulos_menu)
        cantidad = random.randint(1, 5)
        precio = articulo_elegido["precio"]
        total += cantidad * precio
        articulos.append({
            "menuItemId": articulo_elegido["id"],
            "nombre": articulo_elegido["nombre"],
            "cantidad": cantidad,
            "precio": precio
        })
    orden = {
        "id": f"o{i}",
        "usuarioId": usuario_id,
        "restauranteId": restaurante_id,
        "fecha": fecha_str,
        "estado": estado,
        "total": round(total, 2),
        # Convertir lista de artículos a cadena JSON
        "articulos": json.dumps(articulos, ensure_ascii=False)
    }
    ordenes.append(orden)

# ================================
# 5. Generar datos para "resenas"
# ================================
num_resenas = 30
comentarios = [
    "Excelente servicio y comida deliciosa.",
    "Muy bueno, pero el tiempo de espera fue largo.",
    "Regular, se puede mejorar la atención.",
    "Deficiente, no volvería.",
    "No recomendado, mala experiencia."
]
resenas = []
for i in range(1, num_resenas+1):
    usuario_id = random.choice(usuarios)["id"]
    restaurante_id = random.choice(restaurantes)["id"]
    # Con 50% de probabilidad se asigna un id de orden, de lo contrario se deja vacío
    orden_id = random.choice(ordenes)["id"] if random.random() < 0.5 else ""
    calificacion = random.randint(1, 5)
    comentario = random.choice(comentarios)
    # Fecha aleatoria en marzo de 2023
    fecha_resena = datetime(2023, 3, random.randint(1, 28)).strftime("%Y-%m-%d")
    resena = {
        "id": f"res{i}",
        "usuarioId": usuario_id,
        "restauranteId": restaurante_id,
        "ordenId": orden_id,
        "calificacion": calificacion,
        "comentario": comentario,
        "fecha": fecha_resena
    }
    resenas.append(resena)

# ================================
# Escribir los archivos CSV
# ================================
# 1. CSV para restaurantes
fieldnames_restaurantes = ["id", "nombre", "direccion", "lat", "lng", "telefono", "email", "horario"]
write_csv("restaurantes.csv", fieldnames_restaurantes, restaurantes)

# 2. CSV para usuarios
fieldnames_usuarios = ["id", "nombre", "apellido", "email", "telefono", "direccion", "nit", "fechaRegistro", "password", "rol"]
write_csv("usuarios.csv", fieldnames_usuarios, usuarios)

# 3. CSV para articulos_menu
fieldnames_articulos = ["id", "nombre", "descripcion", "precio", "categoria", "imagen"]
write_csv("articulos_menu.csv", fieldnames_articulos, articulos_menu)

# 4. CSV para ordenes
fieldnames_ordenes = ["id", "usuarioId", "restauranteId", "fecha", "estado", "total", "articulos"]
write_csv("ordenes.csv", fieldnames_ordenes, ordenes)

# 5. CSV para resenas
fieldnames_resenas = ["id", "usuarioId", "restauranteId", "ordenId", "calificacion", "comentario", "fecha"]
write_csv("resenas.csv", fieldnames_resenas, resenas)
