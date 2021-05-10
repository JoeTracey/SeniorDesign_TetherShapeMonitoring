import numpy  as  np
from matplotlib import pyplot as plt



# Define Functions 

#Turns strain into circumfrence length (divive 360 by length to get degrees per unit length)
def strainToCurve(ex,  y):
    #find length required to make 360 degrees at this strain
    theta = 360
    L = -theta*y/ex
    return(L)
    pass


if __name__ == '__main__':

    # Set Parameters 
    
    # y is offset from neutral axis, in this case offset from the center
    y1 = 1 #in
    y2 =-1 #in
    y3 = 2 #in


    e_list1 = -0.2+-np.linspace(0,1,100)[1:] #strains (unitless)
    e_list2 = e_list1*-1 #set second strains to be equal and opposite

    # Calculate strain vs circumfrence curves for each offset
    curve1 = [strainToCurve(e, y1) for e in e_list1]
    curve2 = [strainToCurve(e, y2) for e in e_list2]
    curve3 = [strainToCurve(e, y3) for e in e_list1*2]

    # Graph 

    #Sample with only fiber-y1
    plt.title("Length of Circle with Constant Strain (y1)")
    plt.plot(e_list1, curve1)
    plt.xlabel("strain at y=1in")
    plt.ylabel("Length Required (in)")
    plt.show()

    #Sample with only fiber-y2
    plt.title("Length of Circle with Constant Strain (y2)")
    plt.plot(e_list2, curve2)
    plt.xlabel("strain at y=-1in")
    plt.ylabel("Length Required (in)")
    plt.show()

    #Sample with both fiber-y1 and fiber-y2
    plt.title("Length of Circle with Constant Strain (opposite, equal offsets)")
    plt.plot(e_list1, curve1, '*', markersize = 10)
    plt.plot(-e_list2, curve2, '^')
    plt.legend(['y1', '-y2'])
    plt.xlabel("strain at y")
    plt.ylabel("Length Required (in)")
    plt.show()

    #Sample with y1 and y2, unequally offset from neutral axis
    plt.title("Length of Circle with Constant Strain (Unequal Offsets)")
    plt.plot(e_list1, curve1, '*', markersize = 10)
    plt.plot(e_list1*2, curve3, '^')
    plt.legend(['y1', 'y3'])
    plt.xlabel("strain at y")
    plt.ylabel("Length Required (in)")
    plt.show()
