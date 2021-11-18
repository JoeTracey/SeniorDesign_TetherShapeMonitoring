import numpy as np
import math 
from PIL import Image

Vector0 = np.array([1,0])

import matplotlib.pyplot as plt 
import numpy as np    
import time

#provide fixed values from simulation for shape rendering

L = 32# 32m 3200cm
Thickness = 0.15# 15cm

#convert to pixels
L*=100
Thickness*=100


BR = 0.0036  # Rate = degree per unit length
Vector0 = 0 # starting vector = 0 degrees

#uses a set of 8 linear bend rates to render the tether shape
def render_shape(BRs, L=L, Thickness=Thickness, Vector0 = Vector0):
    #start rendering from the bottom center
    center = (L//2,L)
    #set first bend rate to use for first tether segment
    BR = BRs[0]
    #create a blank template to render on
    template = np.zeros((L*2,L*2)).astype('uint8')
    locations = [center]
    print(np.shape(template))
    i=0
    step = 1
    volume = L*Thickness
    Continue =0

    # while Vector0+i*BR < 270 and np.sum(template) <  volume/step: # set max rotation to render and max length (/100th scale)
    timea = time.time()
    while Continue == 0 : #stop rendering and move along if Continue
        #get last location to draw pixels on template
        x,y = locations[-1]
        template[int(x),int(y)]=1
        #add pixels for full tether thickness
        for t in range(int(Thickness)):
            template[int(x),int(y+t)]=1
            template[int(x+t),int(y)]=1
        #calculate next location based on directional vector
        locations+=[(x+step*math.cos(math.radians(Vector0+1*BR)),y+step*math.sin(math.radians(Vector0+1*BR)))]
        i+= step
        if i > L: #trigger Continue, to move past rendering, if total final length reached
            if np.sum(template) >=  volume or Vector0+i*BR < 270 :
                Continue =1
        elif i > 7*L//8: #use 7th bend rate for final segment
            BR = BRs[7]
        elif i > 6*L//8:#use 6th bend rate for 1st segment
            BR = BRs[6]
        elif i > 5*L//8:#use 5th bend rate for 1st segment
            BR = BRs[5]
        elif i > 4*L//8:#use 4th bend rate for 1st segment
            BR = BRs[4]
        elif i > 3*L//8:#use 3rd bend rate for 1st segment
            BR = BRs[3]
        elif i > 2*L//8:#use 2nd bend rate for 1st segment
            BR = BRs[2]
        elif i > L//8: #use 2nd bend rate for 2nd segment
            BR = BRs[1]
        Vector0+=1*BR #set vector for next pixel rendered based on current bend rate

    #convert to an array and return image of rendering
    template = np.array(template)
    template[int(L//2 + x)//2, int(L + y)//2] = 1
    img = Image.fromarray(template*255)
    return(img)

