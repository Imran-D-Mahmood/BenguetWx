# Reference: https://www.programmersought.com/article/70684797782/
import numpy as np
import pandas as pd
from scipy.interpolate import Rbf  # Radial basis function: insert site information on grid points for drawing contour
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.patheffects as PathEffects
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
import cartopy.io.shapereader as shpreader
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from shapely.geometry.polygon import LinearRing
import maskout  # Show only a certain area


plt.rcParams["figure.facecolor"] = 'whitesmoke'

fig = plt.figure(figsize=(6.5,8)) # WxH 650x800
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

plt.title('Benguet Observed + Interpolated Rainfall Accumulation (mm)\n08-05-21 8AM - 08-06-21 8AM PhT', fontsize=10)

# data preparation
#excfile = 'Benguet-Stations.xlsx'
#f = pd.read_excel(excfile, 'Sheet1').dropna()
f = pd.read_csv('Daily-Aug05.csv').dropna()
f.columns = ['NAME','LATITUDE','LONGITUDE','RAIN_ACC_MM']
lon = f['LONGITUDE']
lat = f['LATITUDE']
rain = f['RAIN_ACC_MM']

plt.scatter(lon, lat, s=8, color='lightgray', edgecolor='dimgray', zorder=4, transform=ccrs.PlateCarree())
for i, data in enumerate(rain):
    txt = ax.annotate(' ' + str(data), (lon[i], lat[i]), fontsize=8, color='black', fontweight='bold')
    txt.set_path_effects([PathEffects.withStroke(linewidth=0.8, foreground='w')])

plt.text(120.38, 16.93, '*EXPERIMENTAL; NOT AN OFFICIAL PRODUCT*',  fontsize=9, color='red', transform=ccrs.PlateCarree());

# Drawing preparation
extent = [120.37, 120.95, 16.18, 16.95]
lonmin, lonmax, latmin, latmax = extent
olon = np.linspace (lonmin,lonmax,120) # Long and latitude coordinates, 0.05° resolution 118° to 126° 0.05 resolution is 160 grid points
olat = np.linspace (latmin,latmax,60) # Latitude coordinates, 0.05° resolution
olon,olat = np.meshgrid(olon,olat) # Generate coordinate grid meshgrid meshing
func = Rbf(lon,lat,rain,function='linear') # Interpolation function - Call the cubic interpolation method in the Rbf interpolation function linear
rain_data_new = func(olon,olat) # Interpolation
rain_data_new[rain_data_new <0 ] = 0

# Custom precipitation cmap
clevs = [4,5,10,15,20,30,40,50,60,80,100,120,150,200,250,300,400,500]
cdict = ['#98ffff','#00ceff','#009aff','#006af7','#2e9c00','#2bff00','#fefe08','#ffcb00','#ff9c00','#fe0005','#c90200','#9d0000','#9a009d','#cf00d7','#ff00f7','#fdcafe', 'pink', 'lightpink']
my_cmap = colors.ListedColormap(cdict)
norm = mpl.colors.BoundaryNorm(clevs,my_cmap.N) # Generate color mapping index based on discrete interval

# Draw contours, color contours
cf = ax.contourf(olon, olat, rain_data_new, clevs, transform=ccrs.PlateCarree(), cmap=my_cmap, norm=norm, extend='both')
clb = plt.colorbar(cf, ticks=clevs, fraction=0.04)
clb.ax.set_xlabel('mm')

# Municipality labels
munfs = 7
muncol = 'black'
munalpha = 0.8

plt.text(120.5760, 16.4023, '$\it{Baguio}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.6890, 16.3452, '$\it{Itogon}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.5740, 16.3005, '$\it{Tuba}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.5855, 16.4774, '$\it{La Trinidad}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.5164, 16.4855, '$\it{Sablan}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.6315, 16.5121, '$\it{Tublay}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.7810, 16.4564, '$\it{Bokod}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.5970, 16.6124, '$\it{Kapangan}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.6890, 16.6816, '$\it{Kibungan}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.6890, 16.5974, '$\it{Atok}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.8269, 16.6070, '$\it{Kabayan}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.8368, 16.7492, '$\it{Buguias}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.6890, 16.8080, '$\it{Bakun}$', fontsize=munfs, color=muncol, alpha=munalpha)
plt.text(120.7810, 16.8770, '$\it{Mankayan}$', fontsize=munfs, color=muncol, alpha=munalpha)

# # # #Cut
clip = maskout.shp2clip(cf, ax, 'MuniCities/MuniCities.shp', 'Benguet')

plt.figtext(0.5, 0.02, 'Station data from PAGASA and DOST-ASTI | Plotted by Imran Mahmood', fontsize=8, color='black', ha='center')

ax2 = inset_axes(ax, width="35%", height="35%", loc="upper left", axes_class=cartopy.mpl.geoaxes.GeoAxes, axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))
ax2.add_feature(cartopy.feature.COASTLINE, lw=0.5)
ax2.add_feature(cartopy.feature.LAND, facecolor='white')
ax2.set_extent([116.0, 127.0, 5.0, 22.0])

nvert = 100
lons = np.r_[np.linspace(lonmin, lonmin, nvert),
             np.linspace(lonmin, lonmax, nvert),
             np.linspace(lonmax, lonmax, nvert)].tolist()
lats = np.r_[np.linspace(latmin, latmax, nvert),
             np.linspace(latmax, latmax, nvert),
             np.linspace(latmax, latmin, nvert)].tolist()

ring = LinearRing(list(zip(lons, lats)))
ax2.add_geometries([ring], ccrs.PlateCarree(), facecolor='none', edgecolor='red', linewidth=0.75)
ax2.set_frame_on(False)  

plt.tight_layout()
#plt.savefig('BenguetRain.png')

plt.show()
