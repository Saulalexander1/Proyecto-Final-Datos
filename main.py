import pandas as pd
import Extraccion
import Transformacion
import Analisis
import Visualizador
import sys

def run_pipeline():
    print("="*50)
    print(" INICIANDO PIPELINE DE DATOS RETAIL (ETL) ")
    print("="*50)

    try:
        # EXTRACCIÓN (Extract)
        print("\n[1/5] FASE DE EXTRACCIÓN DE DATOS...")
        # Nota: Asegúrate de que tu base de datos SQL y MongoDB estén corriendo
        df_ventas = Extraccion.extract_sql()
        df_perfiles = Extraccion.extract_nosql()
        df_inventario = Extraccion.extract_csv()
        
        # Extracción de otras fuentes (Opcional, se guardan en memoria)
        # df_api = Extraccion.extract_from_api()
        # df_competencia = Extraccion.extract_from_web_scraping()

        # TRANSFORMACIÓN (Transform)
        print("\n[2/5] FASE DE TRANSFORMACIÓN Y LIMPIEZA...")
        # Pasamos los DataFrames crudos al pipeline de transformación
        df_master_transformado, df_inventario_clean = Transformacion.run_transformation_pipeline(
            df_ventas=df_ventas, 
            df_perfiles=df_perfiles, 
            df_inventario=df_inventario
        )

        # ANALÍTICA AVANZADA (PCA)
        print("\n[3/5] FASE DE ANALÍTICA AVANZADA...")
        # Aplicamos el modelo PCA para reducir las variables de comportamiento a 3 dimensiones
        df_final = Analisis.apply_advanced_analytics(df_master_transformado)

        # CARGA Y ALMACENAMIENTO (Load)
        print("\n[4/5] FASE DE ALMACENAMIENTO Y EXPORTACIÓN...")
        output_file = 'data_master_clean.parquet'
        
        # Guardamos el archivo optimizado
        df_final.to_parquet(output_file, index=False)
        print(f"[ÉXITO] Repositorio maestro guardado como: {output_file}")

        # VISUALIZACIÓN (Dashboarding)
        print("\n[5/5] FASE DE VISUALIZACIÓN DE INSIGHTS...")
        # Llama a las gráficas (Boxplots, Scatter, Sankey)
        Visualizador.generate_dashboard()

        print("\n" + "="*50)
        print(" PIPELINE COMPLETADO EXITOSAMENTE ")
        print("="*50)

    except Exception as e:
        print("\n[ERROR CRÍTICO] El pipeline se ha detenido debido a un error:")
        print(f"Detalle: {e}")
        print("Por favor, revisa tus conexiones a bases de datos y la existencia de los archivos.")
        sys.exit(1)

if __name__ == "__main__":
    # Ejecuta el orquestador solo si el archivo es llamado directamente
    run_pipeline()