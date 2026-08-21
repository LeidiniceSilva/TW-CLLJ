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

path = '/home/netapp-clima-users/users/jsalinas/CCC/ERA5' # Path
#ds = /home/netapp-clima-users/users/jsalinas/CCC/ERA5/prom_ua925_jun-jul_1982-2016_ina.nc

# Subdomains (lat_min, lat_max, lon_min, lon_max)
subdomains = {
    ".": (13, 16,  -71, -76),}


path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/KEP' # Path
#ds = /home/netapp-clima-users/users/jsalinas/CCC/ERA5/prom_ua925_jun-jul_1982-2016_pgw.nc

def import_data(exp):

#	ds = xr.open_dataset('{0}/prom_ua925_{1}.nc'.format(path, exp))
	ds = xr.open_dataset('{0}/prom_ECP700_{1}.nc'.format(path, exp))
#	print(ds)

	lats = ds.variables['lat'][:]
	lons = ds.variables['lon'][:]
	time = ds.variables['time'][:]
	uwnd = ds.variables['ua700'][:]

	return lats, lons, uwnd


lats, lons, uwnd_jun_jul_80_17_eva = import_data('jun-jul_1980-2017_eva')
lats, lons, uwnd_ago_oct_80_17_eva = import_data('ago-oct_1980-2017_eva')
lats, lons, uwnd_jun_jul_80_17_pgw = import_data('jun-jul_1980-2017_pgw')
lats, lons, uwnd_ago_oct_80_17_pgw = import_data('ago-oct_1980-2017_pgw')
lats, lons, uwnd_jun_jul_diff = import_data('jun-jul_diff')
lats, lons, uwnd_ago_oct_diff = import_data('ago-oct_diff')

# uwnd_jun_jul_80_17_eva
min_height_jun_jul_80_17_eva = int(np.min(np.squeeze(uwnd_jun_jul_80_17_eva[0,:,:])))
max_height_jun_jul_80_17_eva = int(np.max(np.squeeze(uwnd_jun_jul_80_17_eva[0,:,:])))

# uwnd_ago_oct_80_17_eva
min_height_ago_oct_80_17_eva = int(np.min(np.squeeze(uwnd_ago_oct_80_17_eva[0,:,:])))
max_height_ago_oct_80_17_eva = int(np.max(np.squeeze(uwnd_ago_oct_80_17_eva[0,:,:])))

# uwnd_jun_jul_82_16_pgw
min_height_jun_jul_80_17_pgw = int(np.min(np.squeeze(uwnd_jun_jul_80_17_pgw[0,:,:])))
max_height_jun_jul_80_17_pgw = int(np.max(np.squeeze(uwnd_jun_jul_80_17_pgw[0,:,:])))

min_height_ago_oct_80_17_pgw = int(np.min(np.squeeze(uwnd_ago_oct_80_17_pgw[0,:,:])))
max_height_ago_oct_80_17_pgw = int(np.max(np.squeeze(uwnd_ago_oct_80_17_pgw[0,:,:])))

# uwnd_diff
mi2= -2
md2= 2

mi= 9
md= 0

# Plot figure
mp = Basemap(projection='merc', llcrnrlon=-85.5, llcrnrlat=8, urcrnrlon=-47, urcrnrlat=27.5, resolution = 'i')
x,y = mp(lons,lats) #mapping them together 

fig = plt.figure(figsize=(13.5,5)) #figure size 

ax = fig.add_subplot(2, 3, 1)
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_eva[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year
lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_jun_jul_80_17_eva[0, :, :]))
mp.contour(lon, lat, Z, levels=[5],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(a) Jun-Jul Evaluation')
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_pgw[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year
lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_jun_jul_80_17_pgw[0, :, :]))
mp.contour(lon, lat, Z, levels=[5],colors='k', linewidths=0.4,linestyles='solid')
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

lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_jun_jul_diff[0, :, :]))
# contorno en nivel cero
mp.contour(lon, lat, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')

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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_80_17_eva[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year

lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_ago_oct_80_17_eva[0, :, :]))
# contorno en nivel cero
mp.contour(lon, lat, Z, levels=[5],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(d) Aug-Oct Evaluation')
#plt.ylabel('Latitude')
#plt.xlabel('Longitude')
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
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_80_17_pgw[0,:,:]), cmap='hot_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year

lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_ago_oct_80_17_pgw[0, :, :]))
# contorno en nivel cero
mp.contour(lon, lat, Z, levels=[5],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(e) Aug-Oct PGW')
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

lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_ago_oct_diff[0, :, :]))
mp.contour(lon, lat, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
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

plt.savefig('figs/KEP-subplots-eva-pgw.png', dpi=400, bbox_inches='tight')
plt.show()
exit()


