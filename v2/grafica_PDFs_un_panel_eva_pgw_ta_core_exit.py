# coding: utf-8

__author__      = "Antonio Salinas"
__email__       = "salinasprieto60@gmail.com "
__credits__     = "Leidinice Silva"
__date__        = "Jul 28, 2026"
__description__ = "This script plot PDFs"

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


latlon = [-85.5, -47, 8, 27.5]

path = '/home/netapp-clima-users/users/jsalinas/Sim_RegCM/PDFs/ta925' # Path

subdomains = {
    ".": (13, 16, -71, -76),
}


def import_data(exp):

    ds = xr.open_dataset('{0}/ta925_day_{1}.nc'.format(path, exp))

    # A veces es lat y a veces latitude
    if 'lat' in ds:
        lats = ds['lat']
    elif 'latitude' in ds:
        lats = ds['latitude']
    else:
        raise ValueError("No se encontró la variable de latitud")

    if 'lon' in ds:
        lons = ds['lon']
    elif 'longitude' in ds:
        lons = ds['longitude']
    else:
        raise ValueError("No se encontró la variable de longitud")

    uwnd = ds['ta925']
    return lats, lons, uwnd


# ============================
# Cargar datos Code 1: Core
# ============================
lats_core, lons_core, uwnd_jun_jul_80_17_eva_core = import_data('jun-jul-eva_coreC')
lats_core, lons_core, uwnd_ago_oct_80_17_eva_core = import_data('ago-oct-eva_coreC')
lats_core, lons_core, uwnd_jun_jul_80_17_pgw_core = import_data('jun-jul-pgw_coreC')
lats_core, lons_core, uwnd_ago_oct_80_17_pgw_core = import_data('ago-oct-pgw_coreC')
lats_core, lons_core, uwnd_jun_jul_80_17_ERA5_core = import_data('jun-jul-ERA5_coreC')
lats_core, lons_core, uwnd_ago_oct_80_17_ERA5_core = import_data('ago-oct-ERA5_coreC')

# Región Core
lat_min_core, lat_max_core = 13, 16
lon_min_core, lon_max_core = -76, -71

if lons_core.max() > 180:
    lon_min_core = 360 + lon_min_core
    lon_max_core = 360 + lon_max_core


# ============================
# Cargar datos Code 2: Exit
# ============================
lats_exit, lons_exit, uwnd_jun_jul_80_17_eva_exit = import_data('jun-jul-eva_exitC')
lats_exit, lons_exit, uwnd_ago_oct_80_17_eva_exit = import_data('ago-oct-eva_exitC')
lats_exit, lons_exit, uwnd_jun_jul_80_17_pgw_exit = import_data('jun-jul-pgw_exitC')
lats_exit, lons_exit, uwnd_ago_oct_80_17_pgw_exit = import_data('ago-oct-pgw_exitC')
lats_exit, lons_exit, uwnd_jun_jul_80_17_ERA5_exit = import_data('jun-jul-ERA5_exitC')
lats_exit, lons_exit, uwnd_ago_oct_80_17_ERA5_exit = import_data('ago-oct-ERA5_exitC')

# Región Exit
lat_min_exit, lat_max_exit = 13, 16
lon_min_exit, lon_max_exit = -83, -78

if lons_exit.max() > 180:
    lon_min_exit = 360 + lon_min_exit
    lon_max_exit = 360 + lon_max_exit


# ============================
# Función para calcular PDF promedio
# ============================

def mean_pdf_region(data, lats, lons,
                    lat_min, lat_max,
                    lon_min, lon_max):

    # máscara espacial
    mask = (
        (lats >= lat_min) &
        (lats <= lat_max) &
        (lons >= lon_min) &
        (lons <= lon_max)
    )

    iy, ix = np.where(mask.values)

    print("Número de puntos de malla:", len(iy))

    # Indexado correcto: pares (y,x)
    puntos = xr.DataArray(
        np.arange(len(iy)),
        dims="points"
    )
    yy = xr.DataArray(iy, dims="points")
    xx = xr.DataArray(ix, dims="points")

    dims = data.dims

    ydim = 'y' if 'y' in dims else 'latitude'
    xdim = 'x' if 'x' in dims else 'longitude'

    datos_region = data.isel({ydim: yy, xdim: xx})
    valores = datos_region.values.ravel()

    valores = valores[np.isfinite(valores)]

    print("Número de datos usados:", len(valores))

    # KDE regional
    x = np.linspace(
        valores.min(),
        valores.max(),
        250
    )

    kde = gaussian_kde(valores)

    pdf = kde(x)

    return x, pdf


# ============================
# Calcular PDFs: Core
# ============================
x1_core, pdf1_core = mean_pdf_region(
    uwnd_jun_jul_80_17_eva_core,
    lats_core, lons_core,
    lat_min_core, lat_max_core,
    lon_min_core, lon_max_core
)

x2_core, pdf2_core = mean_pdf_region(
    uwnd_ago_oct_80_17_eva_core,
    lats_core, lons_core,
    lat_min_core, lat_max_core,
    lon_min_core, lon_max_core
)

x3_core, pdf3_core = mean_pdf_region(
    uwnd_jun_jul_80_17_pgw_core,
    lats_core, lons_core,
    lat_min_core, lat_max_core,
    lon_min_core, lon_max_core
)

x4_core, pdf4_core = mean_pdf_region(
    uwnd_ago_oct_80_17_pgw_core,
    lats_core, lons_core,
    lat_min_core, lat_max_core,
    lon_min_core, lon_max_core
)

x5_core, pdf5_core = mean_pdf_region(
    uwnd_jun_jul_80_17_ERA5_core,
    lats_core, lons_core,
    lat_min_core, lat_max_core,
    lon_min_core, lon_max_core
)

x6_core, pdf6_core = mean_pdf_region(
    uwnd_ago_oct_80_17_ERA5_core,
    lats_core, lons_core,
    lat_min_core, lat_max_core,
    lon_min_core, lon_max_core
)


# ============================
# Calcular PDFs: Exit
# ============================
x1_exit, pdf1_exit = mean_pdf_region(
    uwnd_jun_jul_80_17_eva_exit,
    lats_exit, lons_exit,
    lat_min_exit, lat_max_exit,
    lon_min_exit, lon_max_exit
)

x2_exit, pdf2_exit = mean_pdf_region(
    uwnd_ago_oct_80_17_eva_exit,
    lats_exit, lons_exit,
    lat_min_exit, lat_max_exit,
    lon_min_exit, lon_max_exit
)

x3_exit, pdf3_exit = mean_pdf_region(
    uwnd_jun_jul_80_17_pgw_exit,
    lats_exit, lons_exit,
    lat_min_exit, lat_max_exit,
    lon_min_exit, lon_max_exit
)

x4_exit, pdf4_exit = mean_pdf_region(
    uwnd_ago_oct_80_17_pgw_exit,
    lats_exit, lons_exit,
    lat_min_exit, lat_max_exit,
    lon_min_exit, lon_max_exit
)

x5_exit, pdf5_exit = mean_pdf_region(
    uwnd_jun_jul_80_17_ERA5_exit,
    lats_exit, lons_exit,
    lat_min_exit, lat_max_exit,
    lon_min_exit, lon_max_exit
)

x6_exit, pdf6_exit = mean_pdf_region(
    uwnd_ago_oct_80_17_ERA5_exit,
    lats_exit, lons_exit,
    lat_min_exit, lat_max_exit,
    lon_min_exit, lon_max_exit
)


# ============================
# Graficar: Core + Exit
# ============================

fig, ax = plt.subplots(
    1,
    2,
    figsize=(13, 5.5),
    sharex=True,
    sharey=True
)

# ============================================================
# (a) Jun-Jul: Jet Core + Jet Exit
# ============================================================

# ----------------------------
# Jet Core - Jun-Jul
# ----------------------------
ax[0].plot(
    x1_core, pdf1_core,
    color='navy',
    lw=2,
    linestyle='-',
    label='Evaluation - Core'
)

ax[0].plot(
    x3_core, pdf3_core,
    color='firebrick',
    lw=2,
    linestyle='-',
    label='PGW - Core'
)

ax[0].plot(
    x5_core, pdf5_core,
    color='darkorange',
    lw=2,
    linestyle='-',
    label='ERA5 - Core'
)

# ----------------------------
# Jet Exit - Jun-Jul
# ----------------------------
ax[0].plot(
    x1_exit, pdf1_exit,
    color='navy',
    lw=2,
    linestyle='--',
    label='Evaluation - Exit'
)

ax[0].plot(
    x3_exit, pdf3_exit,
    color='firebrick',
    lw=2,
    linestyle='--',
    label='PGW - Exit'
)

ax[0].plot(
    x5_exit, pdf5_exit,
    color='darkorange',
    lw=2,
    linestyle='--',
    label='ERA5 - Exit'
)

ax[0].set_title('(c) Jun-Jul')
ax[0].set_xlabel('Temperature at 925 hPa (°C) - Active years')
ax[0].set_ylabel('PDF')
ax[0].grid(ls='--', alpha=0.4)

ax[0].legend(
    loc='upper right',
    fontsize=9,
    frameon=True
)


# ============================================================
# (b) Aug-Oct: Jet Core + Jet Exit
# ============================================================

# ----------------------------
# Jet Core - Aug-Oct
# ----------------------------
ax[1].plot(
    x2_core, pdf2_core,
    color='navy',
    lw=2,
    linestyle='-',
    label='Evaluation - Core'
)

ax[1].plot(
    x4_core, pdf4_core,
    color='firebrick',
    lw=2,
    linestyle='-',
    label='PGW - Core'
)

ax[1].plot(
    x6_core, pdf6_core,
    color='darkorange',
    lw=2,
    linestyle='-',
    label='ERA5 - Core'
)

# ----------------------------
# Jet Exit - Aug-Oct
# ----------------------------
ax[1].plot(
    x2_exit, pdf2_exit,
    color='navy',
    lw=2,
    linestyle='--',
    label='Evaluation - Exit'
)

ax[1].plot(
    x4_exit, pdf4_exit,
    color='firebrick',
    lw=2,
    linestyle='--',
    label='PGW - Exit'
)

ax[1].plot(
    x6_exit, pdf6_exit,
    color='darkorange',
    lw=2,
    linestyle='--',
    label='ERA5 - Exit'
)

ax[1].set_title('(d) Aug-Oct')
ax[1].set_xlabel('Temperature at 925 hPa (°C) - Active years')
ax[1].grid(ls='--', alpha=0.4)

ax[1].legend(
    loc='upper right',
    fontsize=9,
    frameon=True
)


# ============================================================
# Layout and save
# ============================================================

plt.tight_layout()

plt.savefig(
    'figs/ta925_PDFs-eva-pgw-ERA5_core_exit_1x2.png',
    dpi=400,
    bbox_inches='tight'
)

plt.show()

exit()
