# ---------------- # Se importan las librerías necesarias # ----------------- #
import pandas as pd                         # Manejo del CSV
import matplotlib.pyplot as plt             # Graficas
from sklearn.cluster import KMeans          # Agrupamiento K-Means
from sklearn.preprocessing import StandardScaler    # Para elbow method

# Para evitar el error de detección de nucleos de mi computadora
import os   # Evita la detección de nucleos
os.environ['LOKY_MAX_CPU_COUNT'] = '2'


# --------------- # Clase para los Sistemas de Agrupamiento # --------------- #
class KMedias:
    def __init__(self) -> None:
        self.__dataframe = pd.DataFrame()

    def setDataFrame(self, dataframe):
        # Verifica si dataframe es algo diferente a lo esperado
        if not isinstance(dataframe, pd.core.frame.DataFrame):
            raise ValueError("\nNo se ingresó un DataFrame.")
        self.__dataframe = dataframe

    def __verificador_columnas(self, columnas):
        # Verifica que columnas sea una lista y contenga más de 2 elementos
        if not isinstance(columnas, list) or len(columnas) < 2:
            raise ValueError("Debe ingresar una lista con al menos dos" +
                             " nombres de columnas.")

        # Verifica que todas las columnas en la lista sean cadenas de texto
        for col in columnas:
            if not isinstance(col, str):
                raise ValueError("Cada nombre de columna debe ser una" +
                                 "cadena de texto.")

        # Verificar que todas las columnas existan dentro del DataFrame
        for col in columnas:
            if col not in self.__dataframe.columns:
                raise ValueError(f"La columna {col} no existe dentro del" +
                                 "DataFrame.")

    def metodo_elbow(self, columnas):
        self.__verificador_columnas(columnas)

        # Se seleccionan las columnas que se quieren utilizar
        data = self.__dataframe[columnas]

        # Procesamiento de los datos, para crear un ajuste multidimensional
        scaler = StandardScaler()                   # Crea un objeto
        scaler_data = scaler.fit_transform(data)    # Entrena los datos

        # Selección del número de clusters usando el método Elbow
        inercia = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaler_data)
            inercia.append(kmeans.inertia_)

        # Graficar el Método del Codo
        plt.plot(range(1, 11), inercia, marker='o')
        plt.title('Método del Codo para Selección de k')
        plt.xlabel('Número de Clusters (k)')
        plt.ylabel('Inercia')
        plt.show()

    def grafica_KMeans(self, colum1, colum2, xlabel, ylabel, k_clusters):
        columnas = [colum1, colum2]
        self.__verificador_columnas(columnas)

        # Verifica que el número de clusters sea permitido
        if not isinstance(k_clusters, int):
            raise ValueError("El número de clusters debe ser entero.")
        if k_clusters < 1:
            raise ValueError("El número de clusters debe ser mayor a 1.")

        # Se selecciona las dos columas que se quieren utilizar.
        data = self.__dataframe[[colum1, colum2]]

        # n_init inicializa 10 veces Kmeans con semillas aleatorias
        # nuevo de clusters decidido por k_clusters
        kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)

        # Se crea una nueva columna con el nombre de "clusters_kmeans" con los
        # datos del entrenamiento de predicción del kmeans (configurado)
        self.__dataframe['cluster_kmeans'] = kmeans.fit_predict(data)

        # Graficar el KMeans
        plt.scatter(self.__dataframe[colum1], self.__dataframe[colum2],
                    c=self.__dataframe['cluster_kmeans'],
                    cmap='viridis', marker='.')
        plt.title('Clusters usando K-means')
        plt.xlabel(str(xlabel))
        plt.ylabel(str(ylabel))
        plt.show()

    def grafica_KMeans_3D(self, colum1, colum2, colum3, xlabel, ylabel,
                          zlabel, k_clusters):
        columnas = [colum1, colum2, colum3]
        self.__verificador_columnas(columnas)

        if not isinstance(k_clusters, int):
            raise ValueError("El número de clusters debe ser entero.")
        if k_clusters < 1:
            raise ValueError("El número de clusters debe ser mayor a 1.")

        # Se seleccionan las tres columnas que se quieren utilizar.
        data = self.__dataframe[[colum1, colum2, colum3]]

        # Realiza KMeans
        kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
        self.__dataframe['cluster_kmeans'] = kmeans.fit_predict(data)

        # Graficar en 3D
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.__dataframe[colum1], self.__dataframe[colum2],
                   self.__dataframe[colum3],
                   c=self.__dataframe['cluster_kmeans'],
                   cmap='viridis', marker='o')

        ax.set_title('Clusters usando K-means en 3D')
        ax.set_xlabel(str(xlabel))
        ax.set_ylabel(str(ylabel))
        ax.set_zlabel(str(zlabel))
        plt.show()
