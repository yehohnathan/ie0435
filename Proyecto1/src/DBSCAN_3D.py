# ---------------- # Se importan las librerías necesarias # ----------------- #
import pandas as pd                         # Manejo del CSV
import numpy as np
import matplotlib.pyplot as plt             # Gráficas
from sklearn.cluster import DBSCAN          # Agrupamiento DBSCAN
from sklearn.preprocessing import StandardScaler    # Escalado de datos
from sklearn.neighbors import NearestNeighbors      # Calcular distancias KNN


# ----------- # Clase para los Sistemas de Agrupamiento DBSCAN # ------------ #
class DBSCAN_3D:
    def __init__(self) -> None:
        self.__dataframe = pd.DataFrame()

    def setDataFrame(self, dataframe):
        # Verifica si dataframe es algo diferente a lo esperado
        if not isinstance(dataframe, pd.core.frame.DataFrame):
            raise ValueError("\nNo se ingresó un DataFrame.")
        self.__dataframe = dataframe

    def __verificador_columnas(self, columnas):
        # Verifica que columnas sea una lista y contenga 3 elementos
        if not isinstance(columnas, list) or len(columnas) != 3:
            raise ValueError("Debe ingresar una lista con tres" +
                             "nombres de columnas.")

        # Verifica que todas las columnas en la lista sean cadenas de texto
        for col in columnas:
            if not isinstance(col, str):
                raise ValueError("Cada nombre de columna debe ser" +
                                 " una cadena de texto.")

        # Verificar que todas las columnas existan dentro del DataFrame
        for col in columnas:
            if col not in self.__dataframe.columns:
                raise ValueError(f"La columna {col} no existe dentro" +
                                 " del DataFrame.")

    def __realizar_DBSCAN(self, columnas, eps=0.5, min_samples=5):
        # Escalado de los datos
        data = self.__dataframe[columnas]
        scaler = StandardScaler()
        scaler_data = scaler.fit_transform(data)

        # Realizar DBSCAN
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(scaler_data)

        # Agregar los resultados de los clusters al DataFrame
        self.__dataframe['cluster_dbscan'] = clusters

    def estimar_eps(self, columnas, min_samples=5):
        # Verificar las columnas
        self.__verificador_columnas(columnas)

        # Escalado de los datos
        data = self.__dataframe[columnas]
        scaler = StandardScaler()
        scaler_data = scaler.fit_transform(data)

        # Calcular distancias de k-vecinos
        neigh = NearestNeighbors(n_neighbors=min_samples)
        nbrs = neigh.fit(scaler_data)
        distances, indices = nbrs.kneighbors(scaler_data)

        # Ordenar distancias de k-vecinos
        distances = np.sort(distances[:, min_samples - 1], axis=0)

        # Graficar distancias de k-vecinos
        plt.plot(distances)
        plt.title('Gráfico de distancia de k-vecinos')
        plt.xlabel('Puntos ordenados por distancia al k-ésimo vecino')
        plt.ylabel(f'Distancia al {min_samples}º vecino más cercano')
        plt.show()

    def grafica_DBSCAN_3D(self, colum1, colum2, colum3,
                          xlabel="", ylabel="", zlabel="",
                          eps=0.5, min_samples=5):
        # Verificar las columnas antes de proceder
        columnas = [colum1, colum2, colum3]
        self.__verificador_columnas(columnas)

        # Realizar DBSCAN (llamando al método privado)
        self.__realizar_DBSCAN(columnas, eps, min_samples)

        # Si los labels no se proporcionan, usar los nombres de las columnas
        xlabel = xlabel if xlabel else colum1
        ylabel = ylabel if ylabel else colum2
        zlabel = zlabel if zlabel else colum3

        # Graficar en 3D
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.__dataframe[colum1], self.__dataframe[colum2],
                   self.__dataframe[colum3],
                   c=self.__dataframe['cluster_dbscan'],
                   cmap='viridis', marker='o')

        ax.set_title('Clusters usando DBSCAN en 3D')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        plt.show()

    def mostrar_clusters(self, colum1, colum2, colum3, eps=0.5, min_samples=5):
        columnas = [colum1, colum2, colum3]
        self.__verificador_columnas(columnas)

        data = self.__dataframe[columnas]
        scaler = StandardScaler()
        scaler_data = scaler.fit_transform(data)

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(scaler_data)

        unique_labels = set(labels)
        for label in unique_labels:
            if label == -1:
                # -1 es considerado ruido
                print(f"Ruido: {len(data[labels == label])} elementos.")
            else:
                cluster_points = scaler_data[labels == label]
                centroid = cluster_points.mean(axis=0)
                print(f"Cluster {label + 1}: Centroide = {centroid} con {len(cluster_points)} elementos.")
