# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Sept 09, 2026"
__description__ = "This script plot map of track density"

import os
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Define specific paths
path_txt_era5 = "/home/mda_silv/users/Reale_Lionello/ERA5"
path_txt_regcm_eval = "/home/mda_silv/users/Reale_Lionello/RegCM5"
path_txt_regcm_pgw = "/home/mda_silv/users/Reale_Lionello/PGW"
path_out = "/home/mda_silv/github_projects/TW-CLLJ/v2/figs"

# Define target years
years = [1980, 1988, 1995, 1996, 1998, 2004, 2005, 2007, 2008, 2017]


def import_dataset(file_path, target_years):

    # Read space-delimited tracking file without predefined headers
    df = pd.read_csv(file_path, sep=r"\s+", header=None, engine="python")

    # Map column positions: Col 0: ID, Col 1: Date string, Col 6: Lon, Col 7: Lat, Col 8: SLP
    df = df.iloc[:, [0, 1, 6, 7, 8]]
    df.columns = ["id", "data", "lon", "lat", "slp"]

    # Format datetime
    df["data"] = pd.to_datetime(
        df["data"].astype(str), format="%Y%m%d%H", errors="coerce"
    )

    # Filter for target years and months JUN to OCT (6 to 10)
    df = df[
        (df["data"].dt.year.isin(target_years))
        & (df["data"].dt.month.isin([6, 7, 8, 9, 10]))
    ]

    # Convert Longitude from [0, 360] to [-180, 180] range
    df["lon"] = np.where(df["lon"] > 180, df["lon"] - 360, df["lon"])

    return df


def load_all_years(path_dir, file_prefix, years_list):
    df_list = []
    for yr in years_list:
        file_path = os.path.join(path_dir, f"{file_prefix}_{yr}.txt")
        if os.path.exists(file_path):
            df_year = import_dataset(file_path, [yr])
            # Assign unique ID per year so cyclone IDs from different years don't merge
            df_year["id"] = str(yr) + "_" + df_year["id"].astype(str)
            df_list.append(df_year)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return pd.DataFrame()


def configure_subplot(ax):
    states_provinces = cfeat.NaturalEarthFeature(
        category="cultural",
        name="admin_1_states_provinces_lines",
        scale="50m",
        facecolor="none",
    )

    # Add background features: Light blue ocean and light brown land
    ax.add_feature(cfeat.OCEAN, facecolor="#D4E6F1", zorder=0)
    ax.add_feature(cfeat.LAND, facecolor="#F5E6D3", zorder=0)

    # Set map view bounds for the target domain
    ax.set_extent([-85, -47, 8, 27], crs=ccrs.PlateCarree())
    ax.set_xticks(np.arange(-85, -45, 10), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(8, 28, 5), crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.grid(c="k", ls="--", alpha=0.3, zorder=2)
    ax.add_feature(cfeat.BORDERS, zorder=2)
    ax.add_feature(states_provinces, edgecolor="0.25", zorder=2)
    ax.coastlines(zorder=2)


def plot_tracks_by_month(ax, df, title_text):
    cyclone_ids = df["id"].unique()

    for c_id in cyclone_ids:
        track = df[df["id"] == c_id].sort_values("data")

        # Plot line trajectory in black
        ax.plot(
            track["lon"],
            track["lat"],
            color="gray",
            linewidth=1.0,
            alpha=0.9,
            zorder=3,
            transform=ccrs.PlateCarree(),
        )

        # Plot cyclogenesis start marker: Green asterisk (*) inside
        ax.plot(
            track["lon"].iloc[0],
            track["lat"].iloc[0],
            marker="*",
            markersize=5,
            color="green",
            zorder=5,
            transform=ccrs.PlateCarree(),
        )

    ax.set_title(title_text, fontsize=11, fontweight="bold", loc="left")
    ax.set_xlabel("Longitude", fontsize=10, fontweight="bold")
    ax.set_ylabel("Latitude", fontsize=10, fontweight="bold")
    configure_subplot(ax)


# Load all datasets across all years
era5_tracks = load_all_years(path_txt_era5, "REALE_LIONELLO_tracks_ERA5", years)
regcm_tracks_eval = load_all_years(path_txt_regcm_eval, "REALE_LIONELLO_tracks_RegCM5", years)
regcm_tracks_pgw = load_all_years(path_txt_regcm_pgw, "REALE_LIONELLO_tracks_RegCM5", years)

# Plotting 2 subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={"projection": ccrs.PlateCarree()}, constrained_layout=True,)

# Plot panels
plot_tracks_by_month(ax1, era5_tracks, "(a) ERA5 (Jun\u2013Oct)")
plot_tracks_by_month(ax2, regcm_tracks_eval, "(b) RegCM5 EVAL (Jun\u2013Oct)")
plot_tracks_by_month(ax3, regcm_tracks_pgw, "(c) RegCM5 PGW (Jun\u2013Oct)")

# Save figure
os.makedirs(path_out, exist_ok=True)
name_out = "pyplt_maps_cyclone_tracks_ERA5_RegCM5_JJASO.png"
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches="tight")
plt.show()
