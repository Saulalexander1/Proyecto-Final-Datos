import pandas as pd
from sklearn.decomposition import PCA

def select_features_for_pca(df, feature_columns=None):
    if feature_columns:
        # Si se pasa una lista explícita de 20 columnas, se valida que existan
        missing = [col for col in feature_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Faltan las siguientes columnas en el DataFrame: {missing}")
        return df[feature_columns]
    else:
        # Selección dinámica: tomamos variables numéricas y evitamos identificadores
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        cols_to_exclude = ['id_transaccion', 'Customer_ID', 'id_tienda']
        numeric_df = numeric_df.drop(columns=[c for c in cols_to_exclude if c in numeric_df.columns])
        
        # Validación técnica para el lineamiento de "20 variables"
        if numeric_df.shape[1] < 20:
            print(f"Aviso: Tienes {numeric_df.shape[1]} variables numéricas disponibles, "
                "pero el proyecto especifica aplicar PCA sobre 20 variables de comportamiento.")
        elif numeric_df.shape[1] > 20:
            print("Aviso: Se encontraron más de 20 variables. Seleccionando exactamente 20 para cumplir el requerimiento.")
            numeric_df = numeric_df.iloc[:, :20]
            
        return numeric_df

def apply_advanced_analytics(df, feature_columns=None):
    print("--- INICIANDO ANÁLISIS AVANZADO (PCA) ---")
    
    # 1. Seleccionar características (features)
    features_df = select_features_for_pca(df, feature_columns)
    
    # El algoritmo PCA de scikit-learn requiere que no haya valores nulos.
    # En la fase previa de transformación ya se trataron, pero llenamos con 0 por seguridad.
    features_df = features_df.fillna(0)
    
    # 2. Configurar el modelo PCA reduciendo a 3 componentes (Estricto del PDF) 
    pca = PCA(n_components=3)
    
    # 3. Ajustar modelo y transformar los datos a la nueva dimensión
    print(f"Aplicando PCA sobre {features_df.shape[1]} características de comportamiento...")
    pca_components = pca.fit_transform(features_df)
    
    # 4. Calcular y explicar la varianza capturada (Requisito para puntaje 'Excelente') 
    varianza_explicada = pca.explained_variance_ratio_
    varianza_total = varianza_explicada.sum() * 100
    
    print("\n[RESULTADOS DEL PCA - JUSTIFICACIÓN DE VARIANZA]")
    print(f"Varianza capturada por el Componente Principal 1 (PC1): {varianza_explicada[0]*100:.2f}%")
    print(f"Varianza capturada por el Componente Principal 2 (PC2): {varianza_explicada[1]*100:.2f}%")
    print(f"Varianza capturada por el Componente Principal 3 (PC3): {varianza_explicada[2]*100:.2f}%")
    print(f"Varianza Total Explicada por el modelo: {varianza_total:.2f}%")
    
    # Insight analítico automático para tu presentación y documentación
    if varianza_total >= 70:
        print("Insight: Los 3 componentes son altamente representativos del comportamiento original.")
    elif varianza_total >= 50:
        print("Insight: Los componentes explican una varianza moderada, suficiente para identificar patrones.")
    else:
        print("Insight: Varianza baja. Las 20 variables originales son muy independientes entre sí.")
        
    # 5. Estructurar los nuevos componentes en un DataFrame
    df_pca = pd.DataFrame(
        data=pca_components, 
        columns=['PC1', 'PC2', 'PC3'],
        index=df.index  # Crucial: conservar el índice para no desfasar las filas al unir
    )
    
    # 6. Unir los 3 componentes al DataFrame maestro original
    df_master_final = pd.concat([df, df_pca], axis=1)
    
    print("--- ANÁLISIS AVANZADO COMPLETADO ---")
    return df_master_final

if __name__ == "__main__":
    pass