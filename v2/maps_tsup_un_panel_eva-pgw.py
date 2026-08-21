#!/usr/bin/env python
# coding: utf-8

# In[1]:

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com"
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plots temperature maps"

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from mpl_toolkits.basemap import Basemap

# Map bounds and configuration
latlon = [-85.5, -47, 8, 27.5]
path = "/home/netapp-clima-users/users/jsalinas/Sim_RegCM/tsuperficial"  # Path

subdomains = {
    ".": (13, 16, -71, -76),
}

# Plot limits & levels
mi2, md2 = 3.0, -3.0
mi, md = 22, 34


def import_data(exp):
    ds = xr.open_dataset("{0}/prom-tas-K_{1}.nc".format(path, exp))

    lats = ds.variables["lat"][:]
    lons = ds.variables["lon"][:]
    time = ds.variables["time"][:]
    uwnd = ds.variables["tas"][:]

    return lats, lons, uwnd


def draw_subdomain_boxes(ax, mp, subdomains):
    """Helper to draw bounding boxes for defined subdomains."""
    for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
        lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
        lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

        x_box, y_box = mp(lons_box, lats_box)
        ax.plot(x_box, y_box, color="black", linewidth=0.5)

        x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
        ax.text(
            x_txt,
            y_txt,
            name,
            color="black",
            fontsize=1,
            bbox=dict(facecolor="none", edgecolor="none"),
        )


def apply_map_features(mp):
    """Helper to draw map gridlines and boundaries."""
    mp.drawcoastlines()
    mp.drawstates()
    mp.drawcountries()

    mp.drawmeridians(
        np.arange(-90, -40, 10),
        labels=[0, 0, 0, 1],
        fontsize=6,
        linewidth=0.1,
    )
    mp.drawparallels(
        np.arange(0, 30, 10),
        labels=[1, 0, 0, 0],
        fontsize=6,
        linewidth=0.1,
    )


# Import data
lats, lons, uwnd_jun_jul_80_17_eva = import_data("jun-jul-1980-2017_eva")
lats, lons, uwnd_ago_oct_80_17_eva = import_data("ago-oct-1980-2017_eva")
lats, lons, uwnd_jun_jul_80_17_pgw = import_data("jun-jul-1980-2017_pgw")
lats, lons, uwnd_ago_oct_80_17_pgw = import_data("ago-oct-1980-2017_pgw")
lats, lons, uwnd_jun_jul_diff = import_data("jun-jul-1980-2017_diff")
lats, lons, uwnd_ago_oct_diff = import_data("ago-oct-1980-2017_diff")

# Initialize Basemap Projection
mp = Basemap(
    projection="merc",
    llcrnrlon=-85.5,
    llcrnrlat=8,
    urcrnrlon=-47,
    urcrnrlat=27.5,
    resolution="i",
)
x, y = mp(lons, lats)
lon, lat = np.array(x), np.array(y)

# Plot figure 
fig = plt.figure(figsize=(13.5, 5))

# Subplot 1
ax = fig.add_subplot(2, 3, 1)
c_scheme = mp.pcolor(x, y, np.squeeze(uwnd_jun_jul_80_17_eva[0, :, :]), cmap="hot_r", vmin=mi, vmax=md)
Z = np.array(np.squeeze(uwnd_jun_jul_80_17_eva[0, :, :]))
mp.contour(lon, lat, Z, levels=[28], colors="k", linewidths=0.4, linestyles="solid")
plt.title("(a) Jun-Jul Evaluation")
apply_map_features(mp)
cbar = mp.colorbar(c_scheme, location="right", pad="2%")
cbar.ax.tick_params(labelsize=6)
draw_subdomain_boxes(ax, mp, subdomains)

# Subplot 2
ax = fig.add_subplot(2, 3, 2)
c_scheme = mp.pcolor(x, y, np.squeeze(uwnd_jun_jul_80_17_pgw[0, :, :]), cmap="hot_r", vmin=mi, vmax=md)
Z = np.array(np.squeeze(uwnd_jun_jul_80_17_pgw[0, :, :]))
mp.contour(lon, lat, Z, levels=[28], colors="k", linewidths=0.4, linestyles="solid")
plt.title("(b) Jun-Jul PGW")
apply_map_features(mp)
cbar = mp.colorbar(c_scheme, location="right", pad="2%")
cbar.ax.tick_params(labelsize=6)
draw_subdomain_boxes(ax, mp, subdomains)

# Subplot 3
ax = fig.add_subplot(2, 3, 3)
c_scheme = mp.pcolor(x, y, np.squeeze(uwnd_jun_jul_diff[0, :, :]), cmap="bwr", vmin=mi2, vmax=md2)
Z = np.array(np.squeeze(uwnd_jun_jul_diff[0, :, :]))
mp.contour(lon, lat, Z, levels=[1.2], colors="k", linewidths=0.4, linestyles="solid")
plt.title("(c) Difference")
apply_map_features(mp)
cbar = mp.colorbar(c_scheme, location="right", pad="2%")
cbar.ax.tick_params(labelsize=6)
draw_subdomain_boxes(ax, mp, subdomains)

# Subplot 4
ax = fig.add_subplot(2, 3, 4)
c_scheme = mp.pcolor(x, y, np.squeeze(uwnd_ago_oct_80_17_eva[0, :, :]), cmap="hot_r", vmin=mi, vmax=md)
Z = np.array(np.squeeze(uwnd_ago_oct_80_17_eva[0, :, :]))
mp.contour(lon, lat, Z, levels=[28], colors="k", linewidths=0.4, linestyles="solid")
plt.title("(d) Aug-Oct Evaluation")
apply_map_features(mp)
cbar = mp.colorbar(c_scheme, location="right", pad="2%")
cbar.ax.tick_params(labelsize=6)
draw_subdomain_boxes(ax, mp, subdomains)

# Subplot 5
ax = fig.add_subplot(2, 3, 5)
c_scheme = mp.pcolor(x, y, np.squeeze(uwnd_ago_oct_80_17_pgw[0, :, :]), cmap="hot_r", vmin=mi, vmax=md)
Z = np.array(np.squeeze(uwnd_ago_oct_80_17_pgw[0, :, :]))
mp.contour(lon, lat, Z, levels=[28], colors="k", linewidths=0.4, linestyles="solid")
plt.title("(e) Aug-Oct PGW")
apply_map_features(mp)
cbar = mp.colorbar(c_scheme, location="right", pad="2%")
cbar.ax.tick_params(labelsize=6)
draw_subdomain_boxes(ax, mp, subdomains)

# Subplot 6
ax = fig.add_subplot(2, 3, 6)
c_scheme = mp.pcolor(x, y, np.squeeze(uwnd_ago_oct_diff[0, :, :]), cmap="bwr", vmin=mi2, vmax=md2)
Z = np.array(np.squeeze(uwnd_ago_oct_diff[0, :, :]))
mp.contour(lon, lat, Z, levels=[1.2], colors="k", linewidths=0.4, linestyles="solid")
plt.title("(f) Difference")
apply_map_features(mp)
cbar = mp.colorbar(c_scheme, location="right", pad="2%")
cbar.ax.tick_params(labelsize=6)
draw_subdomain_boxes(ax, mp, subdomains)

# Save figure 
plt.savefig("figs/tsuperf-subplotseva-pgw.png", dpi=400, bbox_inches="tight")
plt.show()
exit()
