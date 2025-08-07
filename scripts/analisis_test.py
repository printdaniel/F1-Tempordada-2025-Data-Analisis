import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set_theme(style="darkgrid")
plt.style.use("dark_background")

GP_DIR = "gp_data"

def listar_grandes_premios():
    if not os.path.exists(GP_DIR):
        print("❌ No se encontró el directorio 'gp_data/'. Asegúrate de haber descargado algún GP.")
        return []

    gps = sorted([d for d in os.listdir(GP_DIR) if os.path.isdir(os.path.join(GP_DIR, d))])
    if not gps:
        print("⚠️ No hay GPs disponibles en el directorio 'gp_data/'.")
        return []

    print("\n📁 GPs disponibles en 'gp_data/':\n")
    for idx, gp in enumerate(gps, 1):
        print(f"{idx}. {gp}")
    return gps

def seleccionar_gp(gps):
    while True:
        try:
            seleccion = int(input("\nSelecciona el número del GP que deseas analizar: "))
            if 1 <= seleccion <= len(gps):
                return gps[seleccion - 1]
            else:
                print("❌ Selección inválida.")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")

def cargar_y_filtrar_datos(gp_folder):
    #ruta_csv = os.path.join(GP_DIR, gp_folder, f"{gp_folder}.csv")
    #ruta_csv = os.path.join(GP_DIR, gp_folder, "vueltas_crudas.csv")
    ruta_csv = os.path.join(GP_DIR, gp_folder, "raw", "vueltas_crudas.csv")

    if not os.path.exists(ruta_csv):
        print(f"❌ No se encontró el archivo CSV principal: {ruta_csv}")
        return None, None

    laps = pd.read_csv(ruta_csv)
    race_laps = laps[(laps["Compound"].notna()) & (laps["Stint"] > 0)]
    return race_laps, os.path.join(GP_DIR, gp_folder)

def obtener_colores_por_equipo(race_laps):
    team_colors = {
        'Ferrari': '#DC0000',
        'McLaren': '#FF8700',
        'Mercedes': '#00D2BE',
        'Red Bull': '#1E41FF',
        'Aston Martin': '#006F62',
        'Alpine': '#FF87BC',
        'Williams': '#005AFF',
        'RB': '#6692FF',
        'Kick Sauber': '#52E252',
        'Haas': '#B6BABD',
    }
    driver_team_map = race_laps.groupby("Driver")["Team"].first().to_dict()
    driver_colors = {
        driver: team_colors.get(team, "#000000") for driver, team in driver_team_map.items()
    }
    return driver_colors

def guardar_figura(fig, base_path, nombre_archivo):
    fig_path = os.path.join(base_path, "figures")
    os.makedirs(fig_path, exist_ok=True)
    full_path = os.path.join(fig_path, nombre_archivo)
    fig.savefig(full_path, dpi=300)
    print(f"Guardado gráfico: {full_path}")

def generar_graficos(race_laps, base_path, driver_colors, gp_folder):
    # Extraer nombre y año desde gp_folder
    try:
        gp_name, year = gp_folder.rsplit("_", 1)
    except ValueError:
        gp_name, year = gp_folder, ""

    # Gráfico 1: Violinplot de ritmo de carrera
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.violinplot(
        data=race_laps,
        x='Driver',
        y='LapTime',
        hue='Driver',
        palette=driver_colors,
        color='skyblue',
        inner='quartile',
        legend=False,
        ax=ax
    )
    ax.set_title(f"Ritmo de Carrera - GP {gp_name.title()} {year}", fontsize=14)
    ax.set_ylabel("Tiempo de vuelta (s)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    guardar_figura(fig, base_path, "ritmo_carrera.png")
    plt.close(fig)

    # Gráfico 2: Paradas en boxes
    fig, ax = plt.subplots(figsize=(12, 6))
    pit_data = race_laps[race_laps["PitInTime"].notna()]
    sns.scatterplot(data=pit_data, x="LapNumber", y="Driver", hue="Compound", style="Stint", ax=ax)
    ax.set_title(f"Paradas en Boxes - GP {gp_name.title()} {year}")
    ax.set_xlabel("Vuelta")
    ax.set_ylabel("Piloto")
    plt.tight_layout()
    guardar_figura(fig, base_path, "parada_en_boxes.png")
    plt.close(fig)

    # Gráfico 3: Degradación del ritmo
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=race_laps, x="LapNumber", y="LapTime", hue="Driver", ax=ax)
    ax.set_title(f"Degradación del Ritmo - GP {gp_name.title()} {year}")
    ax.set_ylabel("Tiempo de vuelta (s)")
    ax.set_xlabel("Vuelta")
    plt.tight_layout()
    guardar_figura(fig, base_path, "degradacion_ritmo.png")
    plt.close(fig)

    # Gráfico 4: Estrategia de neumáticos
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.stripplot(
        data=race_laps,
        x="LapNumber",
        y="Driver",
        hue="Compound",
        dodge=True,
        palette="Set2",
        ax=ax
    )
    ax.set_title(f"Estrategia de Neumáticos - GP {gp_name.title()} {year}")
    ax.set_xlabel("Vuelta")
    plt.tight_layout()
    guardar_figura(fig, base_path, "estrategia_neumaticos.png")
    plt.close(fig)

    # Gráfico 5: Evolución de posiciones
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=race_laps, x="LapNumber", y="Position", hue="Driver", palette=driver_colors, ax=ax)
    ax.invert_yaxis()
    ax.set_title(f"Evolución de Posiciones - GP {gp_name.title()} {year}")
    ax.set_xlabel("Vuelta")
    ax.set_ylabel("Posición")
    plt.tight_layout()
    guardar_figura(fig, base_path, "evolucion_posiciones.png")
    plt.close(fig)


if __name__ == '__main__':
    gps_disponibles = listar_grandes_premios()
    if not gps_disponibles:
        exit()

    gp_seleccionado = seleccionar_gp(gps_disponibles)
    race_laps, base_path = cargar_y_filtrar_datos(gp_seleccionado)

    if race_laps is not None:
        driver_colors = obtener_colores_por_equipo(race_laps)
        generar_graficos(race_laps, base_path, driver_colors, gp_seleccionado)

