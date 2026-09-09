# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Sept 09, 2026"
__description__ = "This script plot map of track density"

import os
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Define specific paths
path_txt_era5 = "/home/mda_silv/users/Reale_Lionello/ERA5"
path_txt_regcm = "/home/mda_silv/users/Reale_Lionello/RegCM5"
path_out = "/home/mda_silv/users/Reale_Lionello/figs"

# Define dark high-contrast colors for tracks (Jun, Jul, Aug, Sep, Oct)
MONTH_COLORS = {
    6: "#00008B",  # Jun - Dark Blue
    7: "#006400",  # Jul - Dark Green
    8: "#4B0082",  # Aug - Indigo / Dark Purple
    9: "#D95F02",  # Sep - Dark Orange
    10: "#8B0000",  # Oct - Dark Red
}

MONTH_NAMES = {6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct"}


def import_dataset(file_path):

    # Read space-delimited tracking file without predefined headers
    df = pd.read_csv(file_path, sep=r"\s+", header=None, engine="python")

    # Map column positions: Col 0: ID, Col 1: Date string, Col 6: Lon, Col 7: Lat, Col 8: SLP
    df = df.iloc[:, [0, 1, 6, 7, 8]]
    df.columns = ["id", "data", "lon", "lat", "slp"]

    # Format datetime
    df["data"] = pd.to_datetime(
        df["data"].astype(str), format="%Y%m%d%H", errors="coerce"
    )

    # Filter for year 2005 and months JUN to OCT (6 to 10)
    df = df[
        (df["data"].dt.year == 2005) & (df["data"].dt.month.isin([6, 7, 8, 9, 10]))
    ]

    # Convert Longitude from [0, 360] to [-180, 180] range
    df["lon"] = np.where(df["lon"] > 180, df["lon"] - 360, df["lon"])

    return df


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

        # Color determined by the month of cyclogenesis (start of track)
        start_month = track["data"].iloc[0].month
        track_color = MONTH_COLORS.get(start_month, "black")

        # Plot line trajectory
        ax.plot(
            track["lon"],
            track["lat"],
            color=track_color,
            linewidth=2.0,
            alpha=0.9,
            zorder=3,
            transform=ccrs.PlateCarree(),
        )

        # Plot cyclogenesis start marker
        ax.plot(
            track["lon"].iloc[0],
            track["lat"].iloc[0],
            marker="o",
            markersize=5,
            color=track_color,
            markeredgecolor="white",
            markeredgewidth=0.8,
            zorder=4,
            transform=ccrs.PlateCarree(),
        )

    ax.set_title(title_text, fontsize=11, fontweight="bold", loc="left")
    ax.set_xlabel("Longitude", fontsize=10, fontweight="bold")
    ax.set_ylabel("Latitude", fontsize=10, fontweight="bold")
    configure_subplot(ax)


# Load datasets
file_era5 = os.path.join(path_txt_era5, "REALE_LIONELLO_tracks_ERA5_2005.txt")
file_regcm = os.path.join(
    path_txt_regcm, "REALE_LIONELLO_tracks_RegCM5_2005.txt"
)

era5_tracks = import_dataset(file_era5)
regcm_tracks = import_dataset(file_regcm)

# Plotting 2 subplots
fig, (ax1, ax2) = plt.subplots(
    1,
    2,
    figsize=(16, 6),
    subplot_kw={"projection": ccrs.PlateCarree()},
    constrained_layout=True,
)

# Plot panels
plot_tracks_by_month(ax1, era5_tracks, "(a) ERA5 (Jun\u2013Oct)")
plot_tracks_by_month(ax2, regcm_tracks, "(b) RegCM5 (Jun\u2013Oct)")

# Create Legend for Months
legend_handles = [
    mlines.Line2D(
        [],
        [],
        color=MONTH_COLORS[m],
        marker="o",
        markeredgecolor="white",
        markeredgewidth=0.8,
        markersize=6,
        linewidth=2,
        label=MONTH_NAMES[m],
    )
    for m in [6, 7, 8, 9, 10]
]
fig.legend(
    handles=legend_handles,
    loc="lower center",
    bbox_to_anchor=(0.5, 0.04),
    ncol=5,
    fontsize=10,
    frameon=True,
)

# Save figure
os.makedirs(path_out, exist_ok=True)
name_out = "pyplt_maps_cyclone_tracks_ERA5_RegCM5_JJASO.png"
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches="tight")
plt.show()
