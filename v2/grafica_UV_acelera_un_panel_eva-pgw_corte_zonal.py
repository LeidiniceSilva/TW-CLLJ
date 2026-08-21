#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot mean zonal divergence"

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

path_ace = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo' # Path
path_adx = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/advectivos/grad_zonal' # Path
path_ady = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/advectivos/grad_meridional' # Path
path_efv = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/efe_v' # Path
path_dUV = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/UV_PRIMA/UV_PRIMA925' # Path
path_geo = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/grad_geopot' # Path
path_adv= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'
path_sum= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'
path_der= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'
path_uvp= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/UV_PRIMA/UV_PRIMA925'
path_duf= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'
path_ufg= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'
path_fgu= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'
path_uno= '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico'

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(path, file, var):

    ds = xr.open_dataset(f'{path}/{file}')
    lats = ds['lat']
    lons = ds['lon']
    uwnd = ds[var]

    return lats, lons, uwnd

###############  Inicia rpPrimer bloque lectura   eva   #########################################################################
lats, lons, ace_jun_jul_80_17_eva_925 = import_data(path_ace, 'pprom-acelera_ua925_jun-jul_eva.nc', 'ua925') 
lats, lons, efv_jun_jul_80_17_eva_925 = import_data(path_efv, 'prom-efe_ve_jun-jul_eva.nc', 'efeve')
lats, lons, geo_jun_jul_80_17_eva_925 = import_data(path_geo, 'prom-zg925_grad_meridional-jun-jul_eva.nc', 'zg925')
lats, lons, adv_jun_jul_80_17_eva_925 = import_data(path_adv, 'prom-suma-advectivos_jun-jul_eva.nc', 'ua925')
lats, lons, uvp_jun_jul_80_17_eva_925 = import_data(path_uvp, 'grad_meridional-jun-jul_eva_925.nc', 'ua925')
lats, lons, duf_jun_jul_80_17_eva_925 = import_data(path_duf, 'udu_dx_mas_fv_mas_grad_geopot-jun-jul_eva.nc', 'ua925')

ace_jun_jul_80_17_eva_925 = ace_jun_jul_80_17_eva_925.squeeze()
efv_jun_jul_80_17_eva_925 = efv_jun_jul_80_17_eva_925.squeeze()
geo_jun_jul_80_17_eva_925 = geo_jun_jul_80_17_eva_925.squeeze()
adv_jun_jul_80_17_eva_925 = adv_jun_jul_80_17_eva_925.squeeze()
uvp_jun_jul_80_17_eva_925 = uvp_jun_jul_80_17_eva_925.squeeze()
duf_jun_jul_80_17_eva_925 = duf_jun_jul_80_17_eva_925.squeeze()

###############  Inicia segundo  bloque lectura   pgw   #########################################################################
lats, lons, ace_jun_jul_80_17_pgw_925 = import_data(path_ace, 'pprom-acelera_ua925_jun-jul_pgw.nc', 'ua925')
lats, lons, efv_jun_jul_80_17_pgw_925 = import_data(path_efv, 'prom-efe_ve_jun-jul_pgw.nc', 'efeve')
lats, lons, geo_jun_jul_80_17_pgw_925 = import_data(path_geo, 'prom-zg925_grad_meridional-jun-jul_pgw.nc', 'zg925')
lats, lons, adv_jun_jul_80_17_pgw_925 = import_data(path_adv, 'prom-suma-advectivos_jun-jul_pgw.nc', 'ua925')
lats, lons, uvp_jun_jul_80_17_pgw_925 = import_data(path_uvp, 'grad_meridional-jun-jul_pgw_925.nc', 'ua925')
lats, lons, duf_jun_jul_80_17_pgw_925 = import_data(path_duf, 'udu_dx_mas_fv_mas_grad_geopot-jun-jul_pgw.nc', 'ua925')

ace_jun_jul_80_17_pgw_925 = ace_jun_jul_80_17_pgw_925.squeeze()
efv_jun_jul_80_17_pgw_925 = efv_jun_jul_80_17_pgw_925.squeeze()
geo_jun_jul_80_17_pgw_925 = geo_jun_jul_80_17_pgw_925.squeeze()
adv_jun_jul_80_17_pgw_925 = adv_jun_jul_80_17_pgw_925.squeeze()
uvp_jun_jul_80_17_pgw_925 = uvp_jun_jul_80_17_pgw_925.squeeze()
duf_jun_jul_80_17_pgw_925 = duf_jun_jul_80_17_pgw_925.squeeze()

###############  Inicia Tercer bloque lectura   eva   #########################################################################
lats, lons, ace_ago_oct_80_17_eva_925 = import_data(path_ace, 'pprom-acelera_ua925_ago-oct_eva.nc', 'ua925')
lats, lons, efv_ago_oct_80_17_eva_925 = import_data(path_efv, 'prom-efe_ve_ago-oct_eva.nc', 'efeve')
lats, lons, geo_ago_oct_80_17_eva_925 = import_data(path_geo, 'prom-zg925_grad_meridional-ago-oct_eva.nc', 'zg925')
lats, lons, adv_ago_oct_80_17_eva_925 = import_data(path_adv, 'prom-suma-advectivos_ago-oct_eva.nc', 'ua925')
lats, lons, uvp_ago_oct_80_17_eva_925 = import_data(path_uvp, 'grad_meridional-ago-oct_eva_925.nc', 'ua925')
lats, lons, duf_ago_oct_80_17_eva_925 = import_data(path_duf, 'udu_dx_mas_fv_mas_grad_geopot-ago-oct_eva.nc', 'ua925')

ace_ago_oct_80_17_eva_925 = ace_ago_oct_80_17_eva_925.squeeze()
efv_ago_oct_80_17_eva_925 = efv_ago_oct_80_17_eva_925.squeeze()
geo_ago_oct_80_17_eva_925 = geo_ago_oct_80_17_eva_925.squeeze()
adv_ago_oct_80_17_eva_925 = adv_ago_oct_80_17_eva_925.squeeze()
uvp_ago_oct_80_17_eva_925 = uvp_ago_oct_80_17_eva_925.squeeze()
duf_ago_oct_80_17_eva_925 = duf_ago_oct_80_17_eva_925.squeeze()

###############  Inicia cuarto bloque lectura   pgw   #########################################################################
lats, lons, ace_ago_oct_80_17_pgw_925 = import_data(path_ace, 'pprom-acelera_ua925_ago-oct_pgw.nc', 'ua925')
lats, lons, efv_ago_oct_80_17_pgw_925 = import_data(path_efv, 'prom-efe_ve_ago-oct_pgw.nc', 'efeve')
lats, lons, geo_ago_oct_80_17_pgw_925 = import_data(path_geo, 'prom-zg925_grad_meridional-ago-oct_pgw.nc', 'zg925')
lats, lons, adv_ago_oct_80_17_pgw_925 = import_data(path_adv, 'prom-suma-advectivos_ago-oct_pgw.nc', 'ua925')
lats, lons, uvp_ago_oct_80_17_pgw_925 = import_data(path_uvp, 'grad_meridional-ago-oct_pgw_925.nc', 'ua925')
lats, lons, duf_ago_oct_80_17_pgw_925 = import_data(path_duf, 'udu_dx_mas_fv_mas_grad_geopot-ago-oct_pgw.nc', 'ua925')

ace_ago_oct_80_17_pgw_925 = ace_ago_oct_80_17_pgw_925.squeeze()
efv_ago_oct_80_17_pgw_925 = efv_ago_oct_80_17_pgw_925.squeeze()
geo_ago_oct_80_17_pgw_925 = geo_ago_oct_80_17_pgw_925.squeeze()
adv_ago_oct_80_17_pgw_925 = adv_ago_oct_80_17_pgw_925.squeeze()
uvp_ago_oct_80_17_pgw_925 = uvp_ago_oct_80_17_pgw_925.squeeze()
duf_ago_oct_80_17_pgw_925 = duf_ago_oct_80_17_pgw_925.squeeze()

###############  Inicia quinto bloque lectura   diff  #########################################################################
lats, lons, ace_jun_jul_80_17_diff_925 = import_data(path_ace, 'pprom-acelera_ua925_jun-jul_diff.nc', 'ua925')
lats, lons, efv_jun_jul_80_17_diff_925 = import_data(path_efv, 'prom-efe_ve_jun-jul_diff.nc', 'efeve')
lats, lons, geo_jun_jul_80_17_diff_925 = import_data(path_geo, 'prom-zg925_grad_meridional-jun-jul_diff.nc', 'zg925')
lats, lons, adv_jun_jul_80_17_diff_925 = import_data(path_adv, 'prom-suma-advectivos_jun-jul_diff.nc', 'ua925')
lats, lons, uvp_jun_jul_80_17_diff_925 = import_data(path_uvp, 'grad_meridional-jun-jul_diff_925.nc', 'ua925')
lats, lons, duf_jun_jul_80_17_diff_925 = import_data(path_duf, 'udu_dx_mas_fv_mas_grad_geopot-jun-jul_diff.nc', 'ua925')

ace_jun_jul_80_17_diff_925 = ace_jun_jul_80_17_diff_925.squeeze()
efv_jun_jul_80_17_diff_925 = efv_jun_jul_80_17_diff_925.squeeze()
geo_jun_jul_80_17_diff_925 = geo_jun_jul_80_17_diff_925.squeeze()
adv_jun_jul_80_17_diff_925 = adv_jun_jul_80_17_diff_925.squeeze()
uvp_jun_jul_80_17_diff_925 = uvp_jun_jul_80_17_diff_925.squeeze()
duf_jun_jul_80_17_diff_925 = duf_jun_jul_80_17_diff_925.squeeze()

###############  Inicia sexto bloque lectura   diff  #########################################################################
lats, lons, ace_ago_oct_80_17_diff_925 = import_data(path_ace, 'pprom-acelera_ua925_ago-oct_diff.nc', 'ua925')
lats, lons, efv_ago_oct_80_17_diff_925 = import_data(path_efv, 'prom-efe_ve_ago-oct_diff.nc', 'efeve')
lats, lons, geo_ago_oct_80_17_diff_925 = import_data(path_geo, 'prom-zg925_grad_meridional-ago-oct_diff.nc', 'zg925')
lats, lons, adv_ago_oct_80_17_diff_925 = import_data(path_adv, 'prom-suma-advectivos_ago-oct_diff.nc', 'ua925')
lats, lons, uvp_ago_oct_80_17_diff_925 = import_data(path_uvp, 'grad_meridional-ago-oct_diff_925.nc', 'ua925')
lats, lons, duf_ago_oct_80_17_diff_925 = import_data(path_duf, 'udu_dx_mas_fv_mas_grad_geopot-ago-oct_diff.nc', 'ua925')

ace_ago_oct_80_17_diff_925 = ace_ago_oct_80_17_diff_925.squeeze()
efv_ago_oct_80_17_diff_925 = efv_ago_oct_80_17_diff_925.squeeze()
geo_ago_oct_80_17_diff_925 = geo_ago_oct_80_17_diff_925.squeeze()
adv_ago_oct_80_17_diff_925 = adv_ago_oct_80_17_diff_925.squeeze()
uvp_ago_oct_80_17_diff_925 = uvp_ago_oct_80_17_diff_925.squeeze()
duf_ago_oct_80_17_diff_925 = duf_ago_oct_80_17_diff_925.squeeze()

fig = plt.figure(figsize=(14.5,10)) #figure size 

vmin=-2.0e-05
vmax=2.0e-05

vmin2=-6.00e-06
vmax2=6.0e-06

###################   Empieza primera grafica   ##############################################
ax = fig.add_subplot(2, 3, 1)
####  selecciona la banda latitudinal para jun-jul eva #######
uwnd_band1 = ace_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean1 = uwnd_band1.mean(dim='y')

uwnd_band21 = ace_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean21 = uwnd_band21.mean(dim='y')

uwnd_band121 = uvp_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean121 = uwnd_band121.mean(dim='y')

uwnd_band122 = uvp_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean122 = uwnd_band122.mean(dim='y')

plt.plot(lons[0,:], uwnd_mean1.squeeze(), label='Acceleration')
plt.plot(lons[0,:], -uwnd_mean121.squeeze(), label='perturbations')
plt.grid()
plt.legend()

####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band4 = efv_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean4 = uwnd_band4.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean4.squeeze(), label='fv.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band6 = geo_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean6 = uwnd_band6.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean6.squeeze(), label='Geopot. Gradient.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band8 = adv_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean8 = uwnd_band8.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean8.squeeze(), label='Advective terms.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band10 = uvp_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean10 = uwnd_band10.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean10.squeeze(), label='jun-Jul. Perturbations momentum convergence. eva')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band11 = duf_jun_jul_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean11 = uwnd_band11.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean11.squeeze(), label='Advectives terms + fv')
plt.grid()

# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('m/s**2')
plt.title('(a) Jun-Jul Evaluation')
plt.ylim(vmin, vmax)
plt.grid()

# --- Notación científica en eje y ---
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
###################  Termina primera grafica   ##############################################

###################   Empieza segunda grafica   ##############################################
ax = fig.add_subplot(2, 3, 2)
####  selecciona la banda latitudinal para jun-jul pgw #######
uwnd_band21 = ace_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean21 = uwnd_band21.mean(dim='y')
plt.plot(lons[0,:], uwnd_mean21.squeeze(), label='Jun-Jul. Accel. ')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band24 = efv_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean24 = uwnd_band24.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean24.squeeze(), label='fv.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band26 = geo_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean26 = uwnd_band26.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean26.squeeze(), label='Geopot. Gradient.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band28 = adv_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean28 = uwnd_band28.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean28.squeeze(), label='Advective terms.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band30 = uvp_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean30 = uwnd_band30.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean30.squeeze(), label='jun-Jul. pgw')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band31 = duf_jun_jul_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean31 = uwnd_band31.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean31.squeeze(), label='Advectives terms + fv.')
plt.grid()

# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('m/s**2')
plt.title('(b) Jun-Jul PGW')
plt.ylim(vmin, vmax)
plt.grid()
# --- Notación científica en eje y ---
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

###################  Termina segunda grafica   ##############################################

###################   Empieza tercera grafica   ##############################################
ax = fig.add_subplot(2, 3, 4)
####  selecciona la banda latitudinal para jun-jul pgw #######
uwnd_band41 = ace_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean41 = uwnd_band41.mean(dim='y')
plt.plot(lons[0,:], uwnd_mean41.squeeze(), label='Jun-Jul. Accel. eva')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band44 = efv_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean44 = uwnd_band44.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean44.squeeze(), label='fv.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band46 = geo_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean46 = uwnd_band46.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean46.squeeze(), label='Geopot. Gradient.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band48 = adv_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean48 = uwnd_band48.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean48.squeeze(), label='Advective terms.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band40 = uvp_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean40 = uwnd_band40.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean40.squeeze(), label='jun-Jul. momentum conv. ')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band51 = duf_ago_oct_80_17_eva_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean51 = uwnd_band51.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean51.squeeze(), label='Advectives terms + fv.')
plt.grid()

# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('m/s**2')
plt.title('(d) Aug-Oct Evaluation')
plt.ylim(vmin, vmax)
plt.grid()
# --- Notación científica en eje y ---
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

###################  Termina tercera grafica   ##############################################


###################   Empieza cuarta grafica   ##############################################
ax = fig.add_subplot(2, 3, 5)
####  selecciona la banda latitudinal para jun-jul pgw #######
uwnd_band61 = ace_ago_oct_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean61 = uwnd_band61.mean(dim='y')
plt.plot(lons[0,:], uwnd_mean61.squeeze(), label='Jun-Jul. Accel. eva')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band64 = efv_ago_oct_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean64 = uwnd_band64.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean64.squeeze(), label='fv.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band66 = geo_ago_oct_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean66 = uwnd_band66.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean66.squeeze(), label='Geopot. Gradient.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band68 = adv_ago_oct_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean68 = uwnd_band68.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean68.squeeze(), label='Advective terms.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band60 = uvp_ago_oct_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean60 = uwnd_band60.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean60.squeeze(), label='jun-Jul. Pert momentum convergence.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band71 = duf_ago_oct_80_17_pgw_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean71 = uwnd_band71.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean71.squeeze(), label='Advectives terms + fv.')
plt.grid()

# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('m/s**2')
plt.title('(e) Aug-Oct PGW')
plt.ylim(vmin, vmax)
plt.grid()
# --- Notación científica en eje y ---
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

###################  Termina cuarta grafica   ##############################################


###################   Empieza quinta grafica   ##############################################
ax = fig.add_subplot(2, 3, 3)
####  selecciona la banda latitudinal para jun-jul pgw #######
uwnd_band81 = ace_jun_jul_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean81 = uwnd_band81.mean(dim='y')
plt.plot(lons[0,:], uwnd_mean81.squeeze(), label='Jun-Jul. Accel. eva')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band84 = efv_jun_jul_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean84 = uwnd_band84.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean84.squeeze(), label='fv.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band86 = geo_jun_jul_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean86 = uwnd_band86.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean86.squeeze(), label='Geopot. Gradient.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band88 = adv_jun_jul_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean88 = uwnd_band88.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean88.squeeze(), label='Advective terms.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band80 = uvp_jun_jul_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean80 = uwnd_band80.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean80.squeeze(), label='jun-Jul. Perturbations momentum convergence.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band91 = duf_jun_jul_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean91 = uwnd_band91.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean91.squeeze(), label='Advectives terms + fv.')
plt.grid()

# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('m/s**2')
plt.title('(c) Difference')
plt.ylim(vmin2, vmax2)
plt.grid()
# --- Notación científica en eje y ---
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

###################  Termina quinta grafica   ##############################################

###################   Empieza sexta grafica   ##############################################
ax = fig.add_subplot(2, 3, 6)
####  selecciona la banda latitudinal para jun-jul pgw #######
uwnd_band101 = ace_ago_oct_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean101 = uwnd_band101.mean(dim='y')
plt.plot(lons[0,:], uwnd_mean101.squeeze(), label='Jun-Jul. Accel. eva')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band104 = efv_ago_oct_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean104 = uwnd_band104.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean104.squeeze(), label='fv.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band106 = geo_ago_oct_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean106 = uwnd_band106.mean(dim='y')
#plt.plot(lons[0,:], -uwnd_mean106.squeeze(), label='Geopot. Gradient.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band108 = adv_ago_oct_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean108 = uwnd_band108.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean108.squeeze(), label='Advective terms.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band100 = uvp_ago_oct_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean100 = uwnd_band100.mean(dim='y')
plt.plot(lons[0,:], -uwnd_mean100.squeeze(), label='jun-Jul. Perturbations momentum convergence.')
plt.grid()
####  selecciona la banda latitudinal para ago-oct pgw #######
uwnd_band111 = duf_ago_oct_80_17_diff_925.where((lats >= 12.5) & (lats <= 17.5), drop=True)
uwnd_mean111 = uwnd_band111.mean(dim='y')
#plt.plot(lons[0,:], uwnd_mean111.squeeze(), label='Advectives terms + fv.')
plt.grid()

# --- línea horizontal en y=0 ---
plt.axhline(0, color='k', linestyle='-', linewidth=1)

# líneas verticales
plt.axvline(x=-76, color='k', linestyle='--', linewidth=1)
plt.axvline(x=-71, color='k', linestyle='--', linewidth=1)

plt.xlabel('Longitude')
plt.ylabel('m/s**2')
plt.title('(f) Difference')
plt.ylim(vmin2, vmax2)
plt.grid()

plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

plt.tight_layout()   # <--- asegura que se vean todos los textos
plt.savefig('figs/UV_y_ace_corte-zonal-subplots-eva_pgw.png', dpi=400, bbox_inches='tight')
plt.show()
exit()
