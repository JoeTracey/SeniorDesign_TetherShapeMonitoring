from matplotlib import pyplot as plt
import math 
from  PIL import Image
import numpy as np
import cv2
import io 

#Create an animated gif of a graph showing the distance from neutral axis vs rotation for 3 fiber model

turn_range = range(360)

def get_d(degree0, radius, rotation ):
    return(math.sin(math.radians(degree0+rotation))*radius)

if __name__ == '__main__':

    d0,d1,d2 = 90, 210, 330

    distance_from_neutral0 = []
    for i in turn_range:
        distance_from_neutral0 += [get_d(d0, 1, i)]

    distance_from_neutral1 = []
    for i in turn_range:
        distance_from_neutral1 += [get_d(d1, 1, i)]

    distance_from_neutral2 = []
    for i in turn_range:
        distance_from_neutral2 += [get_d(d2, 1, i)]


    arrays =[]
    for i in range(360):
        plt.xlabel('Rotation')
        plt.ylabel('Distance from Neutral Axis')

        plt.plot(turn_range, distance_from_neutral0)
        plt.plot(turn_range, distance_from_neutral1)
        plt.plot(turn_range, distance_from_neutral2)

        plt.legend(['Fiber-1','Fiber-2','Fiber-3'], loc = 'lower right', shadow = True)
        plt.axhline(y=0, color = 'black', linestyle = '-')
        plt.axvline(x=i, color = 'red', linestyle = '--')
        fig = plt.Figure()
        buffer = io.BytesIO()
        plt.savefig(buffer)
        buffer.seek(0)
        im = Image.open(buffer)
        arrays +=[np.array(im)]
        print(np.shape(im))
        plt.clf()

    # Array prep
    arrays = np.array(arrays)
    print(np.shape(arrays))
    arrays = np.moveaxis(arrays, -1, 1)
    arrays = arrays[:,:3]
    arrays = arrays//125*125
    print(np.shape(arrays))

    # # Save as a gif
    # from array2gif import write_gif
    # np.save('numpy.npy', arrays)
    # write_gif(arrays, 'tester.gif', fps = 20)