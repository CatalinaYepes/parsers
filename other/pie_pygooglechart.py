# -*- coding: utf-8 -*-
"""
Demo of a basic pie chart plus a few additional features.

"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(1)
ax1 = fig.add_subplot(111, projection='3d')

xpos = [1,2,3,4,5,6,7,8,9,10]
ypos = [2,3,4,5,10,6,2,1,7,2]

dx = np.ones(10)
dy = np.ones(10)
dz = [1,2,8,4,5,2,7,3,2,10,1,0.5]
zpos = np.zeros(len(dz))

ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
plt.show(1)

#
##%% Plotting damage matrix
#fig = plt.figure(2)
#damage = fig.add_subplot(111, projection='3d')
#
#xpos = ['no_damage', 'moderate', 'extensive', 'collapse']
#ypos = ['A', 'BM/SM', 'BC/SC', 'W', 'CCP']
#
#dx = ['no_damage', 'moderate', 'extensive', 'collapse', 'no_damage', 'moderate', 'extensive', 'collapse']
#dy = ['A', 'A', 'A', 'A', 'BC/SC', 'BC/SC', 'BC/SC', 'BC/SC']
#dz = [246, 1909, 1226, 1808, 21322,13924,4558,4607]
#zpos = np.zeros(len(dz))
#
#damage.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
#plt.show(2)

# These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
             
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  