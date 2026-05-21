import pandas as pd
import numpy as np
import random
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def generar_datos():
    print("Iniciando la generación de archivos del proyecto...")

    # 1. metas_anuales.xlsx (KPIs por región)
    datos_metas = {
        "Region": ["Norte", "Sur", "Centro", "Occidente", "Oriente"],
        "Meta_Ventas_Anual": [5000000, 3500000, 8000000, 4500000, 2000000],
        "Crecimiento_Esperado_Pct": [12.5, 8.0, 15.0, 10.5, 5.0],
        "Presupuesto_Marketing": [200000, 150000, 400000, 180000, 90000]
    }
    df_metas = pd.DataFrame(datos_metas)
    df_metas.to_excel("metas_anuales.xlsx", index=False)
    print("- metas_anuales.xlsx generado.")

    # 2. catalogos.xml (Definiciones de categorías)
    root = ET.Element("Catalogos")
    categorias = [
        {"id": "C01", "nombre": "Electrónica", "descripcion": "Gadgets y dispositivos"},
        {"id": "C02", "nombre": "Ropa", "descripcion": "Prendas de vestir para todas las edades"},
        {"id": "C03", "nombre": "Hogar", "descripcion": "Muebles y decoración"},
        {"id": "C04", "nombre": "Deportes", "descripcion": "Artículos y equipo deportivo"}
    ]
    for cat in categorias:
        categoria_element = ET.SubElement(root, "Categoria")
        for key, val in cat.items():
            child = ET.SubElement(categoria_element, key)
            child.text = val
    tree = ET.ElementTree(root)
    tree.write("catalogos.xml", encoding="utf-8", xml_declaration=True)
    print("- catalogos.xml generado.")

    # 3. logs_servidor.txt (2,500 líneas de actividad web)
    with open("logs_servidor.txt", "w") as f:
        endpoints = ["/home", "/productos", "/carrito", "/checkout", "/login"]
        estados = [200, 200, 200, 301, 404, 500] 
        fecha_base = datetime.now()
        for i in range(2500):
            ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            fecha = (fecha_base - timedelta(minutes=random.randint(1, 10000))).strftime("%d/%b/%Y:%H:%M:%S")
            endpoint = random.choice(endpoints)
            estado = random.choice(estados)
            tiempo_ms = random.randint(20, 1500)
            log = f'{ip} - - [{fecha}] "GET {endpoint} HTTP/1.1" {estado} {tiempo_ms}\n'
            f.write(log)
    print("- logs_servidor.txt generado.")

    # 4. perfiles_usuarios.json (1,500 perfiles)
    perfiles = []
    preferencias_lista = ["Electrónica", "Ropa", "Hogar", "Deportes"]
    for i in range(1, 1501):
        perfil = {
            "Customer_ID": f"CUST_{i:04d}",
            "edad": random.randint(18, 70),
            "preferencias": random.sample(preferencias_lista, k=random.randint(1, 3)),
            "geolocalizacion": {
                "latitud": round(random.uniform(14.0, 32.0), 4),
                "longitud": round(random.uniform(-118.0, -86.0), 4)
            }
        }
        perfiles.append(perfil)
    with open("perfiles_usuarios.json", "w", encoding="utf-8") as f:
        json.dump(perfiles, f, indent=4, ensure_ascii=False)
    print("- perfiles_usuarios.json generado.")

    # 5. ventas_historicas.sql (5,500 registros)
    with open("ventas_historicas.sql", "w") as f:
        f.write("CREATE TABLE IF NOT EXISTS ventas (id_transaccion VARCHAR(20), id_cliente VARCHAR(20), monto DECIMAL(10,2), fecha VARCHAR(50), id_tienda VARCHAR(10));\n")
        f.write("INSERT INTO ventas (id_transaccion, id_cliente, monto, fecha, id_tienda) VALUES\n")
        valores = []
        fecha_base_venta = datetime(2023, 1, 1)
        formatos_fecha = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%y"] # Fechas inconsistentes intencionales
        for i in range(1, 5501):
            id_trans = f"TRX_{i}"
            id_cliente = f"CUST_{random.randint(1, 1500):04d}"
            monto = round(random.uniform(50.0, 5000.0), 2)
            fecha_venta = (fecha_base_venta + timedelta(days=random.randint(0, 365)))
            fecha_str = fecha_venta.strftime(random.choice(formatos_fecha))
            id_tienda = f"T{random.randint(1, 10):02d}"
            valores.append(f"('{id_trans}', '{id_cliente}', {monto}, '{fecha_str}', '{id_tienda}')")
        
        f.write(",\n".join(valores) + ";\n")
    print("- ventas_historicas.sql generado.")

    # 6. inventario.csv (800 filas + 5% duplicados + 10% nulos)
    n_filas = 800
    df_inv = pd.DataFrame({
        "id_producto": [f"PROD_{i:04d}" for i in range(1, n_filas + 1)],
        "categoria": [random.choice(["México", "mex", "mx", "MEXICO"]) for _ in range(n_filas)], # Texto sucio
        "precio_unitario": np.random.uniform(10, 1000, n_filas).round(2),
        "stock": np.random.randint(0, 500, n_filas)
    })
    
    # Agregar 5% de duplicados (40 filas)
    duplicados = df_inv.sample(n=int(n_filas * 0.05), replace=True)
    df_inv = pd.concat([df_inv, duplicados], ignore_index=True)
    
    # Inyectar 10% de valores nulos intencionalmente
    filas_totales, columnas_totales = df_inv.shape
    total_celdas = filas_totales * columnas_totales
    n_nulos = int(total_celdas * 0.10)
    
    for _ in range(n_nulos):
        fila_idx = random.randint(0, filas_totales - 1)
        col_idx = random.choice(["categoria", "precio_unitario", "stock"]) # Evitamos nulos en ID para mantener control
        df_inv.loc[fila_idx, col_idx] = np.nan
        
    df_inv.to_csv("inventario.csv", index=False)
    print("- inventario.csv generado (con nulos y duplicados).")
    
    print("\n¡Todos los archivos han sido generados exitosamente!")

if __name__ == "__main__":
    generar_datos()