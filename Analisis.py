import pandas as pd
from sklearn.decomposition import PCA

def apply_advanced_analytics(df_master):
    print("--- INICIANDO ANÁLISIS AVANZADO (PCA) ---")
    
    # 1. Buscamos todas las columnas numéricas que sirvan para el modelo
    # Ignoramos los IDs porque no son comportamientos, son solo identificadores
    columnas_ignoradas = ['id_transaccion', 'Customer_ID', 'id_tienda']
    cols_pca = [col for col in df_master.columns 
                if pd.api.types.is_numeric_dtype(df_master[col]) and col not in columnas_ignoradas]
    
    if not cols_pca:
        print("Aviso: No se encontraron variables numéricas. Saltando PCA...")
        # Si no hay columnas, creamos columnas falsas para que no falle la visualización
        df_master['PC1'] = 0.0
        df_master['PC2'] = 0.0
        df_master['PC3'] = 0.0
        return df_master

    print(f"Aplicando PCA sobre {len(cols_pca)} variables detectadas: {cols_pca}")
    
    # 2. Ajustamos los componentes para no romper las leyes de las matemáticas
    # Si tenemos menos de 3 variables, usamos ese número; si tenemos más, usamos 3.
    n_components = min(3, len(cols_pca))
    
    # 3. Aplicamos el modelo PCA llenando los nulos temporales con 0
    pca = PCA(n_components=n_components)
    componentes = pca.fit_transform(df_master[cols_pca].fillna(0))
    
    # 4. Guardamos los resultados en el DataFrame
    for i in range(n_components):
        df_master[f'PC{i+1}'] = componentes[:, i]
        
    # PARACAÍDAS: Si se generaron menos de 3 componentes (porque había menos de 3 variables),
    # creamos las columnas faltantes llenas de ceros para que la Visualización no explote.
    for i in range(n_components + 1, 4):
        df_master[f'PC{i}'] = 0.0
        
    print(f"--- PCA COMPLETADO EXITOSAMENTE ({n_components} componentes reales extraídos) ---")
    return df_master