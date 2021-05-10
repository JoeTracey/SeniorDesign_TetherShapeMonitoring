import numpy  as  np
from matplotlib import pyplot as plt
import math


from calculate_rotation import find_theta
from strain_to_curve import *
from render_shape import *
from parser import *


#Input your data as Nodes

bends = []
for i in [2,4,6,8,10,20,50,100,200]: #List of file names as input
    print(i)
    bends+=[get_bend_data(i)]
bends = np.array(bends)
print(np.shape(bends))

# Find bend directions
iter = 0
thetas = []
for trial in range(9):
    for segment in range(8):
        b,c,a = bends[trial,segment,:,0]
        theta = find_theta(a,b,c)
        print(a)
        thetas+= [theta]
        iter+=1




#Check bend rates
iter = 0
for trial in range(9):
    bend_rates = []
    for segment in range(8):
        b,c,a = bends[trial,segment,:,0]
        theta = thetas[iter]
        Length = strainToCurve(a, math.sin(math.radians(90))*7.5) #length in pixels
        bend_rate = 360/Length #degrees per pixel (cm)
        bend_rates +=[bend_rate]
    img=render_shape(bend_rates)
    print('**')
    print(theta)
    print((a, math.sin(math.radians(90))*7.5))
    print(thetas[trial*8:trial*8+8])
    print(bend_rates)
    img.save('Renders/driver_test'+str(trial)+'_.png')
    iter +=1



