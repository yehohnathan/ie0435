# ---------------- # Se importan las librerías necesarias # ----------------- #
import pandas as pd                     # Manejo del CSV
from KMedias import KMedias
from DBSCAN_3D import DBSCAN_3D
from MarkdownToCSV import MarkdownToCSV
import matplotlib.pyplot as plt

# Configurar backend interactivo para matplotlib
plt.switch_backend('TkAgg')

# Para evitar el error de detección de nucleos de mi computadora
import os   # Evita la detección de nucleos
os.environ['LOKY_MAX_CPU_COUNT'] = '2'

# --------------------- # Convierte de Markdown a CSV # --------------------- #
# Determinar la ruta absoluta del archivo markdown
current_dir = os.path.dirname(os.path.abspath(__file__))
name_md = os.path.join(current_dir, "..", "Datos", "AnexoA.md")

# Convertir de Markdown a CSV
md_to_csv = MarkdownToCSV(name_md)
name_csv = md_to_csv.convert()

# Dataframe normalizado
name_csv_norm = md_to_csv.normalize_columns(name_csv)
# ---------------------- # Análisis y limpiza del CSV # --------------------- #
# Se carga el CSV en un DataFrame:
aresep_df = pd.read_csv(name_csv)
aresep_df_norm = pd.read_csv(name_csv_norm)
aresep_df = aresep_df.loc[:, ['DPIR', 'FPI', 'Abonados']]
aresep_df_norm = aresep_df_norm.loc[:, ['DPIR', 'FPI', 'Abonados']]

# Eliminar filas con valores NaN
aresep_df = aresep_df.dropna()
aresep_df_norm = aresep_df_norm.dropna()

# Se muestra la información del DataFrame al usuario:
print("\n================= Datos originales del DataFrame: ==================")
print(aresep_df)

# Análisis exploratorio de datos:
print("\n==================== Información del DataFrame: ====================")
aresep_df.info()

# --- # Prueba de K-Means con los dos csv# --- #
kmedias = KMedias()
kmedias_norm = KMedias()
kmedias.setDataFrame(aresep_df)
kmedias_norm.setDataFrame(aresep_df_norm)
# Estimar un valor adecuado de clusters usando el método del codo
kmedias.metodo_elbow('Abonados', 'DPIR', 'FPI')
kmedias_norm.metodo_elbow('Abonados', 'DPIR', 'FPI')
# Gráfica de los crusters creados por el algortimos
print("\nPrueba: KMeans con datos brutos de Anexo A.")
kmedias.grafica_KMeans_3D('Abonados', 'DPIR', 'FPI', k_clusters=3,
                          xlabel='Abonados por circuito')
kmedias.mostrar_clusters('Abonados', 'DPIR', 'FPI', k_clusters=3)
print("\nPrueba: KMeans con datos normalizado de Anexo A.")
kmedias_norm.grafica_KMeans_3D('Abonados', 'DPIR', 'FPI', k_clusters=3,
                          xlabel='Abonados por circuito')
kmedias_norm.mostrar_clusters('Abonados', 'DPIR', 'FPI', k_clusters=3)

# --- # Prueba de DBSCAN terna con los dos csv # --- #
dbscan = DBSCAN_3D()            # Brutos
dbscan_norm = DBSCAN_3D()       # Normalizados
dbscan.setDataFrame(aresep_df)
dbscan_norm.setDataFrame(aresep_df_norm)
# Estimar un valor adecuado para eps para ambos casos
dbscan.estimar_eps(['Abonados', 'DPIR', 'FPI'], min_samples=6)
dbscan_norm.estimar_eps(['Abonados', 'DPIR', 'FPI'], min_samples=6)
# Gráfica de los crusters creados por el algortimos
print("\nPrueba: DBSCAN con datos brutos de Anexo A.")
dbscan.grafica_DBSCAN_3D('Abonados', 'DPIR', 'FPI', eps = 1.23, min_samples=6)
dbscan.mostrar_clusters('Abonados', 'DPIR', 'FPI', eps = 1.23, min_samples=6)
print("\nPrueba: DBSCAN con datos normalizado de Anexo A.")
dbscan_norm.grafica_DBSCAN_3D('Abonados', 'DPIR', 'FPI', eps = 1.23, min_samples=6)
dbscan_norm.mostrar_clusters('Abonados', 'DPIR', 'FPI', eps = 1.23, min_samples=6)
