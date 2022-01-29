# Importing Libraries
import os
import nibabel as nib
import numpy as np
import scipy
from scipy import stats, optimize, interpolate
import pandas as pd
import matplotlib.pyplot as plt

from findSliceCountsUtils import getImageBoundaryThreshold, getImageBoundaryThreshold


# https://stackoverflow.com/questions/25524192/how-to-get-the-signal-to-noise-ratio-from-an-image-in-python
def signaltonoise(a, axis=2, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

# Main Folder Dir
fp = "./December Journal Submittion Cases v1"

# Maping file names to respective categories
file_map = {
    'vol' : 'dicom_vol',
    'LM' : 'JL_pred_vol',
    'GT' : 'GT_DR_liver_cyst_vol',
    'LS' : 'LevelSet_CL_liver_cyst_vol',
    'IRIS' : 'revisedLevelSet_CL_liver_cyst_vol'}

file_extension = '.nii.gz'

inv_file_map = {v: k for k, v in file_map.items()}

# Retrieve all files in the ROI directory
subdir, dirs, files = os.walk(fp).__next__()

df = pd.DataFrame(columns=[ 'patient_id', 'sagittal_slice_cnt', 'coronal_slice_cnt', 'axial_slice_cnt',
                            'mean_background', 'mean_liver_background', 'mean_just_liver_background', 'mean_liver_cyst',
                            'std_background', 'std_liver_background', 'std_just_liver_background', 'std_liver_cyst'])

for i in dirs:

    # Retrieve all files in the directory
    try:
        dicom_vol = nib.load(os.path.join(fp, i, file_map['vol']+".nii.gz")).get_data()
        LM_msk = nib.load(os.path.join(fp, i, file_map['LM']+".nii.gz")).get_data()
        GT_msk = nib.load(os.path.join(fp, i, file_map['GT']+".nii.gz")).get_data()
        # LS_msk = nib.load(os.path.join(fp, i, file_map['LS']+".nii.gz")).get_data()
        # IRIS_msk = nib.load(os.path.join(fp, i, file_map['IRIS']+".nii.gz")).get_data()
    except Exception as e:
        print("BIG ERROR FOR:", i)
        print(e)
        continue

    input_dict = {}
    
    # Patient ID
    input_dict['patient_id'] = i

    # Get the shape of the volume
    input_dict['sagittal_slice_cnt'] = dicom_vol.shape[0]
    input_dict['coronal_slice_cnt'] = dicom_vol.shape[1]
    input_dict['axial_slice_cnt'] = dicom_vol.shape[2]

    # Get image boundary
    minx, miny, minz, maxx, maxy, maxz = getImageBoundaryThreshold(dicom_vol, voxel_threshold = 25)
    print(minx, miny, minz, maxx, maxy, maxz)

    # Get the mean and std of the background
    background_msk = np.ones_like(dicom_vol)
    background_msk[minx:maxx, miny:maxy, minz:maxz] = 0
    input_dict['mean_background'] = np.mean(dicom_vol[background_msk == 1])
    input_dict['std_background'] = np.std(dicom_vol[background_msk == 1])

    # Get the mean and std of the liver background
    input_dict['mean_liver_background'] = np.mean(dicom_vol[LM_msk == 1])
    input_dict['std_liver_background'] = np.std(dicom_vol[LM_msk == 1])

    # Get the mean and std of the just liver background
    just_LM_msk = LM_msk - GT_msk
    input_dict['mean_just_liver_background'] = np.mean(dicom_vol[just_LM_msk == 1])
    input_dict['std_just_liver_background'] = np.std(dicom_vol[just_LM_msk == 1])

    # Get the mean and std of the liver cyst
    input_dict['mean_liver_cyst'] = np.mean(dicom_vol[GT_msk == 1])
    input_dict['std_liver_cyst'] = np.std(dicom_vol[GT_msk == 1])

    df = df.append(input_dict, ignore_index=True)

    ## DEBUG: show the image
    # dicom_vol[minx:maxx, miny:maxy, minz:maxz] = 5
    # print(dicom_vol[:,:,50].sum())
    # plt.imshow(dicom_vol[:, :, 50])
    # plt.show()
    # new_image = nib.Nifti1Image(dicom_vol, affine=np.eye(4))
    # nib.save(new_image, os.path.join('./', file_map['vol']+".nii.gz"))

print(df)
df.to_csv('./data_stats.csv')