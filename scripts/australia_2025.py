import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configurar estilo oscuro de seaborn
sns.set_theme(style="darkgrid")

# Ruta al archivo CSV del GP de Australia 2025
DATA_PATH = "gp_data/australia_2025/australia_2025.csv"

# Verificar existencia del archivo
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"No se encontró el archivo de datos: {DATA_PATH}")

# Cargar datos
laps = pd.read_csv(DATA_PATH)

# Filtrar solo vueltas de carrera y eliminar datos atípicos
race_laps = laps[(laps["Compound"].notna()) & (laps["Stint"] > 0)]

# Colores por equipo
team_colors = {
    'Ferrari': '#DC0000',        # rojo
    'McLaren': '#FF8700',        # papaya
    'Mercedes': '#00D2BE',       # turquesa
    'Red Bull': '#1E41FF',       # azul
    'Aston Martin': '#006F62',   # verde
    'Alpine': '#FF87BC',         # rosado
    'Williams': '#005AFF',       # azul claro
    'RB': '#6692FF',             # azul pastel
    'Kick Sauber': '#52E252',    # verde lima
    'Haas': '#B6BABD',           # gris claro
}

# Crear un mapeo de piloto a equipo usando los datos de vueltas
driver_team_map = race_laps.groupby("Driver")["Team"].first().to_dict()

# Luego usarlo para asignar colores
driver_colors = {
    driver: team_colors.get(team, "#000000")  # negro por defecto.
    for driver, team in driver_team_map.items()
}


# === Gráfico 1: Violinplot de ritmo de carrera ===
# Estilo oscuro
plt.style.use("dark_background")
sns.set_style("darkgrid")

sns.violinplot(
    data=race_laps,
    x='Driver',
    y='LapTime',
    hue='Driver',  # Para que use 'palette'
    palette=driver_colors,
    color='skyblue',
    inner='quartile',
    legend=False  # Si no querés leyenda duplicada
    )

plt.title("Ritmo de Carrera - GP Australia 2025", fontsize=14)
plt.ylabel("Tiempo de vuelta (s)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/figures/ritmo_carrera_aus2025.png", dpi=300)
plt.show()

# === Gráfico 2: Paradas en boxes ===
# pit_data = race_laps[race_laps["PitInTime"].notna()]
# plt.figure(figsize=(12, 6))
# sns.scatterplot(data=pit_data, x="LapNumber", y="Driver", hue="Compound", style="Stint")
# plt.title("Paradas en Boxes - GP Australia 2025")
# plt.xlabel("Vuelta")
# plt.ylabel("Piloto")
# plt.legend(title="Neumático")
# plt.tight_layout()
# plt.savefig("output/figures/ritmo_carrera_australia_2025.png")
# plt.show()
#
# # === Gráfico 3: Estrategia de neumáticos ===
# strategy = race_laps.groupby(["Driver", "Compound"]).size().reset_index(name="Vueltas")
# plt.figure(figsize=(12, 6))
# sns.barplot(data=strategy, x="Driver", y="Vueltas", hue="Compound")
# plt.title("Estrategia de Neumáticos - GP Australia 2025")
# plt.ylabel("Número de vueltas")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
#
# # === Gráfico 4: Degradación del ritmo ===
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=race_laps, x="LapNumber", y="LapTime", hue="Driver")
# plt.title("Degradación del Ritmo - GP Australia 2025")
# plt.ylabel("Tiempo de vuelta (s)")
# plt.xlabel("Vuelta")
# plt.tight_layout()
# plt.show()
#
# # === Gráfico 5: Velocidades máximas ===
# # Asegurarse de que exista la columna TopSpeed
# if "TopSpeed" in race_laps.columns:
#     top_speeds = race_laps.groupby("Driver")["TopSpeed"].max().reset_index()
#     plt.figure(figsize=(12, 6))
#     sns.barplot(data=top_speeds, x="Driver", y="TopSpeed")
#     plt.title("Velocidades Máximas - GP Australia 2025")
#     plt.ylabel("Velocidad (km/h)")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()
# else:
#     print("Advertencia: No se encontró la columna 'TopSpeed' en los datos.")
#
