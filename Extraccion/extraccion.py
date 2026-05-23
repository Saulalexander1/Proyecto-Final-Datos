import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from pymongo import MongoClient
import xml.etree.ElementTree as ET

#BASES DE DATOS (SQL & NoSQL)

def extract_from_sql():
    """Conecta a la base de datos relacional (MySQL/PostgreSQL) y extrae las ventas."""
    DATABASE_URI = 'mysql+pymysql://root:123456789@localhost:3306/ventas_historicas'
    
    engine = create_engine(DATABASE_URI)
    
    # Consulta para extraer las columnas solicitadas en los lineamientos 
    query = """SELECT id_transaccion, id_cliente, monto, fecha, id_tienda FROM ventas_historicas;"""
    
    print("Conectando a SQL y extrayendo histórico de ventas...")
    df_sql = pd.read_sql_query(query, con=engine)
    return df_sql



def extract_from_mongodb():
    """Conecta a MongoDB y extrae los perfiles de usuario en formato JSON."""
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = "retail_db"
    COLLECTION_NAME = "perfiles_usuarios"
    
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    print("Conectando a MongoDB y extrayendo perfiles de usuario...")
    # Extraer todos los documentos de la colección
    documentos = list(collection.find({}, {"_id": 0})) # Excluimos el ObjectId de Mongo
    
    # Convertir la lista de diccionarios/JSON directamente a un DataFrame de Pandas
    df_mongo = pd.DataFrame(documentos)
    return df_mongo


#ARCHIVOS PLANOS Y ESTRUCTURADOS

def extract_csv(file_path='datos/inventario.csv'):
    """Lee el archivo plano de inventario con datos crudos."""
    print(f"Leyendo archivo plano: {file_path}...")
    return pd.read_csv(file_path)


def extract_server_logs(file_path='datos/logs_servidor.txt'):
    """Lee las líneas del archivo de logs para su posterior parsing con RegEx."""
    print(f"Leyendo registros de actividad web: {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Retorna las líneas crudas en una lista para procesar en la transformación
    return lines


def extract_xml(file_path='datos/catalogos.xml'):
    """Parsea el archivo XML con las definiciones de categorías de productos."""
    print(f"Estructurando datos desde XML: {file_path}...")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Iterar sobre la estructura XML para aplanarla en un DataFrame
    data = []
    for categoria in root.findall('categoria'):
        id_cat = categoria.find('id').text if categoria.find('id') is not None else None
        nombre_cat = categoria.find('nombre').text if categoria.find('nombre') is not None else None
        data.append({'id_categoria': id_cat, 'categoria_producto': nombre_cat})
        
    return pd.DataFrame(data)


def extract_excel(file_path='datos/metas_anuales.xlsx'):
    """Extrae las metas y KPIs de negocio por región desde Excel."""
    print(f"Leyendo KPIs de negocio desde Excel: {file_path}...")
    return pd.read_excel(file_path)


#FUENTES EXTERNAS (API & WEB SCRAPING)

def extract_from_api(api_url="https://api.exchangerate-api.com/v4/latest/USD"):
    """Consume una API REST real para obtener tipos de cambio de monedas."""
    print(f"Consumiendo API REST en: {api_url}...")
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # Convertimos el diccionario de tasas de cambio directamente a DataFrame
        df_api = pd.DataFrame(list(data['rates'].items()), columns=['Moneda', 'Tipo_Cambio'])
        return df_api
    else:
        raise Exception(f"Error al consumir la API. Código de estado: {response.status_code}")


def extract_from_web_scraping(url="https://www.sears.com.mx/buscar/laptop"):
    """Realiza Web Scraping para extraer precios de la competencia desde la página de Sears."""
    print(f"Extrayendo precios de competencia mediante Web Scraping desde: {url}...")
    
    # IMPORTANTE: Los e-commerce grandes como Sears bloquean scripts automáticos.
    # Usamos un 'User-Agent' real para simular que somos un navegador web (Chrome) y evitar bloqueos.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Aviso: Sears respondió con código {response.status_code}. Puede tener protección anti-bots (Cloudflare).")
            # Devolvemos un DataFrame vacío con la estructura correcta para no romper el pipeline
            return pd.DataFrame(columns=['Producto', 'Precio_Competencia'])
            
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = []
        
        # En la estructura de Sears, buscamos los contenedores de las tarjetas de producto.
        # (Nota: Las clases pueden cambiar si la página se actualiza, estas son las etiquetas estándar de su grid)
        tarjetas = soup.find_all('div', class_='cardProduct') or soup.find_all('div', class_='product-item')
        
        for tarjeta in tarjetas:
            # Buscamos el título/nombre del producto
            nombre_elem = tarjeta.find('h3') or tarjeta.find('div', class_='titleProduct')
            # Buscamos el precio asignado
            precio_elem = tarjeta.find('span', class_='price') or tarjeta.find('p', class_='actualPrice')
            
            if nombre_elem and precio_elem:
                productos.append({
                    'Producto': nombre_elem.text.strip(),
                    'Precio_Competencia': precio_elem.text.strip()
                })
        
        # Convertimos la lista de elementos en la estructura tabular requerida por el proyecto
        df_competencia = pd.DataFrame(productos)
        
        # Si el scraper fue bloqueado y el dataframe quedó vacío, le damos soporte para que el pipeline continúe
        if df_competencia.empty:
            print("Aviso: No se pudieron leer las clases dinámicas de Sears (común por renderizado de JavaScript o protección perimetral).")
            df_competencia = pd.DataFrame(columns=['Producto', 'Precio_Competencia'])
            
        return df_competencia

    except Exception as e:
        print(f"Error al conectar con Sears: {e}")
        # Retorno seguro para evitar que falle el main.py
        return pd.DataFrame(columns=['Producto', 'Precio_Competencia'])