#! /usr/bin/python3

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


# GO THROUGH THIS AND ALSO OBSERVE THE ACROBATICS I HAVE TO DO IN ORDER TO MAKE
# THE CODE WORK. THINK ABOUT HOW TO BETTER FORMAT SPREADSHEETS TO BE EASILY
# MACHINE READABLE


##############################
# EDIT THIS PART OF THE CODE #
##############################

spreadsheet_filename = 'UMV radiocarbon compiled vAW2021.xlsx'
output_filename = 'UMV14C.gpkg'
header = 4 # number of blank header lines; often 0
n_col = '°N Lat'
e_col = '°W Lon'
n_neg = False # degrees south, flip sign
e_neg = True # degrees west, flip sign


###############################
# SOME MORE TO EDIT DOWN HERE #
###############################

df = pd.read_excel(spreadsheet_filename, header=4)

_n = df[n_col]
_e = df[e_col]
# Elevations do not seem to be known -- could add more later

# Information associated with this specific data set
# Age information to keep along
_cal_yr_bp = df['CAL YR BP']
_cal_yr_bp_sd = df['1-Sigma'] # But this isn't great representation of non-normal distribution
# Sample depths
_depth = df['Sample Depth below terrace tread [m]']


########################################################
# CREATE NEW (CLEANER) DATAFRAME FOR DATA TABLE OUTPUT #
########################################################

df_points = pd.DataFrame({'age [cal yr BP]': _cal_yr_bp,
                          'sd [cal yr]': _cal_yr_bp_sd,
                          'depth [m]': _depth})

#####################################################################
# GENERATE A SET OF GIS POINTS CORRESPONDING TO THESE ENTRIES TABLE #
#####################################################################

# These are 2D points; 3D points would require an additional "z" specification
# One can also create lines, etc., via Shapely
# cf. https://github.com/MNiMORPH/LSDTT-network-tool/blob/master/lsdtt-network-tool.py

_points = []
for i in _n.index:
    _points.append( Point(_e[i], _n[i]) )

################################
# Write the GeoPackage to file #
################################

# CRS is for WGS84 lat/lon

gdf_points = gpd.GeoDataFrame( df_points, geometry=_points, crs="EPSG:4326")
gdf_points.to_file(output_filename, driver="GPKG")
print("Points written to", output_filename)

