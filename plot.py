import matplotlib.pyplot as plt
import pygmt
import numpy as np
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime as dt
import requests
import time
import seaborn as sns

data=pd.read_csv('LL_Data_1979_2021_values_final.csv')
loc=pd.read_table('SiteLocations.dat', header=None)
LOC = loc.to_numpy()
# print(loc.columns)
elevations = data.to_numpy()


#Figure setup from code
#Edited later on, so this version is just a backup in case things go wrong
# fig = pygmt.Figure()
# pygmt.config(MAP_FRAME_TYPE='plain', FORMAT_GEO_MAP='ddd.xx')
# fig.coast(region=[173, 179, -42, -36],
# shorelines=True,
# land='lightgreen',
# water='lightblue',
# projection='M10c',
# frame=['WSne', 'xa2f1', 'ya2f1'])



#Define time slicing function to get depth data
#slice gives a list of 2 elements, the first hopefully being the 1d vector of elevation values for all stations and the second one being the date of slice taken
# def slice(I):
#     date = elevations[I][0]
#     heights = np.array(elevations[I][1:23])
#     newheights=np.ones(22)
#     for i in range(len(heights)):
#         if pd.isna(heights[i]):
#             newheights[i]*= 340  #Value to replace nan values with
#         else:
#             newheights[i]*= heights[i]
#     return [newheights, date]

# def name_from_dat(index):
#     return LOC[index][0].split(',')[1]


def info_from_dat(station):
    information = []
    for index in range(len(LOC)):
        name = LOC[index][0].split(',')[1]
        if station==name:
            information.append(LOC[index][0].split(',')[2:4])

    return information[0]


#Problem area

# fig.contour(x=np.array(pd.DataFrame([176.01, 176.01, 176.01], columns=['longitude'])),y=np.array(pd.DataFrame([-38.038, -38.038, -38.038], columns=['latitude'])),z=np.array(pd.DataFrame([0.00, 0.03, 0.10], columns=['depth'])), levels=1, annotation=10, pen='2p')

# fig.contour(x=x1,y=y1,z=z1, levels=1, annotation=10, pen='2p')
#trying to make em columns
# fig.contour(x=pd.DataFrame([[176.01],[176.01],[176.01]], columns=['longitude']),y=pd.DataFrame([[-38.038],[-38.038],[-38.038]], columns=['latitude']),z=pd.DataFrame([[0.00],[0.10],[2.00]], columns=['depth']), levels=1, annotation=10, pen='2p')








#
#
# ################
# Previous example that worked
# fig.contour(x=np.array([177,176,166]),y=np.array([-37,-38,-40]),z=np.array([0,2,20]), levels=1, annotation=10, pen='2p')
#
# #This section DOES work and shows contours still
# fig.contour(x=np.linspace(174,178,22),y=np.linspace(-42,-36,22),z=np.linspace(100,200,22), levels=1, annotation=10, pen='2p')
# fig.show()
#
#
# fig = pygmt.Figure()
# pygmt.config(MAP_FRAME_TYPE='plain', FORMAT_GEO_MAP='ddd.xx')
# fig.coast(region=[173, 179, -42, -36],
# shorelines=True,
# land='lightgreen',
# water='lightblue',
# projection='M10c',
# frame=['WSne', 'xa2f1', 'ya2f1'])
#
#
# fig.contour(x=np.linspace(174,178,22),y=np.linspace(-42,-36,22),z=slice(5)[0], levels=1, annotation=10, pen='2p')
# fig.show()
#
# ###########
#But what we need to do is make sure the station locations are in line with the slice station arrangements
#As is evident. they are  not the same

#Here is the slice/elevation/data's station arrangement
data_arrangement = data.columns.to_numpy()[1:-4]

#We are to arrange the dat file import - LOC's arrangement to this
longitude = [float(info_from_dat(coord)[0]) for coord in data_arrangement]
latitude = [float(info_from_dat(coord)[1]) for coord in data_arrangement]


###

#Initial version without removing the "bloat" from elevation values
# fig = pygmt.Figure()
# pygmt.config(MAP_FRAME_TYPE='plain', FORMAT_GEO_MAP='ddd.xx')
# fig.coast(region=[175.5, 176.3, -39, -38.6],
# shorelines=True,
# land='lightgreen',
# water='royalblue',
# projection='M10c',
# frame=['WSne', 'xa.2f1', 'ya.2f1'])
#
#
# fig.contour(x=longitude,y=latitude,z=slice(100)[0], levels=1, annotation=.1, pen='.3p')
# fig.show()





###Note
#Average value to replace nan values with was found by finding a full average of all values recorded

# sum=0
# count=0
# for j in elevations:
#     for i in j[1:23]:
#         if pd.isna(i):
#             pass
#         else:
#             sum+=float(i)
#             count+=1
# print(sum/count)



#[Ans]358.01643499822933

#However, if you use this value, the negative values will not be recorded




#What if we wanted to consider relative elevation versus these arbitrary elevation values?
#Let us have slice command changed to reflect that simply


def slice2(I):
    date = elevations[I][0]
    heights = np.array(elevations[I][1:23])
    newheights=np.ones(22)
    for i in range(len(heights)):
        if pd.isna(heights[i]):
            newheights[i]*= 0  #Value to replace nan values with
        else:
            newheights[i]*= heights[i]-356
    return [newheights, date]



fig = pygmt.Figure()
pygmt.config(MAP_FRAME_TYPE='plain', FORMAT_GEO_MAP='ddd.xx')
fig.coast(region=[175.5, 176.3, -39, -38.6],
shorelines=True,
land='lightgreen',
water='royalblue',
projection='M10c',
frame=['WSne', 'xa.2f1', 'ya.2f1'])

#Set precision
st = '0.0'
thing = np.linspace(0,2,21)
for i in thing[1:]:
    st += ',' + f'{i:.1f}'


st2 = '0.0'
thing = np.linspace(0,2,41)
for i in thing[1:]:
    st2 += ',' + f'{i:.1f}'

# fig.contour(x=longitude,y=latitude,z=slice2(5)[0], levels=.05, annotation=.1, pen='.08p')
fig.contour(x=longitude,y=latitude,z=slice2(5)[0], levels=st, annotation=st2, pen='.08p')
fig.show()


