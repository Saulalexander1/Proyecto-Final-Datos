import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def clean_data(df_ventas, df_perfiles, df_inv):
    # 1. Limpieza: Eliminar duplicados y tratar nulos [cite: 32]
    df_ventas = df_ventas.drop_duplicates()
    df_inv = df_inv.dropna(subset=['stock'])
    
    # 2. Normalización de strings [cite: 29, 68]
    pais_map = {'mex': 'México', 'mx': 'México', 'us': 'USA'}
    df_perfiles['pais'] = df_perfiles['pais'].replace(pais_map)
    
    # 3. Normalización de fechas [cite: 33]
    df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'])
    
    return df_ventas, df_perfiles, df_inv

def enrich_and_rules(df_ventas, df_perfiles):
    # Enriquecimiento: Left Join [cite: 34, 71]
    master_df = pd.merge(df_ventas, df_perfiles, on='Customer_ID', how='left')
    
    # Reglas de Negocio: Segmento Cliente [cite: 35, 71]
    master_df['segmento_cliente'] = np.where(
        (master_df['monto'] > 300) & (master_df['edad'] < 30), 
        "Premium Joven", "Estándar"
    )
    
    # Escalado Min-Max para PCA [cite: 33, 70]
    scaler = MinMaxScaler()
    master_df['monto_esc'] = scaler.fit_transform(master_df[['monto']])
    
    return master_df