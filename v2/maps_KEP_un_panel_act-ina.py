#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot KEP"

import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from mpl_toolkits.basemap import Basemap
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

latlon = [-85.5, -47, 8, 27.5]

path = '/home/netapp-clima-users/users/jsalinas/ERA5_data/KEP' # Path

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(exp):

	ds = xr.open_dataset('{0}/prom_ECP700_{1}.nc'.format(path, exp))
	lats = ds.variables['latitude'][:]
	lons = ds.variables['longitude'][:]
	time = ds.variables['time'][:]
	uwnd = ds.variables['u'][:]

	return lats, lons, uwnd


lats, lons, uwnd_jun_jul_80_17_act = import_data('jun-jul_1980-2017_act')
lats, lons, uwnd_ago_oct_80_17_act = import_data('ago-oct_1980-2017_act')
lats, lons, uwnd_jun_jul_82_16_ina = import_data('jun-jul_1982-2016_ina')
lats, lons, uwnd_ago_oct_82_16_ina = import_data('ago-oct_1982-2016_ina')
lats, lons, uwnd_jun_jul_diff = import_data('jun-jul_diff')
lats, lons, uwnd_ago_oct_diff = import_data('ago-oct_diff')

# uwnd_jun_jul_80_17_act
min_height_jun_jul_80_17_act = int(np.min(np.squeeze(uwnd_jun_jul_80_17_act[0,:,:])))
max_height_jun_jul_80_17_act = int(np.max(np.squeeze(uwnd_jun_jul_80_17_act[0,:,:])))

# uwnd_ago_oct_80_17_act
min_height_ago_oct_80_17_act = int(np.min(np.squeeze(uwnd_ago_oct_80_17_act[0,:,:])))
max_height_ago_oct_80_17_act = int(np.max(np.squeeze(uwnd_ago_oct_80_17_act[0,:,:])))

# uwnd_jun_jul_82_16_ina
min_height_jun_jul_82_16_ina = int(np.min(np.squeeze(uwnd_jun_jul_82_16_ina[0,:,:])))
max_height_jun_jul_82_16_ina = int(np.max(np.squeeze(uwnd_jun_jul_82_16_ina[0,:,:])))

min_height_ago_oct_82_16_ina = int(np.min(np.squeeze(uwnd_ago_oct_82_16_ina[0,:,:])))
max_height_ago_oct_82_16_ina = int(np.max(np.squeeze(uwnd_ago_oct_82_16_ina[0,:,:])))

# uwnd_diff
mi2= -2
md2= 2

#mi= 9
#md= 0

mi= 0
md= 9

# Plot figure
# Definiendo el mapa
mp = Basemap(projection='merc', llcrnrlon=-85.5, llcrnrlat=8, urcrnrlon=-47, urcrnrlat=27.5, resolution = 'i')
lon, lat = np.meshgrid(lons,lats)  #this converts coordinates into 2D arrray
x,y = mp(lon,lat) #mapping them together 

fig = plt.figure(figsize=(13.5,5)) #figure size 

ax = fig.add_subplot(2, 3, 1)
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_act[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year
mp.contour(x, y,np.squeeze(uwnd_jun_jul_80_17_act[0, :, :]), levels=[5],colors='k', linewidths=0.4,linestyles='solid')
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
    np.arange(0, 30, 10),
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_82_16_ina[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year

# contorno en nivel cero
mp.contour(x, y,np.squeeze(uwnd_jun_jul_82_16_ina[0, :, :]), levels=[5],colors='k', linewidths=0.4,linestyles='solid')

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
    np.arange(0, 30, 10),
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_diff[0,:,:]), cmap='bwr', vmin=mi2, vmax=md2) # [0,:,:] is for the first day of the year

# contorno en nivel cero
mp.contour(x, y,np.squeeze(uwnd_jun_jul_diff[0, :, :]), levels=[0],colors='k', linewidths=0.4,linestyles='solid')

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
    np.arange(0, 30, 10),
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_80_17_act[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year
mp.contour(x, y,np.squeeze(uwnd_ago_oct_80_17_act[0, :, :]), levels=[5],colors='k', linewidths=0.4,linestyles='solid')
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
    np.arange(0, 30, 10),
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_82_16_ina[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year
mp.contour(x, y,np.squeeze(uwnd_ago_oct_82_16_ina[0, :, :]), levels=[5],colors='k', linewidths=0.4,linestyles='solid')
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
    np.arange(0, 30, 10),
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_diff[0,:,:]), cmap='bwr', vmin=mi2, vmax=md2) # [0,:,:] is for the first day of the year
mp.contour(x, y,np.squeeze(uwnd_ago_oct_diff[0, :, :]), levels=[0],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(f) Difference')
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
    np.arange(0, 30, 10),
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

plt.savefig('figs/KEP-subplots-act-ina.png', dpi=400, bbox_inches='tight')
plt.show()
exit()

