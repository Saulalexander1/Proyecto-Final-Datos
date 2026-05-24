import pandas as pd
import Extraccion
import Transformacion
import Analisis
import Visualizador
import sys
import importlib

# Esto obliga a Python a recargar el archivo por si se quedó pegado en la memoria caché
importlib.reload(Extraccion)

def run_pipeline():
    print("="*50)
    print(" INICIANDO PIPELINE DE DATOS RETAIL (ETL) ")
    print("="*50)

    try:
        # EXTRACCIÓN (Extract)
        print("\n[1/5] FASE DE EXTRACCIÓN DE DATOS...")
        
        # --- BLOQUE DE AUTO-CORRECCIÓN DE FUNCIONES ---
        # 1. Intentamos leer SQL
        if hasattr(Extraccion, 'extract_from_sql'):
            df_ventas = Extraccion.extract_from_sql()
        elif hasattr(Extraccion, 'extract_sql'):
            df_ventas = Extraccion.extract_sql()
        else:
            raise AttributeError("No se encontró ninguna función para extraer SQL en Extraccion.py")

        # 2. Intentamos leer Mongo
        if hasattr(Extraccion, 'extract_from_mongodb'):
            df_perfiles = Extraccion.extract_from_mongodb()
        elif hasattr(Extraccion, 'extract_nosql'):
            df_perfiles = Extraccion.extract_nosql()
        else:
            raise AttributeError("No se encontró ninguna función para extraer Mongo en Extraccion.py")

        # 3. Intentamos leer CSV
        try:
            df_inventario = Extraccion.extract_csv('inventario.csv')
        except TypeError:
            df_inventario = Extraccion.extract_csv()
        # ----------------------------------------------


        # TRANSFORMACIÓN (Transform)
        print("\n[2/5] FASE DE TRANSFORMACIÓN Y LIMPIEZA...")
        df_master_transformado, df_inventario_clean = Transformacion.run_transformation_pipeline(
            df_ventas=df_ventas, 
            df_perfiles=df_perfiles, 
            df_inventario=df_inventario
        )

        # ANALÍTICA AVANZADA (PCA)
        print("\n[3/5] FASE DE ANALÍTICA AVANZADA...")
        df_final = Analisis.apply_advanced_analytics(df_master_transformado)

        # CARGA Y ALMACENAMIENTO (Load)
        print("\n[4/5] FASE DE ALMACENAMIENTO Y EXPORTACIÓN...")
        output_file = 'data_master_clean.parquet'
        
        df_final.to_parquet(output_file, index=False)
        print(f"[ÉXITO] Repositorio maestro guardado como: {output_file}")

        # VISUALIZACIÓN (Dashboarding)
        print("\n[5/5] FASE DE VISUALIZACIÓN DE INSIGHTS...")
        Visualizador.generate_dashboard()

        print("\n" + "="*50)
        print(" PIPELINE COMPLETADO EXITOSAMENTE ")
        print("="*50)

    except Exception as e:
        print("\n[ERROR CRÍTICO] El pipeline se ha detenido debido a un error:")
        print(f"Detalle: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()