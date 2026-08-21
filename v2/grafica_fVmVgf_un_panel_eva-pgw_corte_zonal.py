#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot Coriolis fv"

import matplotlib.ticker as ticker
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from mpl_toolkits.basemap import Basemap
from scipy.ndimage import gaussian_filter
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.ticker import FormatStrFormatter


latlon = [-85.5, -47, 8, 27.5]
path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/grad_geopot/Vageostrofico' # Path

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(exp):
        ds = xr.open_dataset('{0}/prom-efe_v_menos_efeVg-{1}.nc'.format(path, exp))
	# print(ds)

        lats = ds['lat']
        lons = ds['lon']
        uwnd = ds['fvmfVg']

        return lats, lons, uwnd

lats, lons, uwnd_jun_jul_80_17_eva_925 = import_data('jun-jul_eva')
lats, lons, uwnd_ago_oct_80_17_eva_925 = import_data('ago-oct_eva')
lats, lons, uwnd_jun_jul_82_16_pgw_925 = import_data('jun-jul_pgw')
lats, lons, uwnd_ago_oct_82_16_pgw_925 = import_data('ago-oct_pgw')

fig, ax = plt.subplots()   # ← esto es clave

####  selecciona la banda latitudinal para jun-jul eva #######
uwnd_band1 = uwnd_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)

# Smooth only between -63 and -60 longitude along the longitude axis (axes=-1)
lon_b1 = uwnd_band1['lon']
uwnd_smoothed1 = uwnd_band1.copy()
uwnd_smoothed1.values = gaussian_filter(uwnd_band1.values, sigma=8, axes=-1)
uwnd_band1 = xr.where((lon_b1 >= -63) & (lon_b1 <= -60), uwnd_smoothed1, uwnd_band1)

lons_band1 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band1, uwnd_band1 = xr.align(lons_band1, uwnd_band1)
uwnd_mean1 = uwnd_band1.mean(dim='y')
lons_mean1 = lons_band1.mean(dim='y')

#plt.plot(lons_mean1, uwnd_mean1.isel(time=0)*9.81, label='Jun-Jul. eva')
plt.plot(lons_mean1, uwnd_mean1, label='Jun-Jul Evaluation')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
plt.grid()

####  selecciona la banda latitudinal para ago-oct eva #######
uwnd_band2 = uwnd_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)

# Smooth only between -63 and -60 longitude along the longitude axis (axes=-1)
lon_b2 = uwnd_band2['lon']
uwnd_smoothed2 = uwnd_band2.copy()
uwnd_smoothed2.values = gaussian_filter(uwnd_band2.values, sigma=8, axes=-1)
uwnd_band2 = xr.where((lon_b2 >= -63) & (lon_b2 <= -60), uwnd_smoothed2, uwnd_band2)

lons_band2 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band2, uwnd_band2 = xr.align(lons_band2, uwnd_band2)
uwnd_mean2 = uwnd_band2.mean(dim='y')
lons_mean2 = lons_band2.mean(dim='y')

#plt.plot(lons_mean2, uwnd_mean2.isel(time=0)*9.81, label='Aug-Oct. eva')
plt.plot(lons_mean2, uwnd_mean2, label='Aug-Oct Evaluation')
plt.grid()

#############################################################################
####  selecciona la banda latitudinal para jun-jul eva #######
uwnd_band3 = uwnd_jun_jul_82_16_pgw_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)

# Smooth only between -63 and -60 longitude along the longitude axis (axes=-1)
lon_b3 = uwnd_band3['lon']
uwnd_smoothed3 = uwnd_band3.copy()
uwnd_smoothed3.values = gaussian_filter(uwnd_band3.values, sigma=8, axes=-1)
uwnd_band3 = xr.where((lon_b3 >= -63) & (lon_b3 <= -60), uwnd_smoothed3, uwnd_band3)

lons_band3 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band3, uwnd_band3 = xr.align(lons_band3, uwnd_band3)
uwnd_mean3 = uwnd_band3.mean(dim='y')
lons_mean3 = lons_band3.mean(dim='y')

#plt.plot(lons_mean3, uwnd_mean3.isel(time=0)*9.81, label='Jun-Jul. pgw')
plt.plot(lons_mean3, uwnd_mean3, label='Jun-Jul PGW')
plt.grid()

####  selecciona la banda latitudinal para ago-oct eva #######
uwnd_band4 = uwnd_ago_oct_82_16_pgw_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)

# Smooth only between -63 and -60 longitude along the longitude axis (axes=-1)
lon_b4 = uwnd_band4['lon']
uwnd_smoothed4 = uwnd_band4.copy()
uwnd_smoothed4.values = gaussian_filter(uwnd_band4.values, sigma=8, axes=-1)
uwnd_band4 = xr.where((lon_b4 >= -63) & (lon_b4 <= -60), uwnd_smoothed4, uwnd_band4)

lons_band4 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band4, uwnd_band4 = xr.align(lons_band4, uwnd_band4)
uwnd_mean4 = uwnd_band4.mean(dim='y')
lons_mean4 = lons_band4.mean(dim='y')

#plt.plot(lons_mean4, uwnd_mean4.isel(time=0)*9.81, label='Aug-Oct. pgw')
plt.plot(lons_mean4, uwnd_mean4, label='Aug-Oct PGW')
plt.grid()

#############################################################################
plt.axhline(0, color='k', linestyle='-', linewidth=1)
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)
plt.xlabel('Longitude')
plt.ylabel('fv minus Vgf')
plt.title('Zonal mean 12.5°N–17.5°N')
plt.grid()

plt.legend()   # muestra los nombres con los mismos colores

plt.savefig('figs/Efef_por_Vg-corte-zonal-subplots-eva_pgw.png', dpi=400, bbox_inches='tight')
plt.show()
exit()
