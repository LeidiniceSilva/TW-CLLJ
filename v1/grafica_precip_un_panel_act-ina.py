#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com"
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plots precipitation maps"

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap, BoundaryNorm

# Custom Precipitation Colors (Starts explicitly with white)
color_precip = [
    '#ffffff', '#d7f0fc', '#ade0f7', '#86c4eb', '#60a5d6',
    '#4794b3', '#49a67c', '#55b848', '#9ecf51', '#ebe359',
    '#f7be4a', '#f58433', '#ed5a28', '#de3728', '#cc1f27'
]
cmap_precip = ListedColormap(color_precip)

# Define levels matching the number of colors precisely
levels_precip = [0, 0.5, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 30]
norm_precip = BoundaryNorm(levels_precip, ncolors=cmap_precip.N)

# Difference Colormap (BrBG)
cmap_diff = 'BrBG'
levels_diff = [-4, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 4]
norm_diff = colors.TwoSlopeNorm(vcenter=0, vmin=-4, vmax=4)

path = '/home/netapp-clima-users/users/jsalinas/ERA5_data/precipitation'

subdomains = {
    ".": (13, 16, 289, 284),
}

def import_data(exp):
    ds = xr.open_dataset(f'{path}/prom_pr_{exp}.nc')
    lats = ds.variables['latitude'][:]
    lons = ds.variables['longitude'][:]
    uwnd = ds.variables['tp'][:]
    return lats, lons, uwnd

# Subplot configuration: (exp_name, title, is_difference)
panels = [
    ('jun-jul_mm_act', '(a) Jun-Jul Active', False),
    ('jun-jul_mm_ina', '(b) Jun-Jul Inactive', False),
    ('jun-jul_mm_diff', '(c) Difference', True),
    ('ago-oct_mm_act', '(d) Aug-Oct Active', False),
    ('ago-oct_mm_ina', '(e) Aug-Oct Inactive', False),
    ('ago-oct_mm_diff', '(f) Difference', True)
]

fig = plt.figure(figsize=(13.5,5))

for i, (exp, title, is_diff) in enumerate(panels, 1):
    ax = fig.add_subplot(2, 3, i)
    lats, lons, uwnd = import_data(exp)
    
    mp = Basemap(projection='merc', llcrnrlon=274.5, llcrnrlat=8, urcrnrlon=313, urcrnrlat=27.5, resolution='i')
    lon, lat = np.meshgrid(lons, lats)
    x, y = mp(lon, lat)
    Z = np.squeeze(uwnd[0, :, :])

    if is_diff:
        cf = mp.contourf(
            x, y, Z,
            levels=levels_diff,
            cmap=cmap_diff,
            norm=norm_diff,
            extend='both'
        )
        mp.contour(x, y, Z, levels=[0], colors='k', linewidths=0.4, linestyles='solid')
    else:
        cf = mp.contourf(
            x, y, Z,
            levels=levels_precip,
            cmap=cmap_precip,
            norm=norm_precip,
            extend='max'
        )
        mp.contour(x, y, Z, levels=[4], colors='k', linewidths=0.4, linestyles='solid')

    plt.title(title)
    mp.drawcoastlines(linewidth=0.5)
    mp.drawstates(linewidth=0.3)
    mp.drawcountries(linewidth=0.5)

    cbar = mp.colorbar(cf, location='right', pad='3%')
    cbar.ax.tick_params(labelsize=7)

    mp.drawmeridians(np.arange(-90, -40, 10), labels=[0, 0, 0, 1] if i >= 4 else [0, 0, 0, 0], fontsize=6, linewidth=0.1)
    mp.drawparallels(np.arange(0, 30, 5), labels=[1, 0, 0, 0] if i % 3 == 1 else [0, 0, 0, 0], fontsize=6, linewidth=0.1)

    # Draw subdomain boxes
    for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
        lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
        lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]
        x_box, y_box = mp(lons_box, lats_box)
        ax.plot(x_box, y_box, color='black', linewidth=0.6)

plt.tight_layout()
plt.savefig('figs/Precip-subplot-act-ina.png', dpi=400, bbox_inches='tight')
plt.show()
exit()
