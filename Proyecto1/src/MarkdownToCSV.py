# --------------------- # Clase solicitada a ChatGPT # ---------------------- #
# ---------------- # Se importan las librerías necesarias # ----------------- #
import pandas as pd


# ------------ # Clase para convertir archivos markdown a CSV # ------------- #
class MarkdownToCSV:

    def __init__(self, file_path):
        self.file_path = file_path  # Almacena la ruta del archivo
        self.df = None  # Inicializa el DataFrame como None

    # -------------------- # Leer el archivo markdown # --------------------- #
    def read_markdown(self):
        # Imprime un mensaje indicando que intentará abrir el archivo
        print(f"Intentando abrir markdown: {self.file_path}")
        try:
            # Abre el archivo en modo de lectura con codificación UTF-8
            with open(self.file_path, 'r', encoding='utf-8') as file:
                # Lee todas las líneas del archivo y las almacena en una lista
                lines = file.readlines()
        except UnicodeDecodeError:  # Captura cualquier error de codificación
            print("Failed to read the file due to encoding issues." +
                  " Please check the file encoding.")
            return None  # Devuelve None si ocurre un error

        return lines  # Devuelve las líneas leídas del archivo

    # ------------------ # Extraer la tabla del markdown # ------------------ #
    def extract_table(self, lines):
        if lines is None:  # Si no se leyeron líneas, devuelve None
            print("No lines to process, returning None.")
            return None

        # Filtra las líneas que contienen '|' (partes de la tabla) y
        # elimina los espacios adicionales
        table_lines = [line.strip() for line in lines if '|' in line]
        # Extrae los datos de la tabla, eliminando los espacios adicionales
        # y reemplazando comas por puntos
        table_data = []
        for line in table_lines[2:]:
            cells = line.split('|')[1:-1]
            clean_cells = [cell.strip().replace(',', '.') for cell in cells]
            table_data.append(clean_cells)

        # Extrae y limpia los nombres de las columnas desde la primera línea
        # de la tabla
        columns = [col.strip() for col in table_lines[0].split('|')[1:-1]]
        # Crea un DataFrame con los datos extraídos
        self.df = pd.DataFrame(table_data, columns=columns)
        return self.df  # Devuelve el DataFrame creado

    # ------------ # Guardar el DataFrame como un archivo CSV # ------------- #
    def save_csv(self):
        if self.df is None:  # Verifica si el DataFrame es None
            print("DataFrame is None, cannot save to CSV.")
            return None  # Devuelve None si no hay DataFrame para guardar

        # Reemplaza la extensión del archivo de .md a .csv
        output_csv = self.file_path.replace(".md", ".csv")
        # Guarda el DataFrame en un archivo CSV
        self.df.to_csv(output_csv, index=False)
        # Imprime la ubicación donde se guardó el CSV
        print(f"CSV saved to: {output_csv}")
        return output_csv  # Devuelve la ruta del archivo CSV generado

    # ----------------- # Proceso completo de conversión # ------------------ #
    def convert(self):
        # Lee el archivo markdown
        lines = self.read_markdown()
        # Extrae la tabla desde las líneas leídas
        self.extract_table(lines)
        # Guarda el contenido como CSV y devuelve la ruta del
        # archivo CSV generado
        return self.save_csv()
