#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot mean zonal divergence"

import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from mpl_toolkits.basemap import Basemap
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

latlon = [-85.5, -47, 8, 27.5]

path = '/home/netapp-clima-users/users/jsalinas/ERA5_data/UV_PRIMA/UV_PRIMA925' # Path

subdomains = {
    ".": (13, 16,  289, 284),}


def import_data(exp):

	ds = xr.open_dataset('{0}/grad_meridional-{1}.nc'.format(path, exp))
	lats = ds['latitude']
	lons = ds['longitude']
	uwnd = ds['u']

	return lats, lons, uwnd

lats, lons, uwnd_jun_jul_80_17_act = import_data('jun-jul_act')
lats, lons, uwnd_ago_oct_80_17_act = import_data('ago-oct_act')
lats, lons, uwnd_jun_jul_82_16_ina = import_data('jun-jul_ina')
lats, lons, uwnd_ago_oct_82_16_ina = import_data('ago-oct_ina')
lats, lons, uwnd_jun_jul_diff = import_data('jun-jul_diff')
lats, lons, uwnd_ago_oct_diff = import_data('ago-oct_diff')


# uwnd_diff
mi2= -.00001
md2= .00001

mi= -.00001
md= .00001

# Plot figure
mp = Basemap(projection='merc', llcrnrlon=274.5, llcrnrlat=8, urcrnrlon=313, urcrnrlat=27.5, resolution = 'i')
lon, lat = np.meshgrid(lons,lats)  #this converts coordinates into 2D arrray
x,y = mp(lon,lat) #mapping them together 

fig = plt.figure(figsize=(13.5,5)) #figure size 

ax = fig.add_subplot(2, 3, 1)
data1 = uwnd_jun_jul_80_17_act.squeeze()  # elimina dimensiones de 1
c_scheme = mp.pcolormesh(x, y, -data1, cmap='bwr', vmin=mi, vmax=md)
Z = uwnd_jun_jul_80_17_act.values
Z = np.squeeze(Z)
mp.contour(x, y, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(a) Jun-Jul Active')
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
data2 = uwnd_jun_jul_82_16_ina.squeeze()  # elimina dimensiones de 1
c_scheme = mp.pcolormesh(x, y,-data2,cmap='bwr', vmin=mi, vmax=md)
Z = uwnd_jun_jul_82_16_ina.values
Z = np.squeeze(Z)
mp.contour(x, y, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(b) Jun-Jul Inactive')
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

ax = fig.add_subplot(2, 3, 3)
data3 = uwnd_jun_jul_diff.squeeze()  # elimina dimensiones de 1
c_scheme = mp.pcolormesh(x, y,-data3,cmap='bwr',vmin=mi, vmax=md)
Z = uwnd_jun_jul_diff.values
Z = np.squeeze(Z)
mp.contour(x, y, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
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
data4 = uwnd_ago_oct_80_17_act.squeeze()  # elimina dimensiones de 1
c_scheme = mp.pcolormesh(x, y,-data4,cmap='bwr',vmin=mi, vmax=md)
Z = uwnd_ago_oct_80_17_act.values
Z = np.squeeze(Z)
mp.contour(x, y, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(d) Aug-Oct Active')
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
data5 = uwnd_ago_oct_82_16_ina.squeeze()  # elimina dimensiones de 1
c_scheme = mp.pcolormesh(x, y,-data5,cmap='bwr',vmin=mi, vmax=md)
Z = uwnd_ago_oct_82_16_ina.values
Z = np.squeeze(Z)
mp.contour(x, y, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(e) Aug-Oct Inactive')
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
data6 = uwnd_ago_oct_diff.squeeze()  # elimina dimensiones de 1
c_scheme = mp.pcolormesh(x, y, -data6,cmap='bwr',vmin=mi, vmax=md)
Z = uwnd_ago_oct_diff.values
Z = np.squeeze(Z)
mp.contour(x, y, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(f) Difference.')
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

plt.savefig('figs/UV_PRIMA-subplots-act-ina_925.png', dpi=400, bbox_inches="tight")
plt.show()
exit()

