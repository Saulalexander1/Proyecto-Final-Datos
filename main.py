import extraccion, transformacion, analisis
import pandas as pd

def run_pipeline():
    print("Iniciando Extracción...")
    v = extract.extract_sql()
    p = extract.extract_nosql()
    i = extract.extract_csv()
    
    print("Iniciando Transformación...")
    v_clean, p_clean, i_clean = transform.clean_data(v, p, i)
    master = transform.enrich_and_rules(v_clean, p_clean)
    
    print("Aplicando PCA...")
    final_df = analytics.apply_pca(master)
    
    # Guardar entregable final optimizado 
    final_df.to_parquet('data_master_clean.parquet')
    print("Pipeline completado. Archivo 'data_master_clean.parquet' generado.")

if __name__ == "__main__":
    run_pipeline()