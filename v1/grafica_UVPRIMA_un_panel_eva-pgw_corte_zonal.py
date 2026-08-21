#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot mean zonal divergence"

import matplotlib.patches as patches
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

path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/UV_PRIMA/UV_PRIMA925' # Path

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(exp):

        ds = xr.open_dataset('{0}/grad_meridional-{1}.nc'.format(path, exp))
        lats = ds['lat']
        lons = ds['lon']
        uwnd = ds['ua925']

        return lats, lons, uwnd


lats, lons, uwnd_jun_jul_80_17_eva_925 = import_data('jun-jul_eva_925')
lats, lons, uwnd_ago_oct_80_17_eva_925 = import_data('ago-oct_eva_925')
lats, lons, uwnd_jun_jul_82_16_pgw_925 = import_data('jun-jul_pgw_925')
lats, lons, uwnd_ago_oct_82_16_pgw_925 = import_data('ago-oct_pgw_925')
lats, lons, uwnd_jun_jul_diff_925 = import_data('jun-jul_diff_925')
lats, lons, uwnd_ago_oct_diff_925 = import_data('ago-oct_diff_925')

####  selecciona la banda latitudinal para jun-jul eva #######
uwnd_band1 = uwnd_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean1 = uwnd_band1.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean1.squeeze(), label='Jun-Jul Evaluation')
plt.grid()
####  selecciona la banda latitudinal para ago-oct eva #######
uwnd_band2 = uwnd_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean2 = uwnd_band2.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean2.squeeze(), label='Aug-Oct Evaluation')
plt.grid()
####  selecciona la banda latitudinal para jun-jul pgw #######
uwnd_band3 = uwnd_jun_jul_82_16_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean3 = uwnd_band3.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean3.squeeze(), label='Jun-Jul PGW')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band4 = uwnd_ago_oct_82_16_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean4 = uwnd_band4.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean4.squeeze(), label='Aug-Oct PGW')

plt.axhline(0, color='k', linestyle='-', linewidth=1)
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('Meridional divergence of momentum')
plt.title(' Mean meridional divergence of momentum 12.5°N–17.5°N at 925 hPa')
plt.grid()

plt.legend()   # muestra los nombres con los mismos colores

plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

plt.tight_layout()   # <--- asegura que se vean todos los textos
plt.savefig('figs/grad_merid_UVPPRIMA-corte-zonal-subplots-eva_pgw.png', dpi=400, bbox_inches='tight')

plt.show()
exit()
