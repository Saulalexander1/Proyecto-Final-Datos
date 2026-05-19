import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def extract_sql():
    # Simulación de ventas_historicas.sql (5,000 - 10,000 registros) [cite: 45]
    data = {
        'id_transaccion': range(1, 6001),
        'Customer_ID': np.random.randint(100, 1200, size=6000),
        'monto': np.random.uniform(10, 500, size=6000),
        'fecha': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), 6000))
    }
    return pd.DataFrame(data)

def extract_nosql():
    # Simulación de perfiles_usuarios.json (1,000 - 2,000 registros) [cite: 47]
    data = {
        'Customer_ID': range(100, 1200),
        'edad': np.random.randint(18, 70, size=1100),
        'preferencias': np.random.choice(['Electrónica', 'Ropa', 'Hogar'], size=1100),
        'pais': np.random.choice(['México', 'mex', 'mx', 'USA', 'us'], size=1100)
    }
    return pd.DataFrame(data)

def extract_csv():
    # inventario.csv con 10% nulos y 5% duplicados [cite: 49]
    data = {'id_prod': range(1, 501), 'stock': np.random.randint(0, 100, size=500)}
    df = pd.DataFrame(data)
    # Ensuciar datos [cite: 49]
    df.loc[df.sample(frac=0.1).index, 'stock'] = np.nan
    return pd.concat([df, df.sample(frac=0.05)])

def extract_external():
    # Simulación de API y Web Scraping [cite: 51]
    # En un caso real usarías requests.get() y BeautifulSoup(html, 'html.parser')
    return {"tipo_cambio": 17.5, "competencia_precio": 150.0}