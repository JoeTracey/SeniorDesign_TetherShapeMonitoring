import numpy  as  np
from matplotlib import pyplot as plt
import math


from calculate_rotation import find_theta
from strain_to_curve import *
from render_shape import *
from parser import *


#Driver uses imported functions to determine and graph the bend rate of tether based on rotational testing

#parse bend data for rotation test
bends = []
for i in range(10):
    i= 36*i
    bends +=[get_rotation_data(i)]
bends = np.array(bends)
print(np.shape(bends))

# Find bend directions
iter = 0
thetas = []
for trial in range(10):
    for segment in range(8):
        b,c,a = bends[trial,segment,:,0]
        theta = find_theta(a,b,c)
        print(a)
        thetas+= [theta]
        iter+=1




#Check bend rates, accounting for bend direction, then graph
iter = 0
for trial in range(10):
    bend_rates = []
    for segment in range(8):
        b,c,a = bends[trial,segment,:,0]
        theta = thetas[iter] 
        Length = strainToCurve(a, math.sin(math.radians(theta))*7.5) #length in pixels
        bend_rate = 360/Length #degrees per pixel (cm)
        bend_rates +=[bend_rate*10]
    img=render_shape(bend_rates)
    print('**')
    print(thetas[trial*8:trial*8+8])
    print(bend_rates)
    img.save('Renders/driver_testRot'+str(trial)+'_.png')
    iter +=1



