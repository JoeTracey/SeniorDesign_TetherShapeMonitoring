import numpy as np
from skimage import draw
from PIL import Image 
import cv2
import math

# Generates a diagram of the current tether/fiber layout relative to the neutral axis

# Add a fiber to the diagram
def add_fiber(canvas, C, r, theta, circle_size = 20, thickness = 5, color = (0,0,0)):
    start = (C, C)
    offset = (math.sin(math.radians(theta))*r, math.cos(math.radians(theta))*r)
    x, y = int(start[0]+offset[0]), int(start[1]+offset[1])
    canvas = cv2.circle(canvas, (x,y), circle_size, color, thickness)
    return(canvas)

# Add the tether outline to the diagram
def add_tether(canvas, C, r , color = (0,0,0)):
    canvas = cv2.circle(canvas, (C,C), r, color, 5)
    return(canvas)

# Add the center point to the diagram
def add_center(canvas, C):
    canvas = cv2.circle(canvas, (C,C), 1, (0,0,0,), 5)
    return(canvas)

# Add neutral axis line to the diagram
def add_neutral_axis(canvas, C, r):
    canvas = cv2.line(canvas, (C,C-r), (C,C+r), (0,0,0), 1)
    return(canvas)



if __name__ == '__main__':
    
    #Run through and generate a gif of a full rotation cycle (aligned with graph_rotation.py)

    #set parameters
    size = 640
    C = size // 2
    r_tether = 300
    r_fiber = 200

    #set fiber offsets (degrees)
    d0,d1,d2 = 90, 210, 330

    #Generate tether
    canvas = np.ones((size, size,3))
    print(np.max(canvas))
    canvas = add_tether(canvas, C, r_tether)
    print(np.max(canvas))
    canvas = add_center(canvas, C)
    canvas = add_neutral_axis(canvas, C, r_tether)

    #Add Fibers
    canvas = add_fiber(canvas, C, r_fiber, d0)
    canvas = add_fiber(canvas, C, r_fiber, d1)
    canvas = add_fiber(canvas, C, r_fiber, d2)

    #adjust axis via rotation
    canvas = np.rot90(canvas)

    #Save diagram
    canvas*=255
    canvas = canvas.astype('uint8')
    im = Image.fromarray(canvas)
    im.save('diagram.tif')



    #Generate gif rotating 360
    arrays = []
    for i in range(360):
        #Generate tether
        canvas = np.ones((size, size,3)).astype('uint8')
        canvas = add_tether(canvas, C, r_tether)
        canvas = add_center(canvas, C)
        canvas = add_neutral_axis(canvas, C, r_tether)
        canvas = add_fiber(canvas, C, r_fiber, d0, color = (0,0,1))
        canvas = add_fiber(canvas, C, r_fiber, d1, color = (1,3,0) )
        canvas = add_fiber(canvas, C, r_fiber, d2, color = (0,1,0) )
        d0+=1
        d1+=1
        d2+=1

        canvas = np.rot90(canvas)
        arrays +=[np.array(canvas)]
        print(np.shape(im))

    # Array prep
    arrays = np.array(arrays)
    arrays = np.moveaxis(arrays, -1, 1)
    arrays[arrays==3] = 122
    arrays[arrays==1] = 255
    # arrays = arrays[:,:3]
    # arrays = arrays//10*110

    # # Save as a gif
    # from array2gif import write_gif
    # # np.save('numpy.npy', arrays)
    # print(np.min(arrays))
    # print(np.max(arrays))
    # # print(3/0)
    # write_gif(arrays, 'tester_diagram.gif', fps = 20)