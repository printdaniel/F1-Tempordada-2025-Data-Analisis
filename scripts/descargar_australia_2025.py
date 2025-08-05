# scripts/descargar_australia_2025.py

import fastf1
import os
import pandas as pd

# Configuración
year = 2025
gp = "Australia"
session_type = "R"  # Carrera
DATA_DIR = "gp_data/australia_2025"
CSV_PATH = os.path.join(DATA_DIR, "australia_2025.csv")

# Crear directorio si no existe
os.makedirs(DATA_DIR, exist_ok=True)

# Habilitar caché de FastF1
fastf1.Cache.enable_cache('cache')  # Asegúrate de tener una carpeta `cache/`

# Cargar sesión
print(f"Descargando datos del GP de {gp} {year}...")
session = fastf1.get_session(year, gp, session_type)
session.load()

laps = session.laps
if laps.empty:
    print("No se encontraron datos de vueltas.")
else:
    # Guardar a CSV
    laps.to_csv(CSV_PATH, index=False)
    print(f"Datos guardados exitosamente en: {CSV_PATH}")

