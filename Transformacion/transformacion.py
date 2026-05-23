import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def clean_data(df_ventas, df_inventario):
    print("Iniciando Fase de Limpieza...")
    
    # Eliminar transacciones duplicadas en el SQL (ventas)
    # Asumimos que 'id_transaccion' es el identificador único
    df_ventas = df_ventas.drop_duplicates(subset=['id_transaccion'], keep='first')
    
    # Manejo de nulos en el inventario.csv (ej. imputando con 0 o eliminando)
    # Aquí rellenamos con 0 el stock nulo y eliminamos filas completamente vacías
    df_inventario = df_inventario.dropna(how='all')
    df_inventario['stock'] = df_inventario['stock'].fillna(0)
    
    return df_ventas, df_inventario


def normalize_strings_and_dates(df_ventas, df_perfiles):
    """
    Fase 2a: Normalización de formatos (Fechas y Strings).
    """
    print("Iniciando Normalización de Fechas y Textos...")
    
    #Convertir fechas a datetime64
    #'errors='coerce'' convierte los formatos inválidos a NaT (Not a Time)
    df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'], errors='coerce')
    
    #Limpieza de texto sucio en categorías (Ej: Países/Ubicación)
    #Mapeo para estandarizar cadenas de texto a "México"
    mapeo_paises = {
        'mex': 'México',
        'mx': 'México',
        'MX': 'México',
        'MEXICO': 'México',
        'mexico': 'México'
    }
    
    #Asumiendo que la columna de ubicación se llama 'pais' o similar en MongoDB
    if 'pais' in df_perfiles.columns:
        #Se normaliza todo a minúsculas temporalmente para asegurar que coincida con el mapeo (si es necesario) 
        #o se reemplaza directamente usando el diccionario
        df_perfiles['pais'] = df_perfiles['pais'].replace(mapeo_paises)
        
    return df_ventas, df_perfiles


def enrich_data(df_ventas, df_perfiles):
    print("Iniciando Enriquecimiento (Left Join)...")
    
    # Unión de los datos usando 'Customer_ID' como llave primaria
    df_master = pd.merge(df_ventas, df_perfiles, on='Customer_ID', how='left')
    
    return df_master


def apply_business_rules(df_master):
    print("Aplicando Reglas de Negocio...")
    
    # Regla: Si gasto (monto) > 1000 y edad < 30, entonces "Premium Joven"
    condicion_premium = (df_master['monto'] > 1000) & (df_master['edad'] < 30)
    
    df_master['segmento_cliente'] = np.where(
        condicion_premium, 
        'Premium Joven', 
        'Estándar' # Valor por defecto si no cumple la regla
    )
    
    return df_master


def scale_numerical_features(df_master):
    print("Aplicando Escalado Min-Max a variables numéricas...")
    
    # Seleccionamos las variables numéricas a escalar (ej: monto, gastos_mensuales, etc.)
    # Aquí puedes añadir más columnas numéricas que tengas en tu dataset final
    cols_to_scale = ['monto'] 
    
    if 'gastos_mensuales' in df_master.columns:
        cols_to_scale.append('gastos_mensuales')
        
    if 'puntos_lealtad' in df_master.columns:
        cols_to_scale.append('puntos_lealtad')
        
    scaler = MinMaxScaler()
    
    # Aplicamos el escalado y sobreescribimos o creamos nuevas columnas
    # Crearemos columnas con sufijo '_scaled' para no perder el dato original en caso de validación
    for col in cols_to_scale:
        df_master[f'{col}_scaled'] = scaler.fit_transform(df_master[[col]])
        
    return df_master


def run_transformation_pipeline(df_ventas, df_perfiles, df_inventario):
    print("--- INICIANDO PIPELINE DE TRANSFORMACIÓN (ETL FASE 1 Y 2) ---")
    
    # 1. Limpieza
    df_ventas_clean, df_inventario_clean = clean_data(df_ventas, df_inventario)
    
    # 2. Normalización de Strings y Fechas
    df_ventas_norm, df_perfiles_norm = normalize_strings_and_dates(df_ventas_clean, df_perfiles)
    
    # 3. Enriquecimiento (Left Join)
    df_master = enrich_data(df_ventas_norm, df_perfiles_norm)
    
    # 4. Reglas de Negocio
    df_master_rules = apply_business_rules(df_master)
    
    # 5. Escalado Min-Max (Preparación para PCA)
    df_final_transformed = scale_numerical_features(df_master_rules)
    
    print("--- TRANSFORMACIÓN COMPLETADA EXITOSAMENTE ---")
    
    return df_final_transformed, df_inventario_clean