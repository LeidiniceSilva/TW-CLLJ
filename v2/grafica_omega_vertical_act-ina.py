#!/usr/bin/env python
# coding: utf-8

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com"
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plots vertical velocity cross-sections"

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

path = '/home/netapp-clima-users/users/jsalinas/ERA5_data/vel_vertical'

subdomains = {
    ".": (13, 16, -71, -76),
}

def import_data(exp):
    ds = xr.open_dataset(f'{path}/prom-wwnd_{exp}.nc')
    lats = ds['latitude']
    lons = ds['longitude']
    levs = ds['pressure_level']
    ds = ds.assign_coords(lons=((ds.longitude + 180) % 360) - 180)
    ds = ds.sortby("lons")
    uwnd = ds['w']
    return lats, lons, levs, uwnd

# Setup subplots grid configuration
experiments = [
    ('jun-jul_act_r', '(a) Jun-Jul Active', -0.1, 0.1),
    ('jun-jul_ina_r', '(b) Jun-Jul Inactive', -0.1, 0.1),
    ('jun-jul_diff_r', '(c) Difference', -0.03, 0.03),
    ('ago-oct_act_r', '(d) Aug-Oct Active', -0.1, 0.1),
    ('ago-oct_ina_r', '(e) Aug-Oct Inactive', -0.1, 0.1),
    ('ago-oct_diff_r', '(f) Difference', -0.03, 0.03)
]

fig, axes = plt.subplots(2, 3, figsize=(16, 10), sharex=True, sharey=True)
axes = axes.flatten()

# Box coordinates for CCC
p_top, p_bot = 875, 975
lon_min, lon_max = -71, -76

for i, (exp_name, title, vmin, vmax) in enumerate(experiments):
    ax = axes[i]
    lats, lons, levs, uwnd_data = import_data(exp_name)
    
    lon_lev = uwnd_data.sel(latitude=slice(17.5, 12.5)).mean(dim="latitude").isel(time=0)
    
    # Adjust longitude coordinates
    lon = lon_lev.longitude.values
    lon_w = lon.copy()
    lon_w[lon > 180] -= 360
    idx = np.argsort(lon_w)
    lon_w = lon_w[idx]
    
    lon_lev = lon_lev.assign_coords(lon_w=("longitude", lon_w))
    
    # Plot cross section with extend='neither' to clean colorbar ends
    p = lon_lev.plot(
        ax=ax,
        x="lon_w",
        y="pressure_level",
        cmap="bwr",
        vmin=vmin,
        vmax=vmax,
        yincrease=False,
        add_colorbar=True,
        cbar_kwargs={
            'extend': 'neither', 
            'label': 'w (Pa/s)' if i in [2, 5] else ''
        }
    )
    
    # Zero contour line
    vert_dim = lon_lev.dims[0]
    lev = lon_lev[vert_dim].values
    Z = lon_lev.values
    ax.contour(lon_w, lev, Z, levels=[0], colors='k', linewidths=0.5)
    
    # Add CCC box overlay
    rect = Rectangle(
        (lon_min, p_top),
        lon_max - lon_min,
        p_bot - p_top,
        fill=False,
        edgecolor='black',
        linewidth=0.8,
        zorder=10
    )
    ax.add_patch(rect)
    
    # Formatting subplots
    ax.set_title(title)
    ax.set_xlabel('Longitude' if i >= 3 else '')
    ax.set_ylabel('Pressure Level (hPa)' if i % 3 == 0 else '')

plt.tight_layout()
plt.savefig('figs/Vel_vert-subplots-act-ina.png', dpi=400, bbox_inches='tight')
plt.show()
exit()
