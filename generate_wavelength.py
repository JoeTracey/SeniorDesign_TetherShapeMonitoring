import numpy  as  np
from matplotlib import pyplot as plt
import math


from calculate_rotation import find_theta
from strain_to_curve import *
from render_shape import *
from parser import *

##File computes the expected shift in C-band wavelength for each trial. Values are then printed out to be transfered into a data table

#Prepare data from bend force and rotation testing separately
bends = []
for i in [2,4,6,8,10,20,50,100,200]: #list of bend forces applied in Ansys
    bends+=[get_bend_data(i)] #parse bend data
bends = np.array(bends)
print(np.shape(bends))


rot_bends = []
for i in range(10): 
    i= 36*i #list of rotation angles tested in Ansys
    rot_bends +=[get_rotation_data(i)] #parse rotation data
rot_bends = np.array(rot_bends)
print(np.shape(rot_bends))



# Set material constants for photoelastic equations
gamma0 = 120 
neff = 1.457
p11 = 0.121
p12 = 0.270

#Define wavelength shift as function of materials constants using photoelastic equation, where e=strain
def find_shift(gamma0, e, neff=neff, p11=p11, p12=p12):
    dg = gamma0*(1-(neff/2)*(p11-p12))*e
    gamma = gamma0+dg
    return(dg, gamma)


# Find the wavelength shift for bend testing
print('results from wavelength shift, bend test')
print("[strain1,strain2,strain3,gammaA, shiftA,gammaB, shiftB,gammaC, shiftC]")
for trial in range(9):
        print('trial-'+str(trial))
        b = max(max(bends[trial,:,0].flatten()), abs(min(bends[trial,:,0].flatten())))
        c = max(max(bends[trial,:,1].flatten()), abs(min(bends[trial,:,1].flatten())))
        a = max(max(bends[trial,:,2].flatten()), abs(min(bends[trial,:,2].flatten())))
        if a != max(bends[trial,:,0].flatten()):
            a = -a
        if b != max(bends[trial,:,1].flatten()):
            b = -b
        if c != max(bends[trial,:,2].flatten()):
            c = -c
        shiftA, gammaA = find_shift(gamma0, a, neff, p11, p12)
        shiftB,gammaB = find_shift(gamma0, b, neff, p11, p12)
        shiftC,gammaC = find_shift(gamma0, c, neff, p11, p12)
        print([a,b,c,gammaA, shiftA,gammaB, shiftB,gammaC, shiftC])






# Find the wavelength shift for rotation testing
bends = rot_bends

print('results from wavelength shift, rotation test')
print("[strain1,strain2,strain3,gammaA, shiftA,gammaB, shiftB,gammaC, shiftC]")
for trial in range(10):
        print('trial-'+str(trial))
        b = max(max(bends[trial,:,0].flatten()), abs(min(bends[trial,:,0].flatten())))
        c = max(max(bends[trial,:,1].flatten()), abs(min(bends[trial,:,1].flatten())))
        a = max(max(bends[trial,:,2].flatten()), abs(min(bends[trial,:,2].flatten())))
        if a != max(bends[trial,:,0].flatten()):
            a = -a
        if b != max(bends[trial,:,1].flatten()):
            b = -b
        if c != max(bends[trial,:,2].flatten()):
            c = -c
        gammaA, shiftA = find_shift(gamma0, a, neff, p11, p12)
        gammaB, shiftB = find_shift(gamma0, b, neff, p11, p12)
        gammaC, shiftC = find_shift(gamma0, c, neff, p11, p12)
        print([a,b,c,gammaA, shiftA,gammaB, shiftB,gammaC, shiftC])
