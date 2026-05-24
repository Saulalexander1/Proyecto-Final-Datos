import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

def load_data(filepath='data_master_clean.parquet'):
    """Carga el dataset limpio directamente desde el archivo Parquet."""
    print(f"Cargando datos desde {filepath}...")
    df = pd.read_parquet(filepath)
    return df

def plot_boxplots(df):
    """Genera Boxplots para detectar outliers en los montos de venta."""
    plt.figure(figsize=(10, 6))
    # Asegúrate de que las columnas 'segmento_cliente' y 'monto' existan en tu DF real
    sns.boxplot(x='segmento_cliente', y='monto', data=df, palette='Set2')
    plt.title('Detección de Outliers en Montos de Venta por Segmento', fontsize=14)
    plt.xlabel('Segmento de Cliente', fontsize=12)
    plt.ylabel('Monto de Venta ($)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('boxplot_outliers.png')
    plt.show()

def plot_scatter_pca(df):
    """Genera un Scatter Plot para visualizar los clusters tras aplicar el PCA."""
    plt.figure(figsize=(10, 6))
    # Asegúrate de que las columnas 'PC1' y 'PC2' existan en tu DF tras el PCA
    sns.scatterplot(
        x='PC1', y='PC2', 
        hue='segmento_cliente', 
        palette='viridis', 
        data=df, 
        alpha=0.7
    )
    plt.title('Visualización de Clusters (Componentes Principales 1 y 2)', fontsize=14)
    plt.xlabel('Componente Principal 1 (PC1)', fontsize=12)
    plt.ylabel('Componente Principal 2 (PC2)', fontsize=12)
    plt.legend(title='Segmento')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('scatter_pca.png')
    plt.show()

def plot_sankey():
    """Genera un Sankey Diagram para mostrar el flujo de usuarios.
    Nota: Ajusta los valores de 'value' según las métricas reales que extraigas de tus logs.
    """
    labels = ["Visita Web (Logs)", "Añade al Carrito", "Abandono", "Checkout", "Compra Final"]
    source = [0, 0, 1, 1, 3, 3]
    target = [1, 2, 3, 2, 4, 2]
    
    # Valores de ejemplo, sustituir por agregaciones de tus datos reales
    value = [2000, 1000, 1200, 800, 1000, 200]
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = ["#3498db", "#f1c40f", "#e74c3c", "#e67e22", "#2ecc71"]
        ),
        link = dict(
            source = source,
            target = target,
            value = value,
            color = "rgba(189, 195, 199, 0.5)"
        )
    )])
    
    fig.update_layout(
        title_text="Flujo de Usuarios: Desde la Web hasta la Compra Final", 
        font_size=12
    )
    fig.write_html("sankey_diagram.html")
    fig.show()

def generate_dashboard():
    """Orquesta la creación del dashboard estático."""
    df = load_data()
    
    print("1. Generando Boxplots de montos de venta...")
    plot_boxplots(df)
    
    print("2. Generando Scatter Plot de clústeres PCA...")
    plot_scatter_pca(df)
    
    print("3. Generando Diagrama de Sankey del embudo de conversión...")
    plot_sankey()
    
    print("¡Visualizaciones completadas! Gráficos guardados en el directorio actual.")

if __name__ == "__main__":
    generate_dashboard()