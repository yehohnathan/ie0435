# Makefile para el Proyecto 1: Sistemas de Agrupamiento

# Detectar el sistema operativo
ifeq ($(OS),Windows_NT)
    # Comandos para Windows
    PYTHON = py  # Cambiar a 'py' en lugar de 'python'
    RM = del /Q
    RMDIR = rmdir /Q /S
else
    # Comandos para Linux (ajustar según sea necesario)
    PYTHON = python3
    RM = rm -f
    RMDIR = rm -rf
endif

# Directorios
SRC_DIR = src

# Archivos
MAIN_FILE = main.py

# Objetivo por defecto
all: run

# Compilar y ejecutar el programa
run:
	$(PYTHON) $(SRC_DIR)/$(MAIN_FILE)

# Limpiar __pycache__
clean:
	$(RM) $(SRC_DIR)/__pycache__/*.pyc
	$(RMDIR) $(SRC_DIR)/__pycache__
