# Reference: https://www.programmersought.com/article/70684797782/
import numpy as np
import pandas as pd
from scipy.interpolate import Rbf  # Radial basis function: insert site information on grid points for drawing contour
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
import cartopy.io.shapereader as shpreader
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import maskout  # Show only a certain area


plt.rcParams["figure.facecolor"] = 'whitesmoke'

fig = plt.figure(figsize=(6.5,8)) # WxH 650x800
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

plt.title('Benguet Observed Rainfall Accumulation (mm)\n05-22-21 8AM - 05-23-21 8AM (PhT)')
plt.figtext(0.5, 0.01, 'Station data from PAGASA and DOST-ASTI | Plotted by Imran Mahmood', fontsize=8, color='black', ha='center')

# data preparation
excfile = 'Benguet-Stations.xlsx'
f = pd.read_excel(excfile, 'Sheet1').dropna()
f.columns = ['NAME','LATITUDE','LONGITUDE','RAIN_ACC_MM']
lon = f['LONGITUDE']
lat = f['LATITUDE']
rain = f['RAIN_ACC_MM']

plt.scatter(lon, lat, s=8, color='lightgray', edgecolor='dimgray', zorder=4, transform=ccrs.PlateCarree())
#for i, data in enumerate(rain):
#    ax.annotate(' ' + str(data), (lon[i], lat[i]), fontsize=9, color='black', fontweight='bold') # repr - convert float to str w/o losing precision

# Drawing preparation
olon = np.linspace (120.37,120.95,120) # Long and latitude coordinates, 0.05° resolution 118° to 126° 0.05 resolution is 160 grid points
olat = np.linspace (16.18,16.95,60) # Latitude coordinates, 0.05° resolution
olon,olat = np.meshgrid(olon,olat) # Generate coordinate grid meshgrid meshing
func = Rbf(lon,lat,rain,function='linear') # Interpolation function - Call the cubic interpolation method in the Rbf interpolation function linear
rain_data_new = func(olon,olat) # Interpolation
rain_data_new[rain_data_new <0 ] = 0

# Custom precipitation cmap
clevs = [0,1,2,5,10,15,20,30,40,50,70,90,100,130,150,200,300,500]
cdict = ['#ffffff','#98ffff','#00ceff','#009aff','#006af7','#2e9c00','#2bff00','#fefe08','#ffcb00','#ff9c00','#fe0005','#c90200','#9d0000','#9a009d','#cf00d7','#ff00f7','#fdcafe']
my_cmap = colors.ListedColormap(cdict)
norm = mpl.colors.BoundaryNorm(clevs,my_cmap.N) # Generate color mapping index based on discrete interval

# Draw contours, color contours
cf = ax.contourf(olon, olat, rain_data_new, clevs, transform=ccrs.PlateCarree(), cmap=my_cmap, norm=norm) #alpha=0.3

# ct = ax.contour(olon,olat,rain_data_new,clevs) # draw contour
# clabel = ax.clabel(ct,fmt = '%i')
position = fig.add_axes([0.82,0.2,0.05,0.2]) # Position [left, bottom, width. high】
plt.colorbar(cf, cax=position)

#ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
#ax.yaxis.set_major_formatter(LatitudeFormatter())

# # # #Cut
clip = maskout.shp2clip(cf, ax, 'bg2/bg2.shp', 'Philippines')

#shpname = r'MuniCities/MuniCities.shp'  # MuniCities/MuniCities.shp
#adm1_shapes=list(shpreader.Reader(shpname).geometries())
#ax.add_geometries(adm1_shapes[:], ccrs.PlateCarree(), edgecolor='k', facecolor='none', alpha=0.5)

#plt.savefig('BenguetRain.png')
plt.show()
