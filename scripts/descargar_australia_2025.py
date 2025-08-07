# scripts/descargar_australia_2025.py
import fastf1
import os


def listar_gps(year):
    schedule = fastf1.get_event_schedule(year)
    print(f"Calendario F1 {year}:")
    for i, row in schedule.iterrows():
        print(f"{i+1}. {row['EventName']} (nombre para usar: '{row['Event']}' )")
    return schedule

def descargar_gp(year, gp, session_type='R'):
    DATA_DIR = f"gp_data/{gp.lower().replace(' ', '_')}_{year}"
    CSV_PATH = f"{DATA_DIR}/{gp.lower().replace(' ', '_')}_{year}.csv"

    import os
    os.makedirs(DATA_DIR, exist_ok=True)
    fastf1.Cache.enable_cache('cache')

    print(f"Descargando datos del GP de {gp} {year}...")
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    laps = session.laps
    if laps.empty:
        print("No se encontraron datos de vueltas.")
    else:
        laps.to_csv(CSV_PATH, index=False)
        print(f"Datos guardados exitosamente en: {CSV_PATH}")

if __name__ == "__main__":
    year = 2025
    schedule = listar_gps(year)
    gp_input = input("Ingresa el nombre exacto del GP (campo 'Event') para descargar: ")
    descargar_gp(year, gp_input)
