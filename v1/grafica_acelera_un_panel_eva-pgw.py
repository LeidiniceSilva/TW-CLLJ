#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot zonal difference at 925 hPa"

import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

from mpl_toolkits.basemap import Basemap
from scipy.ndimage import gaussian_filter
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


latlon = [-85.5, -47, 8, 27.5]

#grad_meridional-jun-jul_eva_925.nc
#grad_meridional-ago-oct_pgw_925.nc
#grad_meridional-jun-jul_diff_925.nc
path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo'

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(exp):
        ds = xr.open_dataset('{0}/pprom-acelera_ua925_{1}.nc'.format(path, exp))
	# print(ds)

        lats = ds['lat']
        lons = ds['lon']
        time = ds.variables['time'][:]
        uwnd = ds['ua925']

        return lats, lons, uwnd

lats, lons, uwnd_jun_jul_80_17_eva_925 = import_data('jun-jul_eva')
lats, lons, uwnd_ago_oct_80_17_eva_925 = import_data('ago-oct_eva')
lats, lons, uwnd_jun_jul_82_16_pgw_925 = import_data('jun-jul_pgw')
lats, lons, uwnd_ago_oct_82_16_pgw_925 = import_data('ago-oct_pgw')
lats, lons, uwnd_jun_jul_diff_925 = import_data('jun-jul_diff')
lats, lons, uwnd_ago_oct_diff_925 = import_data('ago-oct_diff')


# uwnd_diff_925
mi2= -.00001
md2= .00001

mi= -.000025
md= .000025

#########lon = lons.values        # (y, x)
#########lat = lats.values        # (y, x)

# Plot figure
# Definiendo el mapa
mp = Basemap(projection='merc', llcrnrlon=-85.5, llcrnrlat=8, urcrnrlon=-47, urcrnrlat=27.5, resolution = 'i')
x,y = mp(lons,lats) #mapping them together 

fig = plt.figure(figsize=(13.5,5)) #figure size 

ax = fig.add_subplot(2, 3, 1)

data1 = uwnd_jun_jul_80_17_eva_925.squeeze()  # elimpgw_925 dimensiones de 1
lon = np.array(x)
lat = np.array(y)
Z = uwnd_jun_jul_80_17_eva_925.values
sigma = 3  # controla suavidad, prueba 1-3
Z_smooth = gaussian_filter(Z, sigma=sigma)
Z_smooth = Z_smooth.squeeze()
c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap='bwr',vmin=mi, vmax=md)
# contorno en nivel cero
eps = 0.2e-6  # ajusta según la magnitud de tus datos
mp.contour(lon, lat, Z_smooth, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
mp.contour(lon, lat, Z_smooth, levels=[-.0000001],colors='k', linewidths=0.4,linestyles='solid')


#####PRUEBA#c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_eva_925[:,:]), cmap='jet', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year
plt.title('(a) Jun-Jul Evaluation')
#lt.ylabel('Latitude')
#mp.drawmeridians(np.arange(urcrnrlon, llcrnrlon, 20), size=6, labels=[0,0,0,1], linewidth=0.4, color='black')
#mp.drawparallels()
mp.drawcoastlines()
mp.drawstates()
mp.drawcountries()

cbar = mp.colorbar(c_scheme,location='right',pad = '2%') # map information
cbar.ax.tick_params(labelsize=6)

mp.drawmeridians(
    np.arange(-90, -40, 10),
    labels=[0, 0, 0, 1],
    fontsize=6,
    linewidth=0.1
)

mp.drawparallels(
    np.arange(0, 30, 5),
    labels=[1, 0, 0, 0],
    fontsize=6,
    linewidth=0.1
)

# Draw red boxes for subdomains
for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
    lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
    lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

    x_box, y_box = mp(lons_box, lats_box)

    ax.plot(x_box, y_box, color='black', linewidth=0.5)

    x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
    ax.text(x_txt, y_txt, name,
            color='black', fontsize=1,
            bbox=dict(facecolor='none', edgecolor='none'))


#################################################



ax = fig.add_subplot(2, 3, 2)

data2 = uwnd_jun_jul_82_16_pgw_925.squeeze()  # elimpgw_925 dimensiones de 1

#c_scheme = mp.pcolormesh(x, y,data2,cmap='jet',vmin=mi, vmax=md)

lon = np.array(x)
lat = np.array(y)
Z = uwnd_jun_jul_82_16_pgw_925.values
sigma = 3  # controla suavidad, prueba 1-3
Z_smooth = gaussian_filter(Z, sigma=sigma)
Z_smooth = Z_smooth.squeeze()
c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap='bwr',vmin=mi, vmax=md)
# contorno en nivel cero
eps = 0.2e-6  # ajusta según la magnitud de tus datos
mp.contour(lon, lat, Z_smooth, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
mp.contour(lon, lat, Z_smooth, levels=[-.0000001],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(b) Jun-Jul PGW')
mp.drawcoastlines()
mp.drawstates()
mp.drawcountries()

cbar = mp.colorbar(c_scheme,location='right',pad = '2%') # map information
cbar.ax.tick_params(labelsize=6)

mp.drawmeridians(
    np.arange(-90, -40, 10),
    labels=[0, 0, 0, 1],
    fontsize=6,
    linewidth=0.1
)

mp.drawparallels(
    np.arange(0, 30, 5),
    labels=[1, 0, 0, 0],
    fontsize=6,
    linewidth=0.1
)

# Draw red boxes for subdomains
for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
    lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
    lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

    x_box, y_box = mp(lons_box, lats_box)

    ax.plot(x_box, y_box, color='black', linewidth=0.5)

    x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
    ax.text(x_txt, y_txt, name,
            color='black', fontsize=1,
            bbox=dict(facecolor='none', edgecolor='none'))


#################################################



ax = fig.add_subplot(2, 3, 3)

data3 = uwnd_jun_jul_diff_925.squeeze()  # elimpgw_925 dimensiones de 1

#c_scheme = mp.pcolormesh(x, y,data3,cmap='jet',vmin=mi, vmax=md)

lon = np.array(x)
lat = np.array(y)
Z = uwnd_jun_jul_diff_925.values
sigma = 3  # controla suavidad, prueba 1-3
Z_smooth = gaussian_filter(Z, sigma=sigma)
Z_smooth = Z_smooth.squeeze()
c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap='bwr',vmin=mi2, vmax=md2)
# contorno en nivel cero
eps = 0.2e-6  # ajusta según la magnitud de tus datos
mp.contour(lon, lat, Z_smooth, levels=[0],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(c) Difference')
mp.drawcoastlines()
mp.drawstates()
mp.drawcountries()

cbar = mp.colorbar(c_scheme,location='right',pad = '2%') # map information
cbar.ax.tick_params(labelsize=6)

mp.drawmeridians(
    np.arange(-90, -40, 10),
    labels=[0, 0, 0, 1],
    fontsize=6,
    linewidth=0.1
)

mp.drawparallels(
    np.arange(0, 30, 5),
    labels=[1, 0, 0, 0],
    fontsize=6,
    linewidth=0.1
)

# Draw red boxes for subdomains
for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
    lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
    lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

    x_box, y_box = mp(lons_box, lats_box)

    ax.plot(x_box, y_box, color='black', linewidth=0.5)

    x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
    ax.text(x_txt, y_txt, name,
            color='black', fontsize=1,
            bbox=dict(facecolor='none', edgecolor='none'))


#################################################



ax = fig.add_subplot(2, 3, 4)

data4 = uwnd_ago_oct_80_17_eva_925.squeeze()  # elimpgw_925 dimensiones de 1

#c_scheme = mp.pcolormesh(x, y,data4,cmap='jet',vmin=mi, vmax=md)

lon = np.array(x)
lat = np.array(y)
Z = uwnd_ago_oct_80_17_eva_925.values
sigma = 3  # controla suavidad, prueba 1-3
Z_smooth = gaussian_filter(Z, sigma=sigma)
Z_smooth = Z_smooth.squeeze()
c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap='bwr',vmin=mi, vmax=md)
# contorno en nivel cero
eps = 0.2e-6  # ajusta según la magnitud de tus datos
mp.contour(lon, lat, Z_smooth, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
mp.contour(lon, lat, Z_smooth, levels=[.0000001],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(d) Aug-Oct Evaluation')
#lt.ylabel('Latitude')
#lt.xlabel('Longitude')
mp.drawcoastlines()
mp.drawstates()
mp.drawcountries()

cbar = mp.colorbar(c_scheme,location='right',pad = '2%') # map information
cbar.ax.tick_params(labelsize=6)

mp.drawmeridians(
    np.arange(-90, -40, 10),
    labels=[0, 0, 0, 1],
    fontsize=6,
    linewidth=0.1
)

mp.drawparallels(
    np.arange(0, 30, 5),
    labels=[1, 0, 0, 0],
    fontsize=6,
    linewidth=0.1
)

# Draw red boxes for subdomains
for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
    lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
    lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

    x_box, y_box = mp(lons_box, lats_box)

    ax.plot(x_box, y_box, color='black', linewidth=0.5)

    x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
    ax.text(x_txt, y_txt, name,
            color='black', fontsize=1,
            bbox=dict(facecolor='none', edgecolor='none'))


#################################################



ax = fig.add_subplot(2, 3, 5)

data5 = uwnd_ago_oct_82_16_pgw_925.squeeze()  # elimpgw_925 dimensiones de 1

#c_scheme = mp.pcolormesh(x, y,data5,cmap='jet',vmin=mi, vmax=md)

lon = np.array(x)
lat = np.array(y)
Z = uwnd_ago_oct_82_16_pgw_925.values
sigma = 3  # controla suavidad, prueba 1-3
Z_smooth = gaussian_filter(Z, sigma=sigma)
Z_smooth = Z_smooth.squeeze()
c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap='bwr',vmin=mi, vmax=md)
# contorno en nivel cero
eps = 0.2e-6  # ajusta según la magnitud de tus datos
mp.contour(lon, lat, Z_smooth, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
mp.contour(lon, lat, Z_smooth, levels=[.0000001],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(e) Aug-Oct PGW')
#lt.xlabel('Longitude')
mp.drawcoastlines()
mp.drawstates()
mp.drawcountries()


cbar = mp.colorbar(c_scheme,location='right',pad = '2%') # map information
cbar.ax.tick_params(labelsize=6)

mp.drawmeridians(
    np.arange(-90, -40, 10),
    labels=[0, 0, 0, 1],
    fontsize=6,
    linewidth=0.1
)

mp.drawparallels(
    np.arange(0, 30, 5),
    labels=[1, 0, 0, 0],
    fontsize=6,
    linewidth=0.1
)

# Draw red boxes for subdomains
for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
    lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
    lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

    x_box, y_box = mp(lons_box, lats_box)

    ax.plot(x_box, y_box, color='black', linewidth=0.5)

    x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
    ax.text(x_txt, y_txt, name,
            color='black', fontsize=1,
            bbox=dict(facecolor='none', edgecolor='none'))


#################################################



ax = fig.add_subplot(2, 3, 6)

data6 = uwnd_ago_oct_diff_925.squeeze()  # elimpgw_925 dimensiones de 1

#c_scheme = mp.pcolormesh(x, y,data6,cmap='jet',vmin=mi, vmax=md)

lon = np.array(x)
lat = np.array(y)
Z = uwnd_ago_oct_diff_925.values
sigma = 3  # controla suavidad, prueba 1-3
Z_smooth = gaussian_filter(Z, sigma=sigma)
Z_smooth = Z_smooth.squeeze()
c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap='bwr',vmin=mi2, vmax=md2)
# contorno en nivel cero
eps = 0.2e-6  # ajusta según la magnitud de tus datos
mp.contour(lon, lat, Z_smooth, levels=[0],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(f) Difference')
#lt.xlabel('Longitude')
mp.drawcoastlines()
mp.drawstates()
mp.drawcountries()

cbar = mp.colorbar(c_scheme,location='right',pad = '2%') # map information
cbar.ax.tick_params(labelsize=6)

mp.drawmeridians(
    np.arange(-90, -40, 10),
    labels=[0, 0, 0, 1],
    fontsize=6,
    linewidth=0.1
)

mp.drawparallels(
    np.arange(0, 30, 5),
    labels=[1, 0, 0, 0],
    fontsize=6,
    linewidth=0.1
)

# Draw red boxes for subdomains
for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
    lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
    lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

    x_box, y_box = mp(lons_box, lats_box)

    ax.plot(x_box, y_box, color='black', linewidth=0.5)

    x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
    ax.text(x_txt, y_txt, name,
            color='black', fontsize=1,
            bbox=dict(facecolor='none', edgecolor='none'))

plt.savefig('figs/aacelera-du_dt-subplots-eva_pgw.png', dpi=400, bbox_inches='tight')
plt.show()
exit()

