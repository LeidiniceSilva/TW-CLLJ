#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot CLLJ subplots"

import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

from mpl_toolkits.basemap import Basemap
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

latlon = [-85.5, -47, 8, 27.5]

path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/verif_act-eva' # Path
#ds = /home/netapp-clima-users/users/jsalinas/CCC/ERA5/prom_ua925_jun-jul_1982-2016_ina.nc

# Subdomains (lat_min, lat_max, lon_min, lon_max)
subdomains = {
    ".": (13, 16,  -71, -76),}

def import_data(exp):

        ds = xr.open_dataset('{0}/prom_ua925_{1}.nc'.format(path, exp))
	# print(ds)

        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        time = ds.variables['time'][:]
        uwnd = ds.variables['ua925'][:]

        return lats, lons, uwnd


def import_data2(exp):

        ds = xr.open_dataset('{0}/prom_ua925_{1}.nc'.format(path, exp))
	# print(ds)

        lats2 = ds.variables['latitude'][:]
        lons2 = ds.variables['longitude'][:]
        time2 = ds.variables['time'][:]
        uwnd2 = ds.variables['u'][:]

        return lats2, lons2, uwnd2

###############  Inicia rpPrimer bloque lectura   eva   #########################################################################
lats, lons, uwnd_jun_jul_80_17_eva = import_data('jun-jul_1980-2017_eva')
lats, lons, uwnd_ago_oct_80_17_eva = import_data('ago-oct_1980-2017_eva')

lats2, lons2, uwnd2_jun_jul_80_17_act = import_data2('jun-jul_1980-2017_act')
lats2, lons2, uwnd2_ago_oct_80_17_act = import_data2('ago-oct_1980-2017_act')

lats, lons, uwnd_jun_jul_80_17_diff = import_data('jun-jul_diff')
lats, lons, uwnd_ago_oct_80_17_diff = import_data('ago-oct_diff')

# uwnd_jun_jul_80_17_act
min_height_jun_jul_80_17_act = int(np.min(np.squeeze(uwnd2_jun_jul_80_17_act[0,:,:])))
max_height_jun_jul_80_17_act = int(np.max(np.squeeze(uwnd2_jun_jul_80_17_act[0,:,:])))

# uwnd_ago_oct_80_17_act
min_height_ago_oct_80_17_act = int(np.min(np.squeeze(uwnd2_ago_oct_80_17_act[0,:,:])))
max_height_ago_oct_80_17_act = int(np.max(np.squeeze(uwnd2_ago_oct_80_17_act[0,:,:])))

# uwnd_jun_jul_82_16_ina
min_height_jun_jul_80_17_eva = int(np.min(np.squeeze(uwnd_jun_jul_80_17_eva[0,:,:])))
max_height_jun_jul_80_17_eva = int(np.max(np.squeeze(uwnd_jun_jul_80_17_eva[0,:,:])))

min_height_ago_oct_80_17_eva = int(np.min(np.squeeze(uwnd_ago_oct_80_17_eva[0,:,:])))
max_height_ago_oct_80_17_eva = int(np.max(np.squeeze(uwnd_ago_oct_80_17_eva[0,:,:])))

# uwnd_diff
mi2= -4
md2= 4

# uwnd_diff
#mi2= .5
#md2= 1.5

mi= -17
md= 0

# Plot figure
# Definiendo el mapa
mp = Basemap(projection='merc', llcrnrlon=-85.5, llcrnrlat=8, urcrnrlon=-47, urcrnrlat=27.5, resolution = 'i')
lon2, lat2 = np.meshgrid(lons2,lats2)  #this converts coordinates into 2D arrray
x2,y2 = mp(lon2,lat2) #mapping them together 

fig = plt.figure(figsize=(13.5,5)) #figure size 

ax = fig.add_subplot(2, 3, 1)

#c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_act[0,:,:]), cmap='jet', vmin=min_height_jun_jul_80_17_act, vmax=max_height_jun_jul_80_17_act) # [0,:,:] is for the first day of the year
c_scheme = mp.pcolor(x2,y2,np.squeeze(uwnd2_jun_jul_80_17_act[0,:,:]), cmap='Blues_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year

# contorno en nivel nueve
mp.contour(x2, y2, np.squeeze(uwnd2_jun_jul_80_17_act[0, :, :]), levels=[-9],colors='k', linewidths=0.4,linestyles='solid')
plt.title('(a) Jun-Jul ERA5')
#plt.ylabel('Latitude')

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
x,y = mp(lons,lats) #mapping them together 

ax = fig.add_subplot(2, 3, 2)
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_eva[0,:,:]), cmap='Blues_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year


lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_jun_jul_80_17_eva[0, :, :]))

# contorno en nivel nueve
mp.contour(lon, lat, Z, levels=[-9],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(b) Jun-Jul Evaluation')
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


ax = fig.add_subplot(2, 3, 3)
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_jun_jul_80_17_diff[0,:,:]), cmap='bwr', vmin=mi2, vmax=md2) # [0,:,:] is for the first day of the year

lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_jun_jul_80_17_diff[0, :, :]))

# contorno en nivel nueve
mp.contour(lon, lat, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
mp.contour(lon, lat, Z, levels=[2],colors='k', linewidths=0.4,linestyles='solid')


# contorno en nivel cero
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


ax = fig.add_subplot(2, 3, 4)
c_scheme = mp.pcolor(x2,y2,np.squeeze(uwnd2_ago_oct_80_17_act[0,:,:]), cmap='Blues_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year

# contorno en nivel nueve
mp.contour(x2, y2,np.squeeze(uwnd2_ago_oct_80_17_act[0, :, :]), levels=[-9],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(d) Aug-Oct ERA5')
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


ax = fig.add_subplot(2, 3, 5)
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_80_17_eva[0,:,:]), cmap='Blues_r', vmin=mi, vmax=md) # [0,:,:] is for the first day of the year


lon = np.array(x)
lat = np.array(y)
Z = np.array(np.squeeze(uwnd_ago_oct_80_17_eva[0, :, :]))
# contorno en nivel cero
mp.contour(lon, lat, Z, levels=[-9],colors='k', linewidths=0.4,linestyles='solid')

plt.title('(e) Aug-Oct Evaluation')
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


ax = fig.add_subplot(2, 3, 6)
c_scheme = mp.pcolor(x,y,np.squeeze(uwnd_ago_oct_80_17_diff[0,:,:]), cmap='bwr', vmin=mi2, vmax=md2) # [0,:,:] is for the first day of the year


lon = np.array(x)
lat = np.array(y)

Z = np.array(np.squeeze(uwnd_ago_oct_80_17_diff[0, :, :]))
# contorno en nivel cero
mp.contour(lon, lat, Z, levels=[0],colors='k', linewidths=0.4,linestyles='solid')
mp.contour(lon, lat, Z, levels=[2],colors='k', linewidths=0.4,linestyles='solid')


plt.title('(f) Difference')
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


plt.savefig('figs/CLLJ-subplots-act-eva.png', dpi=400, bbox_inches='tight')
plt.show()
exit()

############################################
