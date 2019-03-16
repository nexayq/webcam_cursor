
from __future__ import print_function, division

import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt

y_in_array = np.arange(0,4000,20)
sum_Y_array = np.arange(0,4000,20)
y_out_array = np.arange(0,4000,20)

speed = 20
for i in range(0,200):
    y_out = y_in_array[i]
    sum_Y = sum_Y_array[i]
    if(sum_Y < 1000/5*2):
        y_out = y_out/2
        # use some OK default speed
        y_out = 25*y_out/1000
    # fast cursor movements
    elif(sum_Y > 2000/5*2):
        y_out = 2*speed*y_out/1000
    # normal speed cursor movements
    else:
        # speed scale
        y_out = speed*y_out/1000

    y_out_array[i] = y_out

f = interpolate.interp2d(y_in_array, sum_Y_array, y_out_array, kind='cubic')

x = np.arange(0,200)
plt.plot(x, y_out_array)
plt.show()

z_new = f(y_in_array, sum_Y_array)
#  print(z_new)
plt.plot(x, z_new[0,:])
plt.show()
