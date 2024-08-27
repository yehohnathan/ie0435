# ---------------- # Se importan las librerías necesarias # ----------------- #
import pandas as pd                     # Manejo del CSV
from Proyecto1.src.KMedias import SistemasAgrupamiento
# Para evitar el error de detección de nucleos de mi computadora
import os   # Evita la detección de nucleos
os.environ['LOKY_MAX_CPU_COUNT'] = '2'

# -------------------------- # Se importa el CSV # -------------------------- #
name_csv = ("../Datos_Abiertos_ARESEP" +
            "_Indicadores_de_continuidad_por_empresa_2022.csv")

# ---------------------- # Análisis y limpiza del CSV # --------------------- #
# Se carga el CSV en un DataFrame:
aresep_df = pd.read_csv(name_csv)
aresep_df = aresep_df.loc[:, ['DPIR', 'FPI', 'Abonados Por Circuito']]

# Eliminar filas con valores NaN
aresep_df = aresep_df.dropna()

# Se muestra la información del DataFrame al usuario:
print("\n================= Datos originales del DataFrame: ==================")
print(aresep_df)

# Análisis exploratorio de datos:
print("\n==================== Información del DataFrame: ====================")
aresep_df.info()

# --- # Prueba de K-Means # --- #
kmedias = SistemasAgrupamiento()
kmedias.setDataFrame(aresep_df)
kmedias.metodo_elbow(['Abonados Por Circuito', 'DPIR', 'FPI'])
kmedias.grafica_KMeans('Abonados Por Circuito', 'DPIR',
                       'Abonados', 'DPIR', k_clusters=4)
kmedias.grafica_KMeans_3D('Abonados Por Circuito', 'DPIR', 'FPI',
                          'Abonados', 'DPIR', 'FPI', k_clusters=4)
