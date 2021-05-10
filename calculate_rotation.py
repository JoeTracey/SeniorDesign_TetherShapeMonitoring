import numpy as np
import math 
from matplotlib import pyplot as plt
from PIL import Image
import io
from tqdm import tqdm
from array2gif import write_gif



# Find the rotation angle based on the three equidistant strain values (s1,s2, and s3) 
def find_theta(s0,s1,s2, sofar = 0):
    def guess_theta(ratio, theta, iter = 0):
        difference = ratio - math.sin(math.radians(theta))/math.sin(math.radians(theta+120))
        if difference > 40:
            difference = np.random.randint(0,40)
            iter+=1
        if difference < -40:
            difference = np.random.randint(0,40)*-1
            iter+=1
        return(difference/10, iter)
    result = 100
    theta = 120
    ratio = s0/s1
    iter =0
    while result > 0.00001 or result < -0.00001:
        theta+= result
        result, iter =  guess_theta(ratio, theta, iter)
        if theta > 900 or iter>10 or ratio > 10 or ratio <-10:
            return(find_theta(s1, s2, s0 ,sofar=sofar-120))
    print(theta)
    print(sofar)
    if theta > 180 and s0>0 and sofar ==0:
        theta-=180
    if theta < 180 and s0<0 and sofar ==0:
        theta+=180
    theta=theta+sofar
    if theta<0:
        theta+=360
    return(theta)


if __name__ == '__main__':

    #Run script to test find_theta

    #initial degrees
    d0,d1,d2 = 90, 210, 330
    offset = 1

    #strains 
    s0 = math.sin(math.radians(d0)) * offset
    s1 = math.sin(math.radians(d1)) * offset
    s2 = math.sin(math.radians(d2)) * offset
    print("strains:"+str((s0,s1,s2)))

    theta  = find_theta(s0,s1,s2)

    print('Found theta')
    print(theta)
    print(d0)

    rotation=50
    print('Rotating:'+str(rotation))
    d0+= rotation
    d1+= rotation
    d2+= rotation

    #strains 
    s0 = math.sin(math.radians(d0)) * offset
    s1 = math.sin(math.radians(d1)) * offset
    s2 = math.sin(math.radians(d2)) * offset
    print("strains:"+str((s0,s1,s2)))

    theta  = find_theta(s0,s1,s2)

    print('Found theta')
    print(theta)
    print(d0)


    # graph prediction
    # d0,d1,d2 = 90, 210, 330
    d0,d1,d2 = 0.001,120.001,240.001

    thetas = []
    #Run script to test find_theta on fiber layout for all points in rotation, then graph output
    truths = []
    print('predicting with graph')
    for i in range(720):
        i=i
        s0 = math.sin(math.radians(d0+i)) * offset
        s1 = math.sin(math.radians(d1+i)) * offset
        s2 = math.sin(math.radians(d2+i)) * offset
        theta = find_theta(s0, s1, s2)
        print((s0,s1,theta, d0+i))
        thetas+=[theta]
        truths+=[d0+i]

    truths = np.array(truths)
    thetas = np.array(thetas)
    plt.plot(truths, thetas)
    plt.xlabel('Degrees of Rotation')
    plt.ylabel('Predicted Degrees of Rotation')
    plt.savefig("PredictedDirection")
    plt.show()

    #Save as a gif - calculate with line
    arrays = []
    for i in tqdm(range(720)): #720
        plt.plot(truths, thetas)
        plt.axvline(x=i, color = 'red', linestyle = '--')
        plt.xlabel('Degrees of Rotation')
        plt.ylabel('Predicted Degrees of Rotation')
        plt.savefig("PredictedDirection")
        buffer = io.BytesIO()
        plt.savefig(buffer)
        buffer.seek(0)
        im = Image.open(buffer)
        arrays +=[np.array(im)]
        print(np.shape(im))
        plt.clf()
        

    # Array prep
    print('prepping')
    arrays = np.array(arrays)

    print(np.shape(arrays))
    arrays = np.moveaxis(arrays, -1, 1)
    arrays = arrays[:,:3]
    arrays = arrays//20*20
    print(np.shape(arrays))

    # Save as a gif
    print(np.min(arrays))
    print(np.max(arrays))
    write_gif(arrays, 'tester_direction.gif', fps = 20)