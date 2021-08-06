#coding=utf-8
###################################################################################################################################
#####This module enables you to maskout the unneccessary data outside the interest region on a matplotlib-plotted output instance
####################in an effecient way,You can use this script for free     ########################################################
#####################################################################################################################################
#####USAGE: INPUT  include           'originfig': the matplotlib instance##
#                                    'ax': the Axes instance
#                                    'shapefile': the shape file used for generating a basemap A
#                                    'region': the name of a region of on the basemap A,outside the region the data is to be maskout
#           OUTPUT    is             'clip': the the masked-out or clipped matplotlib instance.
import shapefile
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
import cartopy.io.shapereader as shpreader
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import geopandas

def shp2clip(originfig,ax,shpfile,region):
    
    sf = shapefile.Reader(shpfile, encoding='ISO8859-1') # encoding utf-8 / ISO8859-1
    
    # obtain shapes and its records
    # the shapes are the actual coordinate points 
    # the record contains all attributes related to each shape
    shape_records = sf.shapeRecords()

    # search for the ones with desired records
    desired_shapes = []
    
    #adm1_shapes=list(shpreader.Reader(shpfile).geometries())
    #ax.add_geometries(adm1_shapes[:], ccrs.PlateCarree(), edgecolor='k', facecolor='none', alpha=0.5)
    
    # read the shapefile using geopandas
    df = geopandas.read_file(shpfile)

    # read the borders
    for i in range(0,13):
        poly = df.loc[df['PROVINCE'] == 'Benguet']['geometry'].values[i]
        ax.add_geometries([poly], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='k', lw=0.5)
    #ax = plt.axes(projection=ccrs.PlateCarree())
    #for pol in [poly]:
    #    ax.add_geometries([pol], crs=ccrs.PlateCarree(), facecolor='none', edgecolor='k')
    #countries = sf.records()
    #for country in countries:
    #    if country.attributes['PROVINCE'] == "Benguet":
    #        ax.add_geometries(country.geometry, ccrs.PlateCarree(), edgecolor='k', facecolor='none', alpha=0.5)
    
    for shape_rec in shape_records:
        if shape_rec.record[4] == region:  ####Here you need to find a unique identifier that matches the region, and one item in record[] must correspond.
            desired_shapes.append(shape_rec.shape)
            vertices = []
            codes = []
            
            for x in desired_shapes:
                pts = x.points
                prt = list(x.parts) + [len(pts)]
                for i in range(len(prt) - 1):
                    for j in range(prt[i], prt[i+1]):
                        vertices.append((pts[j][0], pts[j][1]))
                    codes += [Path.MOVETO]
                    codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
                    codes += [Path.CLOSEPOLY]
                clip = Path(vertices, codes)
                clip = PathPatch(clip, transform=ax.transData, facecolor='white')
    for contour in originfig.collections:
        contour.set_clip_path(clip)
    return clip