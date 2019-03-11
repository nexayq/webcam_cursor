#!/usr/bin/env python2

from __future__ import print_function, division
import numpy as np
from scipy import signal

# input
x = np.array([0, 20, 0])
x = np.array([0, 1, -1, 0])


v = [None]*5
# inputs
v[0] = np.array([0])
v[1] = np.array([20, 0])
v[2] = np.array([-20, 20, 0])
v[3] = np.array([0, -20, 20, 0])
v[4] = np.array([0, 0, -20, 20])

# coefficients
#  c = np.array([0.5, 0.5])
c = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
#  out = np.zeros(5)

# design filter
numtaps = 5
f = 0.2
c2 = signal.firwin(numtaps, f)
print(c2)

# output
#  out[0] = x[0]*c[0] + 0
#  out[1] = x[1]*c[0] + x[0]*c[1]
#  out[2] = x[2]*c[0] + x[1]*c[1]

out = np.convolve(x, c)

#  for i in range(0, len(c) + 1):
    #  out[i] = x[j]*c[i]

print(len(out))
print(out)

out2 = np.convolve(x, c2)
print(out2)

# convolve multiple inputs
print
print("V inputs")
for i in range(0,5):
    print(np.convolve(v[i], c2))
#  print(out[0], out[1], out[2])
#  for i in len(x):
    #  out[i] = x[i]*c[i]

#  y[n] = x[n-2]*c[2] + x[n-1]*c[1] + x[n]

print
x = np.array([0, 20, 0, 0])
x2 = np.array([-20, 0, 20, 0])
x3 = np.array([0, -20, 0, 20])
c = np.array([0.25, 0.25, 0.25, 0.25])
y  = x[3]*c[3]  + x[2]*c[2]   + x[1]*c[1]  + x[0]*c[0]
y2 = x2[3]*c[3] + x2[2]*c[2]  + x2[1]*c[1] + x2[1]*c[0]
y3 = x3[3]*c[3] + x3[2]*c[2]  + x3[1]*c[1] + x3[1]*c[0]
#  y2 = x2[2]*c[2] + x2[1]*c[1] + x2[1]*c[0]
print(y)
print(y2)
print(y3)
print(np.convolve(x, c))
print(np.convolve(x2, c))
print(np.convolve(x3, c))

a = np.array([1,2,3])
b = np.append([4], a)
print(b)

# design filter
numtaps = 5
f = 0.2
c2 = signal.firwin(numtaps, f)
print(c2)
