import fastf1
import os

def crear_cache(cache_path):
    os.makedirs(cache_path, exist_ok=True)
    fastf1.Cache.enable_cache(cache_path)

def listar_gps(year):
    schedule = fastf1.get_event_schedule(year)
    print(f"GPs disponibles para la temporada {year}:")
    for i, row in schedule.iterrows():
        print(f"{i+1:2d}. {row['EventName']} (código: '{row['Event']}', fecha: {row['Date'].date()})")

def descargar_gp(year, gp_code, session_type='R'):
    data_dir = f"gp_data/{gp_code.lower()}_{year}"
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, f"{gp_code.lower()}_{year}.csv")

    print(f"Descargando datos del GP {gp_code} {year} sesión {session_type}...")

    session = fastf1.get_session(year, gp_code, session_type)
    session.load()

    laps = session.laps
    if laps.empty:
        print("No se encontraron datos de vueltas.")
        return

    laps.to_csv(csv_path, index=False)
    print(f"Datos guardados en: {csv_path}")

def main():
    year = int(input("Ingrese el año de la temporada (ej. 2025): "))
    cache_path = 'cache'
    crear_cache(cache_path)

    listar_gps(year)

    gp_code = input("Ingrese el código exacto del GP a descargar (ej. 'Australia'): ").strip()
    descargar_gp(year, gp_code)

if __name__ == "__main__":
    main()
