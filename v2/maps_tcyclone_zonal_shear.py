#!/usr/bin/env python
# coding: utf-8
 
# In[1]:

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot mean zonal shear"

import os
import glob
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from scipy.ndimage import gaussian_filter

BASE = "/home/netapp-clima-scratch/jsalinas/wind_shear"
EXPS = {
    "Evaluation": dict(
        wind_dir=f"{BASE}/evaluation",
        track_dir="/home/mda_silv/github_projects/TW-CLLJ/v2/track/RegCM5"),
    "PGW": dict(
        wind_dir=f"{BASE}/pgw",
        track_dir="/home/mda_silv/github_projects/TW-CLLJ/v2/track/PGW"),
}
# one row per season: label, {month number: month name in the file names}, panel letters
SEASONS = [
    ("Jun-Jul", {6: "jun", 7: "jul"}, "abc"),
    ("Aug-Oct", {8: "ago", 9: "sep", 10: "oct"}, "def"),
]
OUTDIR = "/home/mda_silv/github_projects/TW-CLLJ/v2/figs"  # folder where the figure is saved
YEARS = [1980, 1988, 1995, 1996, 1998, 2004, 2005, 2007, 2008, 2017]
COLS = ["track_id", "stamp", "year", "month", "day", "hour", "lon", "lat", "pres"]
LON_NAMES, LAT_NAMES = ("lon", "xlon", "longitude"), ("lat", "xlat", "latitude")

subdomains = {
    ".": (13, 16, -71, -76), }


def open_u(wind_dir, level, name, year):
    ds = xr.open_dataset(f"{wind_dir}/ua{level}/ua{level}_6hr_{name}-{year}_clean.nc")
    lon = ds[next(n for n in LON_NAMES if n in ds.variables)]
    lat = ds[next(n for n in LAT_NAMES if n in ds.variables)]
    skip = {lon.name, lat.name}
    var = "ua" if "ua" in ds else next(v for v in ds.data_vars if v not in skip and ds[v].ndim >= 3)
    return ds[var].squeeze(), lon.values, lat.values


def track_file(track_dir, year):
    """Find the track file of a given year (the PGW file name may differ from the evaluation one)."""
    files = sorted(glob.glob(f"{track_dir}/*{year}*.txt"))
    if not files:
        raise FileNotFoundError(f"No track file for {year} in {track_dir}")
    return files[0]


def mean_shear(wind_dir, track_dir, months):
    """Mean (ua200 - ua850) over all 6-hourly times with a TC in the given months, all years."""
    total, count = 0.0, 0
    lon2d = lat2d = None
    for year in YEARS:
        trk = pd.read_csv(track_file(track_dir, year), sep=r"\s+", header=None, names=COLS)
        for month, name in months.items():
            pts = trk[trk["month"] == month]
            if pts.empty:
                continue
            u200, lon2d, lat2d = open_u(wind_dir, 200, name, year)
            u850, _, _ = open_u(wind_dir, 850, name, year)

            tc_times = pd.to_datetime(pts["stamp"].astype(str).unique(), format="%Y%m%d%H")
            sel = xr.DataArray(tc_times.values, dims="time")
            shear = u200.sel(time=sel, method="nearest").values - u850.sel(time=sel, method="nearest").values

            total = total + np.nansum(shear, axis=0)
            count += shear.shape[0]
    return lon2d, lat2d, total / count, count


# Plot 
mi = -2    # Evaluation and PGW
md = 20
mi2 = -4    # Difference
md2 = 4
step = 4    # contour interval, Evaluation and PGW
step2 = 1   # contour interval, Difference
sigma = 3  # smoothness, try 1-3

# Defining the map
mp = Basemap(projection='merc', llcrnrlon=-85.5, llcrnrlat=8, urcrnrlon=-47, urcrnrlat=27.5, resolution='i')

# Panels in plotting order (row by row): (title, lons, lats, field, vmin, vmax)
panels = []
for season, months, letters in SEASONS:
    fields = {}
    for exp, cfg in EXPS.items():
        lons, lats, Z, n = mean_shear(cfg["wind_dir"], cfg["track_dir"], months)
        print(f"{season} {exp}: {n} TC times")
        fields[exp] = Z
    panels.append((f"({letters[0]}) {season} Evaluation", lons, lats, fields["Evaluation"], mi, md, 'hot_r', step))
    panels.append((f"({letters[1]}) {season} PGW", lons, lats, fields["PGW"], mi, md, 'hot_r', step))
    # Difference: PGW - Evaluation
    panels.append((f"({letters[2]}) Difference", lons, lats, fields["PGW"] - fields["Evaluation"], mi2, md2, 'bwr', step2))

fig = plt.figure(figsize=(13.5, 5))  # figure size

for i, (title, lons, lats, Z, vmin, vmax, cmap, dc) in enumerate(panels, start=1):
    x, y = mp(lons, lats)  # mapping them together

    ax = fig.add_subplot(len(SEASONS), 3, i)

    Z_smooth = gaussian_filter(Z, sigma=sigma).squeeze()
    c_scheme = mp.pcolormesh(x, y, Z_smooth, cmap=cmap, vmin=vmin, vmax=vmax, ax=ax)
    # contour lines (zero excluded) and highlighted zero contour
    levels = np.arange(vmin, vmax + dc, dc)
    mp.contour(x, y, Z_smooth, levels=[0], colors='k', linewidths=0.3, linestyles='solid', ax=ax)

    ax.set_title(title)
    mp.drawcoastlines(ax=ax)
    mp.drawstates(ax=ax)
    mp.drawcountries(ax=ax)

    cbar = mp.colorbar(c_scheme, location='right', pad='2%', ax=ax)  # map information
    cbar.ax.tick_params(labelsize=6)

    mp.drawmeridians(np.arange(-90, -40, 10), labels=[0, 0, 0, 1], fontsize=6, linewidth=0.1, ax=ax)
    mp.drawparallels(np.arange(0, 30, 5), labels=[1, 0, 0, 0], fontsize=6, linewidth=0.1, ax=ax)

    # Draw boxes for subdomains
    for name, (lat_min, lat_max, lon_min, lon_max) in subdomains.items():
        lats_box = [lat_min, lat_max, lat_max, lat_min, lat_min]
        lons_box = [lon_min, lon_min, lon_max, lon_max, lon_min]

        x_box, y_box = mp(lons_box, lats_box)
        ax.plot(x_box, y_box, color='black', linewidth=0.5)

        x_txt, y_txt = mp(lon_min + 0.5, lat_max - 0.5)
        ax.text(x_txt, y_txt, name,
                color='black', fontsize=1,
                bbox=dict(facecolor='none', edgecolor='none'))

os.makedirs(OUTDIR, exist_ok=True)
plt.savefig(os.path.join(OUTDIR, "maps_zonal_shear_tc_cllj.png"), dpi=400, bbox_inches='tight')
plt.show()
