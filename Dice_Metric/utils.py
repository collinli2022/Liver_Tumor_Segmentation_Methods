import os
import nibabel as nib


def openImage(fp):
    """
    Open up nifty image and convert to numpy arrays

    Paramaters
    ----------
    fp: string
        The file path to the nifty image

    Returns
    ----------
    img: numpy array
    vol: volume of image in cm³
    """
    
    if (not fp) or ('nii' not in fp):
        return

    nii = nib.load(fp)
    sx, sy, sz = nii.header.get_zooms()
    
    return nii.get_fdata(), sx*sy*sz/1000
def organizeFiles(fp):
    """
    Organize nifty files into array
    
    Parameters
    ----------
    fp: string
        The file path to the folder containing nifty images

    Returns
    ----------
    arr: array of file paths to numpy images
    """

    arr = []
    for f in os.listdir(fp):
        if 'nii' in f:
            arr.append(os.path.join(fp, f))
    return arr

def organizeFolders(fp):
    """
    Organize folders into array
    
    Paramaters
    ----------
    fp: string
        The file path to the folder containing nifty images

    Returns
    ----------
    arr: array of file paths to folders
    """

    print('DEBUG: list directories -', os.listdir(fp))

    arr = []
    for f in os.listdir(fp):
        if os.path.isdir(os.path.join(fp, f)):
            arr.append(os.path.join(fp, f))
    return arr
