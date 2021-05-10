import numpy as np
import math 
from PIL import Image

Vector0 = np.array([1,0])

import matplotlib.pyplot as plt 
import numpy as np    
import time

L = 32# 32m 3200cm
Thickness = 0.15# 15cm

L*=100
Thickness*=100


BR = 0.0036  # Rate = degree per unit length
# BR = 0
Vector0 = 0 # starting vector = 0 degrees

def render_shape(BRs, L=L, Thickness=Thickness, Vector0 = Vector0):
    center = (L//2,L)
    BR = BRs[0]
    template = np.zeros((L*2,L*2)).astype('uint8')

    locations = [center]
    print(np.shape(template))
    i=0
    step = 1
    volume = L*Thickness
    Continue =0

    # while Vector0+i*BR < 270 and np.sum(template) <  volume/step: # set max rotation to render and max length (/100th scale)
    timea = time.time()
    while Continue == 0 : # set max rotation to render and max length (/100th scale)
        time0 = time.time()
        x,y = locations[-1]
        locations+=[(x+step*math.cos(math.radians(Vector0+1*BR)),y+step*math.sin(math.radians(Vector0+1*BR)))]
        template[int(x),int(y)]=1
        for t in range(int(Thickness)):
            template[int(x),int(y+t)]=1
            template[int(x+t),int(y)]=1
        time5 = time.time()
        i+= step
        if i > L:
            # print('hit')
            if np.sum(template) >=  volume or Vector0+i*BR < 270 :
                Continue =1
        
        elif i > 7*L//8:
            BR = BRs[7]
        elif i > 6*L//8:
            BR = BRs[6]
        elif i > 5*L//8:
            BR = BRs[5]
        elif i > 4*L//8:
            BR = BRs[4]
        elif i > 3*L//8:
            BR = BRs[3]
        elif i > 2*L//8:
            BR = BRs[2]
        elif i > L//8:
            BR = BRs[1]
        time6 = time.time()
        Vector0+=1*BR

    # template[0,0] = 2
    # print('calculated')
    template = np.array(template)
    template[int(L//2 + x)//2, int(L + y)//2] = 1
    img = Image.fromarray(template*255)
    return(img)

# img.save('early_shape_render.png')
