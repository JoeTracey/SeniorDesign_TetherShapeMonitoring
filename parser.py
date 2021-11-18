import numpy as np

#Functions in charge of parsing out data from saved Ansys simulation results
bending_loc = "./results/Bending/"
rotation_loc = "./results/Rotation/"


def get_bend_data(i):
    # Get nodes
    node_text = open(bending_loc+'NODE FILTERS.txt')
    #select rotation nodes to use
    node_string = node_text.read().split('0')[-1]
    #get each fibers node
    nodes = []
    for f in range(3):
        f+=1
        node = node_string.split(' - Fiber '+str(f))[0]
        node = node.split('ODE ')[-1]
        nodes+=[node]
    # Get each strain Value
    # First Parse each segment
    full_strain_data = []
    for seg in range(8):
        seg+=1
        #try both naming methods that were used
        try:
            segment_text = open(bending_loc+str(i)+' N/location '+str(seg)+'/strain val.py')
        except(Exception):
            segment_text = open(bending_loc+str(i)+' N/location '+str(seg)+'/strain.py')

        segment_text = segment_text.read().split('EPTOXY')[-1]
        # Parse segment into fibers, based on their nodes
        strains =[]
        for f in range(3):
            node_strain = segment_text.split('  '+str(nodes[f])+'  ')[-1]
            if len(node_strain.split('     ')[1]) > 15:
                node_strain = node_strain.split('     ')[1]
                node_strain = node_strain.split(' ')
                node_strain = [x for x in node_strain if x != '']
            else:
                node_straina = [node_strain.split('     ')[1]]
                node_strainb= node_strain.split('     ')[2]
                node_strainb =node_strainb.split(' ')
                node_strainb = [x for x in node_strainb if x != '']
                node_strain = node_straina + node_strainb
            xyz_strain = []
            for x in range(3): #convert xyz strains to floats
                node_strain[x] = float(node_strain[x])
                xyz_strain+=[node_strain[x]]
            strains+=[xyz_strain]
        #return 3 xyz strain tensors (one for each fiber) [3,3] array
        full_strain_data += [strains]
    full_strain_data = np.array(full_strain_data)
    # print(full_strain_data)
    return(full_strain_data) #[8,3,3] [segment,fiber, xyz-strain]



def get_rotation_data(i):
    # Get nodes for this angle
    node_text = open(rotation_loc+'NODE FILTERS.txt')
    #select rotation nodes to use
    node_string = node_text.read().split(' '+str(i)+'  ')[-1]
    #get each fibers node
    nodes = []
    for f in range(3):
        f+=1
        node = node_string.split(' - Fiber '+str(f))[0]
        node = node.split('ODE ')[-1]
        nodes+=[node]
    print('Rotation '+str(i)+' N')
    print(nodes)
    # Get each strain Value
    # First Parse each segment
    full_strain_data = []
    for seg in range(8):
        seg+=1
        #Try opening files saved under both naming formats
        try:
            segment_text = open(rotation_loc+str(i)+' deg/location '+str(seg)+'/strain val.py')
        except(Exception):
            segment_text = open(rotation_loc+str(i)+' deg/location '+str(seg)+'/strain.py')

        segment_text = segment_text.read().split('EPTOXY')[-1]
        # Parse segment into fibers, based on their nodes
        strains =[]
        for f in range(3):
            node_strain = segment_text.split(' '+str(nodes[f])+' ')[-1]
            node_strain = node_strain.split('     ')[1]
            node_strain = node_strain.split(' ')
            node_strain = [x for x in node_strain if x != '']
            xyz_strain = []
            for x in range(3): #convert xyz strains to floats
                node_strain[x] = float(node_strain[x])
                xyz_strain+=[node_strain[x]]
            strains+=[xyz_strain]
        #return 3 xyz strain tensors (one for each fiber) [3,3] array
        full_strain_data += [strains]
    full_strain_data = np.array(full_strain_data)
    print(full_strain_data)
    return(full_strain_data) 


## Test out get_bend_data on some Ansys files
# for i in range(5):
#     i= 2*i+2
#     get_bend_data(i)

## Test out get_rotation_data on Ansys files
# for i in range(10):
#     i= 36*i
#     get_rotation_data(i)
