import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import time

class Xorshift():
    # El maximo se debe utilizar para limitar el tamaño del int en python
    max = 2**64
    seed = time.time_ns() % max

    def __xorshift__(self) -> int:
        x = self.seed
        x = x ^ (x << 13) % self.max
        x = x ^ (x >> 7) % self.max
        x = x ^ (x << 17) % self.max
        self.seed = x
        return x

    def rand(self, number, betweenZeroAndOne: bool):
        x = []
        for i in range(number):
            if(betweenZeroAndOne):
                x.append(self.__xorshift__()/self.max)
            else:
                x.append(self.__xorshift__())
        return x

#Generación del mapa a partir del archivo .json:
path = 'caba_barrios.json'
map_data = gpd.read_file(path)

#Generación de puntos aleatorios:
LAT_MIN = -34.725
LAT_MAX = -34.500
LONG_MIN = -58.550
LONG_MAX = -58.325
N_POINTS = 1000

xorshift = Xorshift()
lat = xorshift.rand(N_POINTS, True)
long = xorshift.rand(N_POINTS, True)
random_lat = np.array([(LAT_MAX - LAT_MIN) * n + LAT_MIN for n in lat])
random_long = np.array([(LONG_MAX - LONG_MIN) * n + LONG_MIN for n in long])

map_points = pd.DataFrame()
map_points['longitud'] = random_long
map_points['latitud'] = random_lat

new_points_list = [[], []]

#Se recorren todos los polígonos (barrios) para determinar
#si los puntos de map_points se encuentran en el mapa
for poly_index in map_data.index:
    poly = map_data.loc[poly_index, 'geometry']
    new_points = map_points[map_points.apply(lambda row: poly.contains(Point(row.longitud, row.latitud)), axis=1)]
    points_list = new_points.to_numpy().transpose().tolist()
    new_points_list[0] += points_list[0] 
    new_points_list[1] += points_list[1]

inside_points = pd.DataFrame()
inside_points['longitud'] = new_points_list[0]
inside_points['latitud'] = new_points_list[1]

#MAPA CON LOS PUNTOS:

fig, ax = plt.subplots(figsize=(20, 20))
 
ax.set_title('Ciudad Autónoma de Bs As', 
             pad = 5, 
             fontdict={'fontsize':20, 'color': '#4873ab'})
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

inside_points.plot('longitud', 'latitud', kind="scatter", color = "red", ax=ax, zorder=1)
map_data.plot(ax=ax, zorder=0)
plt.show()