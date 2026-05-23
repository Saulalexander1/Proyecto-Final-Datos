import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from pymongo import MongoClient

# =====================================================================
# 1. BASES DE DATOS (SQL & NoSQL)
# =====================================================================

def extract_from_sql():
    """Conecta a la base de datos MySQL y extrae las ventas."""
    
    # ⚠️ REEMPLAZA ESTOS DATOS CON LOS DE TU MYSQL LOCAL ⚠️
    usuario = "root"              # Tu usuario de MySQL (suele ser root)
    contrasena = "123456789"  # Tu contraseña de MySQL
    host = "localhost"            # o la IP de tu servidor
    puerto = "3306"               # Puerto por defecto de MySQL
    base_datos = "ventas_historicas"      # Nombre de la base de datos donde tienes la tabla
    
    # Cadena de conexión específica para MySQL usando pymysql
    DATABASE_URI = f"mysql+pymysql://{usuario}:{contrasena}@{host}:{puerto}/{base_datos}"
    
    engine = create_engine(DATABASE_URI)
    
    # La consulta a la tabla que pide tu PDF
    query = """
        SELECT id_transaccion, id_cliente, monto, fecha, id_tienda 
        FROM ventas_historicas;
    """
    print("Conectando a MySQL y extrayendo histórico de ventas...")
    df_sql = pd.read_sql_query(query, con=engine)
    return df_sql


def extract_from_mongodb():
    """Conecta a MongoDB y extrae los perfiles de usuario."""
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = "retail_db"
    COLLECTION_NAME = "perfiles_usuarios"
    
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    print("Conectando a MongoDB y extrayendo perfiles de usuario...")
    documentos = list(collection.find({}, {"_id": 0})) 
    df_mongo = pd.DataFrame(documentos)
    return df_mongo


# =====================================================================
# 2. ARCHIVOS PLANOS Y ESTRUCTURADOS
# =====================================================================

def extract_csv(file_path='inventario.csv'):
    """Lee el archivo plano de inventario con datos crudos."""
    print(f"Leyendo archivo plano: {file_path}...")
    return pd.read_csv(file_path)


# =====================================================================
# 3. FUENTES EXTERNAS (API & WEB SCRAPING) - Opcionales para el main
# =====================================================================

def extract_from_api(api_url="https://api.exchangerate-api.com/v4/latest/USD"):
    print(f"Consumiendo API REST en: {api_url}...")
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(list(data['rates'].items()), columns=['Moneda', 'Tipo_Cambio'])
    else:
        raise Exception("Error al consumir la API.")

def extract_from_web_scraping(url="https://www.sears.com.mx/buscar/laptop"):
    print(f"Extrayendo web scraping desde: {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = []
        tarjetas = soup.find_all('div', class_='cardProduct') or soup.find_all('div', class_='product-item')
        
        for tarjeta in tarjetas:
            nombre_elem = tarjeta.find('h3') or tarjeta.find('div', class_='titleProduct')
            precio_elem = tarjeta.find('span', class_='price') or tarjeta.find('p', class_='actualPrice')
            if nombre_elem and precio_elem:
                productos.append({'Producto': nombre_elem.text.strip(), 'Precio_Competencia': precio_elem.text.strip()})
        
        df = pd.DataFrame(productos)
        if df.empty:
            df = pd.DataFrame(columns=['Producto', 'Precio_Competencia'])
        return df
    except Exception:
        return pd.DataFrame(columns=['Producto', 'Precio_Competencia'])