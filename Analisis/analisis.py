from sklearn.decomposition import PCA
import pandas as pd

def apply_pca(df):
    # Seleccionar 20 variables de comportamiento (simuladas aquí como columnas numéricas)
    # Nota: En tu proyecto real, asegúrate de tener 20 columnas numéricas escaladas.
    features = df.select_dtypes(include=['float64', 'int64']).drop(columns=['id_transaccion', 'Customer_ID'])
    
    pca = PCA(n_components=3) # Reducción a 3 componentes
    components = pca.fit_transform(features.fillna(0))
    
    df_pca = pd.DataFrame(data=components, columns=['PC1', 'PC2', 'PC3'])
    print(f"Varianza explicada: {pca.explained_variance_ratio_.sum()}") [cite: 75]
    
    return pd.concat([df, df_pca], axis=1)