import numpy as np


bending_loc = "./results/Bending/"
rotation_loc = "./results/Rotation/"

bending_set = [2,4,6,8,10]
Rotation_set = [0, 36, 27, 108, 144, 180, 216, 252, 288, 324]

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
    # print('Bending '+str(i)+' N')
    # print(nodes)
    # Get each strain Value
    # First Parse each segment
    full_strain_data = []
    for seg in range(8):
        seg+=1
        # print('Seg-'+str(seg))
        try:
            segment_text = open(bending_loc+str(i)+' N/location '+str(seg)+'/strain val.py')
        except(Exception):
            segment_text = open(bending_loc+str(i)+' N/location '+str(seg)+'/strain.py')

        segment_text = segment_text.read().split('EPTOXY')[-1]
        # print(segment_text)
        # Parse segment into fibers, based on their nodes
        strains =[]
        for f in range(3):
            # print('********')
            # print('node - '+str(nodes[f]))
            # print(segment_text)
            node_strain = segment_text.split('  '+str(nodes[f])+'  ')[-1]
            print(node_strain.split('     ')[1])
            if len(node_strain.split('     ')[1]) > 15:
                node_strain = node_strain.split('     ')[1]
                node_strain = node_strain.split(' ')
                print(node_strain)
                node_strain = [x for x in node_strain if x != '']
            else:
                node_straina = [node_strain.split('     ')[1]]
                node_strainb= node_strain.split('     ')[2]
                print(node_strainb)
                node_strainb =node_strainb.split(' ')

                print(node_strainb)
                node_strainb = [x for x in node_strainb if x != '']
                node_strain = node_straina + node_strainb
            xyz_strain = []
            print(node_strain)
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
        # print('Seg-'+str(seg))
        try:
            segment_text = open(rotation_loc+str(i)+' deg/location '+str(seg)+'/strain val.py')
        except(Exception):
            segment_text = open(rotation_loc+str(i)+' deg/location '+str(seg)+'/strain.py')

        segment_text = segment_text.read().split('EPTOXY')[-1]
        # print(segment_text)
        # Parse segment into fibers, based on their nodes
        strains =[]
        for f in range(3):
            # print('********')
            # print('node - '+str(nodes[f]))
            # print(segment_text)
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
    return(full_strain_data) #[8,3,3] [segment,fiber, xyz-strain]


# for i in range(5):
#     i= 2*i+2
#     get_bend_data(i)


# for i in range(10):
#     i= 36*i
#     get_rotation_data(i)
