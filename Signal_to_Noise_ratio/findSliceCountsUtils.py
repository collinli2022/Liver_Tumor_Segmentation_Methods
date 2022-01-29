import numpy as np

def getImageBoundaryUniqueValues(mask, unique_values_threshold = 5):
    
    minx = miny = minz = 0
    maxx = maxy = maxz = 0

    n,m,p = mask.shape

    for i in range(n):
        uniques = np.unique(mask[i,:,:])
        if len(uniques) > unique_values_threshold:
            minx = i
            break
    
    for i in range(n-1,-1,-1):
        uniques = np.unique(mask[i,:,:])
        if len(uniques) > unique_values_threshold:
            maxx = i
            break

    for i in range(m):
        uniques = np.unique(mask[:,i,:])
        if len(uniques) > unique_values_threshold:
            miny = i
            break
    
    for i in range(m-1,-1,-1):
        uniques = np.unique(mask[:,i,:])
        if len(uniques) > unique_values_threshold:
            maxy = i
            break
    
    for i in range(p):
        uniques = np.unique(mask[:,:,i])
        if len(uniques) > unique_values_threshold:
            minz = i
            break
    
    for i in range(p-1,-1,-1):
        uniques = np.unique(mask[:,:,i])
        if len(uniques) > unique_values_threshold:
            maxz = i
            break

    return minx, miny, minz, maxx, maxy, maxz


def getImageBoundaryThreshold(mask, voxel_threshold = 10):
    
    minx = miny = minz = 0
    maxx = maxy = maxz = 0

    n,m,p = mask.shape

    for i in range(n):
        if mask[i,:,:].max() > voxel_threshold:
            minx = i
            break
    
    for i in range(n-1,-1,-1):
        if mask[i,:,:].max() > voxel_threshold:
            maxx = i
            break

    for i in range(m):
        if mask[:,i,:].max() > voxel_threshold:
            miny = i
            break
    
    for i in range(m-1,-1,-1):
        if mask[:,i,:].max() > voxel_threshold:
            maxy = i
            break
    
    for i in range(p):
        if mask[:,:,i].max() > voxel_threshold:
            minz = i
            break
    
    for i in range(p-1,-1,-1):
        if mask[:,:,i].max() > voxel_threshold:
            maxz = i
            break

    return minx, miny, minz, maxx+1, maxy+1, maxz+1 # To account for the fact that the max is not included in the mask