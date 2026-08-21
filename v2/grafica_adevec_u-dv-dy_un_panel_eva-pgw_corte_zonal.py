#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot zonal wind advection at 925 hPa"

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


latlon = [-85.5, -47, 8, 27.5]

#grad_meridional-jun-jul_eva_925.nc
#grad_meridional-ago-oct_pgw_925.nc
#grad_meridional-jun-jul_diff_925.nc
path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/advectivos/grad_meridional' # Path

#ds = /home/netapp-clima-users/users/jsalpgw_925s/CCC/ERA5/prom_ua925_jun-jul_1982-2016_pgw_925.nc

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(exp):
        ds = xr.open_dataset('{0}/prom-du_grad_merid-{1}.nc'.format(path, exp))
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

#########################################################################
####  selecciona la banda latitudinal para jun-jul eva #######
uwnd_band1 = uwnd_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
uwnd_mean1 = uwnd_band1.mean(dim='y')
lons_band1 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band1, uwnd_band1 = xr.align(lons_band1, uwnd_band1)
uwnd_mean1 = uwnd_band1.mean(dim='y')
lons_mean1 = lons_band1.mean(dim='y')
plt.plot(lons_mean1, -uwnd_mean1.isel(time=0)*9.81, label='Jun-Jul Evaluation')
plt.grid()
####  selecciona la banda latitudinal para ago-oct eva #######
uwnd_band2 = uwnd_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
uwnd_mean1 = uwnd_band1.mean(dim='y')
lons_band2 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band2, uwnd_band2 = xr.align(lons_band2, uwnd_band2)
uwnd_mean2 = uwnd_band2.mean(dim='y')
lons_mean2 = lons_band2.mean(dim='y')
plt.plot(lons_mean2, -uwnd_mean2.isel(time=0)*9.81, label='Aug-Oct Evaluation')
plt.grid()

#############################################################################
####  selecciona la banda latitudinal para jun-jul eva #######
uwnd_band3 = uwnd_jun_jul_82_16_pgw_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
uwnd_mean3 = uwnd_band3.mean(dim='y')
lons_band3 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band3, uwnd_band3 = xr.align(lons_band3, uwnd_band3)
uwnd_mean3 = uwnd_band3.mean(dim='y')
lons_mean3 = lons_band3.mean(dim='y')
plt.plot(lons_mean3, -uwnd_mean3.isel(time=0)*9.81, label='Jun-Jul PGW')
plt.grid()
####  selecciona la banda latitudinal para ago-oct eva #######
uwnd_band4 = uwnd_ago_oct_82_16_pgw_925.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
uwnd_mean4 = uwnd_band4.mean(dim='y')
lons_band4 = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
#  CLAVE: alinear explícitamente
lons_band4, uwnd_band4 = xr.align(lons_band4, uwnd_band4)
uwnd_mean4 = uwnd_band4.mean(dim='y')
lons_mean4 = lons_band4.mean(dim='y')
plt.plot(lons_mean4, -uwnd_mean4.isel(time=0)*9.81, label='Aug-Oct PGW')
plt.grid()

#############################################################################
# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('Advective meridional term')
plt.title('v_du_dy_zonal_mean 12.5°N–17.5°N at 925 hPa')
plt.grid()

plt.legend()   # muestra los nombres con los mismos colores

# --- Notación científica en eje y ---
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

plt.tight_layout()   # <--- asegura que se vean todos los textos
plt.savefig('figs/advective-meridional-term-corte-zonal-subplots-eva_pgw.png', dpi=400, bbox_inches='tight')
plt.show()
exit()
############################################
