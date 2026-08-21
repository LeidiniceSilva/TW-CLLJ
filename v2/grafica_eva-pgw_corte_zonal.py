#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com"
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plots 925 hPa atmospheric dynamics terms in a 3x3 panel layout with subplot labels (a)-(g)"

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd

from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from mpl_toolkits.basemap import Basemap
from scipy.ndimage import gaussian_filter

# Configuration & Constants
LATLON = [-85.5, -47, 8, 27.5]
PATH_ACCEL       = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo' 
PATH_ADVEC_ZONAL = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/advectivos/grad_zonal'
PATH_ADVEC_MERID = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/advectivos/grad_meridional'
PATH_U2P_ZONAL   = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/advectivos/u2P_zonal'
PATH_UV_PRIMA    = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/UV_PRIMA/UV_PRIMA925'
PATH_CORIOLIS    = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/grad_geopot/Vageostrofico'
PATH_BALANCE     = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/acelera_tiempo/balance_dinamico/nuevo_balance_dinamico'

EXPERIMENTS = [
    ('jun-jul_eva', 'Jun-Jul Evaluation'),
    ('ago-oct_eva', 'Aug-Oct Evaluation'),
    ('jun-jul_pgw', 'Jun-Jul PGW'),
    ('ago-oct_pgw', 'Aug-Oct PGW')
]


def import_dataset(file_path, var_name='ua925'):
    """Opens a NetCDF file and extracts latitude, longitude, time, and target variable safely."""
    ds = xr.open_dataset(file_path)
    lats = ds['lat']
    lons = ds['lon']
    
    # Safely extract time values (handles 0D scalars, 1D+ arrays, and missing time)
    if 'time' in ds:
        time = ds['time'].values
    else:
        time = None
        
    var = ds[var_name]
    return lats, lons, time, var


def process_zonal_advection(lats, lons, var, sigma=4, lon_min=-63, lon_max=-59):
    """Applies lat/lon bounds, selective Gaussian smoothing, alignment, and spatial averaging."""
    var_band = var.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
    
    # Selective smoothing along longitude axis
    lon_b = var_band['lon']
    var_smoothed = var_band.copy()
    var_smoothed.values = gaussian_filter(var_band.values, sigma=sigma, axes=-1)
    var_band = xr.where((lon_b >= lon_min) & (lon_b <= lon_max), var_smoothed, var_band)

    # Alignment and averaging
    lons_band = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
    lons_band, var_band = xr.align(lons_band, var_band)
    
    return lons_band.mean(dim='y'), var_band.mean(dim='y')


def process_meridional_advection(lats, lons, var):
    """Applies lat/lon bounds, coordinate alignment, and spatial averaging for meridional terms."""
    var_band = var.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
    lons_band = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
    
    lons_band, var_band = xr.align(lons_band, var_band)
    
    return lons_band.mean(dim='y'), var_band.mean(dim='y')


def process_coriolis_term(lats, lons, var, sigma=8, lon_min=-63, lon_max=-60):
    """Applies lat/lon bounds, selective Gaussian smoothing (sigma=8), alignment, and spatial averaging for Coriolis term."""
    var_band = var.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
    
    lon_b = var_band['lon']
    var_smoothed = var_band.copy()
    var_smoothed.values = gaussian_filter(var_band.values, sigma=sigma, axes=-1)
    var_band = xr.where((lon_b >= lon_min) & (lon_b <= lon_max), var_smoothed, var_band)

    lons_band = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
    lons_band, var_band = xr.align(lons_band, var_band)
    
    return lons_band.mean(dim='y'), var_band.mean(dim='y')


def process_balance_term(lats, lons, var, sigma=6, lon_min=-63, lon_max=-59):
    """Applies lat/lon bounds, selective Gaussian smoothing (sigma=6), alignment, and spatial averaging for dynamic balance term."""
    var_band = var.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -85) & (lons <= -47), drop=True)
    
    lon_b = var_band['lon']
    var_smoothed = var_band.copy()
    var_smoothed.values = gaussian_filter(var_band.values, sigma=sigma, axes=-1)
    var_band = xr.where((lon_b >= lon_min) & (lon_b <= lon_max), var_smoothed, var_band)

    lons_band = lons.where((lats >= 12.5) & (lats <= 17.5) & (lons >= -84) & (lons <= -47), drop=True)
    lons_band, var_band = xr.align(lons_band, var_band)
    
    return lons_band.mean(dim='y'), var_band.mean(dim='y')


def setup_subplot_style(ax, title, ylabel=''):
    """Applies common aesthetics, gridlines, axis formatting, and legends to each panel."""
    ax.axhline(0, color='k', linestyle='-', linewidth=1)
    ax.axvline(x=-76, color='k', linestyle='--', linewidth=1)
    ax.axvline(x=-71, color='k', linestyle='--', linewidth=1)
    ax.set_xlabel('Longitude')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))


# Initialize 3x3 Subplots Figure (7 Active Panels)
fig, axes = plt.subplots(3, 3, figsize=(22, 16))

# ==========================================
# Panel (a): Zonal Mean Acceleration
# ==========================================
ax = axes[0, 0]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_ACCEL}/pprom-acelera_ua925_{exp_key}.nc'
    lats, lons, _, uwnd = import_dataset(file_path)
    
    uwnd_band = uwnd.where((lats >= 12.5) & (lats <= 17.5), drop=True)
    uwnd_mean = uwnd_band.mean(dim='y')
    
    ax.plot(lons[0, :], uwnd_mean.squeeze(), label=label)

setup_subplot_style(ax, '(a) Zonal mean 12.5°N–17.5°N at 925 hPa', ylabel='')

# ==========================================
# Panel (b): Zonal Wind Advection
# ==========================================
ax = axes[0, 1]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_ADVEC_ZONAL}/prom-u_du_meridional-{exp_key}.nc'
    lats, lons, _, uwnd = import_dataset(file_path)
    
    lons_mean, uwnd_mean = process_zonal_advection(lats, lons, uwnd, sigma=4, lon_min=-63, lon_max=-59)
    advec_term = -uwnd_mean.isel(time=0) * 9.81
    
    ax.plot(lons_mean, advec_term, label=label)

setup_subplot_style(ax, '(b) u_du_dx_zonal_mean 12.5°N–17.5°N at 925 hPa', ylabel='Advective zonal term')

# ==========================================
# Panel (c): Meridional Wind Advection
# ==========================================
ax = axes[0, 2]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_ADVEC_MERID}/prom-du_grad_merid-{exp_key}.nc'
    lats, lons, _, uwnd = import_dataset(file_path)
    
    lons_mean, uwnd_mean = process_meridional_advection(lats, lons, uwnd)
    advec_term = -uwnd_mean.isel(time=0) * 9.81
    
    ax.plot(lons_mean, advec_term, label=label)

setup_subplot_style(ax, '(c) v_du_dy_zonal_mean 12.5°N–17.5°N at 925 hPa', ylabel='Advective meridional term')

# ==========================================
# Panel (d): Mean Zonal Divergence
# ==========================================
ax = axes[1, 0]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_U2P_ZONAL}/du_grad_zonal-{exp_key}.nc'
    lats, lons, _, uwnd = import_dataset(file_path)
    
    lons_mean, uwnd_mean = process_zonal_advection(lats, lons, uwnd, sigma=2, lon_min=-63, lon_max=-60)
    div_term = -uwnd_mean.isel(time=0) * 9.81
    
    ax.plot(lons_mean, div_term, label=label)

setup_subplot_style(ax, '(d) Mean zonal divergence 12.5°N–17.5°N at 925 hPa', ylabel='du2_dx')

# ==========================================
# Panel (e): Mean Meridional Divergence of Momentum
# ==========================================
ax = axes[1, 1]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_UV_PRIMA}/grad_meridional-{exp_key}_925.nc'
    lats, lons, _, uwnd = import_dataset(file_path)
    
    uwnd_band = uwnd.where((lats >= 12.5) & (lats <= 17.5), drop=True)
    uwnd_mean = uwnd_band.mean(dim='y')
    
    ax.plot(lons[0, :], -uwnd_mean.squeeze(), label=label)

setup_subplot_style(ax, '(e) Mean meridional divergence of momentum 12.5°N–17.5°N at 925 hPa', ylabel='Meridional divergence of momentum')

# ==========================================
# Panel (f): Coriolis Term f(v - vg)
# ==========================================
ax = axes[1, 2]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_CORIOLIS}/prom-efe_v_menos_efeVg-{exp_key}.nc'
    lats, lons, _, uwnd = import_dataset(file_path, var_name='fvmfVg')
    
    lons_mean, uwnd_mean = process_coriolis_term(lats, lons, uwnd, sigma=8, lon_min=-63, lon_max=-60)
    
    ax.plot(lons_mean, uwnd_mean, label=label)

setup_subplot_style(ax, '(f) f(v - vg) zonal mean 12.5°N–17.5°N at 925 hPa', ylabel='fv minus Vgf')

# ==========================================
# Panel (g): Dynamic Balance Term (Term III - Term IV)
# ==========================================
ax = axes[2, 0]
for exp_key, label in EXPERIMENTS:
    file_path = f'{PATH_BALANCE}/vvg_mas_adv_{exp_key}.nc'
    lats, lons, _, uwnd = import_dataset(file_path, var_name='bal3')
    
    lons_mean, uwnd_mean = process_balance_term(lats, lons, uwnd, sigma=6, lon_min=-63, lon_max=-59)
    
    ax.plot(lons_mean, uwnd_mean, label=label)

setup_subplot_style(ax, '(g) Dynamic balance zonal mean 12.5°N–17.5°N at 925 hPa', ylabel='TermIII minus TermIV')

# ==========================================
# Hide Unused Subplots (3x3 Grid cleanup)
# ==========================================
axes[2, 1].set_visible(False)
axes[2, 2].set_visible(False)

# Save and Display
plt.tight_layout()
plt.savefig('figs/dynamics_terms_3x3_grid.png', dpi=400, bbox_inches='tight')
plt.show()
