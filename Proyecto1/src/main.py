# ---------------- # Se importan las librerías necesarias # ----------------- #
import pandas as pd                     # Manejo del CSV
from KMedias import KMedias
from MarkdownToCSV import MarkdownToCSV
# Para evitar el error de detección de nucleos de mi computadora
import os   # Evita la detección de nucleos
os.environ['LOKY_MAX_CPU_COUNT'] = '2'

# --------------------- # Convierte de Markdown a CSV # --------------------- #
# Prueba de pasar de AnexoA.md a AnexoA.csv
name_md = ("../Datos/AnexoA.md")
md_to_csv = MarkdownToCSV(name_md)

# Se carga la dirección del csv
name_csv = md_to_csv.convert()

# ---------------------- # Análisis y limpiza del CSV # --------------------- #
# Se carga el CSV en un DataFrame:
aresep_df = pd.read_csv(name_csv)
aresep_df = aresep_df.loc[:, ['DPIR', 'FPI', 'Abonados']]

# Eliminar filas con valores NaN
aresep_df = aresep_df.dropna()

# Se muestra la información del DataFrame al usuario:
print("\n================= Datos originales del DataFrame: ==================")
print(aresep_df)

# Análisis exploratorio de datos:
print("\n==================== Información del DataFrame: ====================")
aresep_df.info()

# --- # Prueba de K-Means # --- #
kmedias = KMedias()
kmedias.setDataFrame(aresep_df)
kmedias.metodo_elbow(['Abonados', 'DPIR', 'FPI'])
kmedias.grafica_KMeans('Abonados', 'DPIR',
                       'Abonados', 'DPIR', k_clusters=4)
kmedias.grafica_KMeans_3D('Abonados', 'DPIR', 'FPI',
                          'Abonados', 'DPIR', 'FPI', k_clusters=4)
