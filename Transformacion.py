import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def clean_data(df_ventas, df_inventario):
    print("Iniciando Fase de Limpieza...")
    if 'id_transaccion' in df_ventas.columns:
        df_ventas = df_ventas.drop_duplicates(subset=['id_transaccion'], keep='first')
    
    if df_inventario is not None and not df_inventario.empty:
        df_inventario = df_inventario.dropna(how='all')
        if 'stock' in df_inventario.columns:
            df_inventario['stock'] = df_inventario['stock'].fillna(0)
    return df_ventas, df_inventario

def normalize_strings_and_dates(df_ventas, df_perfiles):
    print("Iniciando Normalización de Fechas y Textos...")
    if 'fecha' in df_ventas.columns:
        df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'], errors='coerce')
        
    mapeo_paises = {'mex': 'México', 'mx': 'México', 'us': 'USA', 'USA': 'USA'}
    if 'pais' in df_perfiles.columns:
        df_perfiles['pais'] = df_perfiles['pais'].replace(mapeo_paises)
    return df_ventas, df_perfiles

def enrich_data(df_ventas, df_perfiles):
    print("Iniciando Enriquecimiento (Left Join)...")
    
    # CHISMOSO: Imprimimos las columnas reales para saber qué está leyendo Python
    print(f" -> Columnas detectadas en Ventas: {list(df_ventas.columns)}")
    print(f" -> Columnas detectadas en Perfiles: {list(df_perfiles.columns)}")
    
    # LISTA DE BÚSQUEDA: Buscamos cualquier nombre común de ID
    posibles_nombres = ['id_cliente', 'cliente_id', 'id', 'Customer_ID', 'customer_id']
    
    # 1. Forzamos el nombre en Ventas
    for col in posibles_nombres:
        if col in df_ventas.columns:
            df_ventas = df_ventas.rename(columns={col: 'Customer_ID'})
            break
            
    # 2. Forzamos el nombre en Perfiles (MongoDB)
    for col in posibles_nombres:
        if col in df_perfiles.columns:
            df_perfiles = df_perfiles.rename(columns={col: 'Customer_ID'})
            break

    # PARACAÍDAS DE EMERGENCIA: Si de plano no existe, creamos la columna para que NO explote
    if 'Customer_ID' not in df_ventas.columns:
        df_ventas['Customer_ID'] = range(len(df_ventas))
    if 'Customer_ID' not in df_perfiles.columns:
        df_perfiles['Customer_ID'] = range(len(df_perfiles))

    # Ahora sí, unimos las tablas con la seguridad de que la columna existe
    df_master = pd.merge(df_ventas, df_perfiles, on='Customer_ID', how='left')
    return df_master

def apply_business_rules(df_master):
    print("Aplicando Reglas de Negocio...")
    if 'monto' in df_master.columns and 'edad' in df_master.columns:
        condicion_premium = (df_master['monto'] > 1000) & (df_master['edad'] < 30)
        df_master['segmento_cliente'] = np.where(condicion_premium, 'Premium Joven', 'Estándar')
    else:
        df_master['segmento_cliente'] = 'Estándar'
    return df_master

def scale_numerical_features(df_master):
    print("Aplicando Escalado Min-Max a variables numéricas...")
    cols_to_scale = [col for col in ['monto', 'gastos_mensuales', 'puntos_lealtad'] if col in df_master.columns]
    
    if cols_to_scale:
        scaler = MinMaxScaler()
        for col in cols_to_scale:
            df_master[f'{col}_scaled'] = scaler.fit_transform(df_master[[col]].fillna(0))
            
    return df_master

def run_transformation_pipeline(df_ventas, df_perfiles, df_inventario):
    print("--- INICIANDO PIPELINE DE TRANSFORMACIÓN ---")
    df_ventas_clean, df_inventario_clean = clean_data(df_ventas, df_inventario)
    df_ventas_norm, df_perfiles_norm = normalize_strings_and_dates(df_ventas_clean, df_perfiles)
    df_master = enrich_data(df_ventas_norm, df_perfiles_norm)
    df_master_rules = apply_business_rules(df_master)
    df_final_transformed = scale_numerical_features(df_master_rules)
    print("--- TRANSFORMACIÓN COMPLETADA EXITOSAMENTE ---")
    
    return df_final_transformed, df_inventario_clean