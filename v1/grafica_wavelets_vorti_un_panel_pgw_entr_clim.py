#!/usr/bin/env python
# coding: utf-8

# In[1]:

import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from mpl_toolkits.basemap import Basemap
from scipy.ndimage import gaussian_filter
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from scipy.stats import gaussian_kde
import pycwt as wavelet
from pycwt.helpers import find
from matplotlib.ticker import ScalarFormatter
import matplotlib.dates as mdates

latlon = [-85.5, -47, 8, 27.5]

#grad_meridional-jun-jul_eva_925.nc
#grad_meridional-ago-oct_pgw_925.nc
#grad_meridional-jun-jul_diff_925.nc
path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/wavelets/vorticity/pgw' # Path

subdomains = {
    ".": (13, 16,  -71, -76),}


def import_data(exp):

    ds = xr.open_dataset(
        '{0}/vor925_day_{1}.nc'.format(path, exp)
    )

    if 'lat' in ds:
        lats = ds['lat']
    else:
        lats = ds['latitude']

    if 'lon' in ds:
        lons = ds['lon']
    else:
        lons = ds['longitude']

    va925 = ds['vo']

    time = ds['time']

    return time, lats, lons, va925


# Define Entrance": (13.5, 16,  -62, -67),
lat_min, lat_max = 13, 16
lon_min, lon_max = -67, -62

# ============================
# Wavelet
# ============================

def calcular_wavelet(exp):

    print("Procesando:", exp)

    time, lats, lons, datos_viento = import_data(exp)


    # -----------------------------
    # Región de interés
    # -----------------------------
    if lons.max() > 180:
        lon1 = 360 + lon_min
        lon2 = 360 + lon_max
    else:
        lon1 = lon_min
        lon2 = lon_max


    if lats.ndim == 1:

        datos = datos_viento.sel(
            lat=slice(lat_min, lat_max),
            lon=slice(lon1, lon2)
        )

    else:

        mascara = (
            (lats >= lat_min) &
            (lats <= lat_max) &
            (lons >= lon1) &
            (lons <= lon2)
        )

        datos = datos_viento.where(mascara)
    # -----------------------------
    # Promedio espacial
    # -----------------------------

    if "lat" in datos.dims:

        serie = datos.mean(
            dim=("lat","lon")
        )

    elif "latitude" in datos.dims:

        serie = datos.mean(
            dim=("latitude","longitude")
        )

    else:

        serie = datos.mean(
            dim=("y","x")
        )


    serie = serie.values

    serie = serie[np.isfinite(serie)]


    # -----------------------------
    # Normalizar serie
    # -----------------------------

    serie = serie - serie.mean()
    serie = serie / serie.std()


    # -----------------------------
    # Wavelet Morlet
    # -----------------------------

    dt = 1.0

    mother = wavelet.Morlet(6)

    periodo_min = 2
    periodo_max = 15

    s0 = periodo_min
    dj = 1/12

    J = int(
        np.log2(periodo_max/s0)/dj
    )


    alpha, _, _ = wavelet.ar1(serie)


    wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(
        serie,
        dt,
        dj=dj,
        s0=s0,
        J=J,
        wavelet=mother
    )


    power = np.abs(wave)**2

    period = 1/freqs



    # -----------------------------
    # Significancia 95 %
    # -----------------------------

    signif, fft_theor = wavelet.significance(
        1.0,
        dt,
        scales,
        0,
        alpha,
        significance_level=0.95,
        wavelet=mother
    )


    sig95 = power / signif[:, None]


    return power, period, coi, sig95




# =====================================================
# Lista de experimentos/archivos a procesar
# =====================================================

experimentos = [
    'jun-oct-clim_entr',
]




# =====================================================
# Figura general: 10 wavelets en 
# =====================================================


fig, ax = plt.subplots(
    nrows=1,
    ncols=1,
    figsize=(10, 8),
    sharex=True,
    sharey=True
)

vmin = 0
vmax = 5

for i, exp in enumerate(experimentos):
    power, period, coi, sig95 = calcular_wavelet(exp)

    levels = np.linspace(
        vmin,
        vmax,
        30
    )



######################


    cf = ax.contourf(
        np.arange(power.shape[1]),
        period,
        power,
        levels=levels,
        cmap="Spectral_r",
        extend="both"
    )


    # significancia 95 %

    ax.contour(
        np.arange(power.shape[1]),
        period,
        sig95,
        levels=[1],
        colors="black",
        linewidths=1
    )


    # cono de influencia

    ax.fill_between(
        np.arange(power.shape[1]),
        coi,
        period.max(),
        color="white",
        alpha=0.5,
        hatch="//"
    )

    # escala log pero etiquetas normales

    ax.set_yscale("log")

    ax.set_ylim(
        15,
        2
    )

    ax.set_yticks(
        [2,3,4,5,6,8,10,12,15]
    )

    ax.yaxis.set_major_formatter(
        ScalarFormatter()
    )


    # meses

    ax.set_xticks(
        [0,30,61,92,122]
    )

    ax.set_xticklabels(
        ['Jun','Jul','Aug','Sep','Oct']
    )


    ax.set_title(
        exp.replace("jun-oct-",""),
        fontsize=12
    )

    if i % 2 == 0:
        ax.set_ylabel(
            "Period (days)"
        )


    if i >= 8:
        ax.set_xlabel(
            "Time"
        )


# barra de colores común

# Barra de colores a la derecha sin tapar paneles

fig.subplots_adjust(
    right=0.88,
    hspace=0.25,
    wspace=0.15
)

cbar_ax = fig.add_axes(
    [0.91, 0.15, 0.02, 0.70]
)

cbar = fig.colorbar(
    cf,
    cax=cbar_ax
)

cbar.set_label(
    "Normalized wavelet power of 925-hPa vorticity"
)

plt.tight_layout(rect=[0,0,0.88,1])


plt.savefig(
    "wavelets_vorti_clim_entr_pgw.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()


####################Fin de lo traido para wavelets  #####

exit()

############################################
