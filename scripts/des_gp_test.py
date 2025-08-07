import fastf1
import pandas as pd
import os
from datetime import datetime

fastf1.Cache.enable_cache('cache')


def normalizar_nombre_gp(nombre):
    return nombre.lower().replace(' ', '_')


def crear_estructura_directorios(nombre_gp, año):
    base_path = f'gp_data/{nombre_gp}_{año}'
    subdirs = ['raw', 'processed', 'figures']
    for sub in subdirs:
        os.makedirs(os.path.join(base_path, sub), exist_ok=True)
    return base_path


def descargar_datos_gp(año, gp_nombre):
    print(f"\nDescargando datos del GP de {gp_nombre} ({año})")
    session = fastf1.get_session(año, gp_nombre, 'R')
    session.load()
    laps = session.laps

    gp_id = normalizar_nombre_gp(gp_nombre)
    ruta_base = crear_estructura_directorios(gp_id, año)

    ruta_csv = os.path.join(ruta_base, 'raw', 'vueltas_crudas.csv')
    laps.to_csv(ruta_csv, index=False)
    print(f"✅ Datos guardados en: {ruta_csv}")


def mostrar_gps_disponibles(año):
    print(f"\n🔎 Obteniendo eventos de la temporada {año}...")
    schedule = fastf1.get_event_schedule(año)
    hoy = pd.Timestamp(datetime.today())
    eventos_pasados = schedule[schedule['EventDate'] <= hoy]

    if eventos_pasados.empty:
        print("❌ No hay eventos pasados todavía para este año.")
        return None

    print(f"\nGPs disponibles hasta hoy ({hoy.date()}):\n")
    for _, row in eventos_pasados.iterrows():
        print(f"- {row['EventName']}")

    return eventos_pasados['EventName'].tolist()


if __name__ == '__main__':
    try:
        año = int(input("Ingrese el año de la temporada (ej. 2025): "))
        gps_disponibles = mostrar_gps_disponibles(año)

        if not gps_disponibles:
            exit()

        gp_nombre = input("\nIngrese el nombre EXACTO del GP (como aparece arriba): ")
        if gp_nombre not in gps_disponibles:
            print("❌ El GP ingresado no está en la lista de eventos disponibles.")
        else:
            descargar_datos_gp(año, gp_nombre)

    except Exception as e:
        print(f"⚠️ Error: {e}")

