import numpy as np
import re
from natsort import natsorted
from glob import glob
from PIL import Image
from numpy import asarray
from scipy.fft import fft
import os
from skimage import exposure


def load_fft(file_name : str):
    '''Docstring'''
    folder_path = os.path.abspath(f'/Users/Corty/Downloads/fft_arrays/**/')
    arr = None

    for file in glob(folder_path, recursive=True):
        pattern = re.compile(f"/{file_name}.npy")
        if pattern.search(file):
            arr = np.load(file, allow_pickle=True)

    return arr


def load_dataset(folder_path : str = os.path.abspath(f'/Users/Corty/Downloads/fft_arrays/**/')):
    '''Docstring'''
    data = {}
    anomalies = []
    for i in range(0,11):
        data[i] = []
        for path in natsorted(glob(folder_path, recursive=True)):
            pattern_1 = re.compile(f"arr_{i}/.+")
            if pattern_1.search(path):
                arr = np.load(path, allow_pickle=True)
                data[i].append(arr)

    for path in natsorted(glob(folder_path, recursive=True)):
        pattern_2 = re.compile(f"fft_anomalous_dice_arrays/.+")
        if pattern_2.search(path):
            arr = np.load(path, allow_pickle=True)
            anomalies.append(arr)

    return data, anomalies


##For normal dices
for j in range(0,11):
    folder_path = os.path.abspath('/Users/Corty/Downloads/')
    locationFiles=str(folder_path)+"/normal_dice/"+str(j)
    all_files = os.listdir(locationFiles)
    new_path = os.path.join(folder_path, 'fft_arrays/fft_normal_dice_arrays/arr_'+str(j))
    os.mkdir(new_path)
    text_files=[]
    for i in range(len(all_files)):
        if all_files[i][-4:]=='.jpg':
            # load the image
            image = Image.open(os.path.join(locationFiles, all_files[i]))
            image = image.convert('L')
            # convert image to numpy array
            data = asarray(image)
            data = exposure.adjust_gamma(data, gamma=1.1, gain=1.001)
            data = exposure.adjust_log(data, gain = 1.001)
            if j == 0:
                data = exposure.adjust_sigmoid(data, cutoff=0.20, gain=20, inv=False)
            else:
                data = exposure.adjust_sigmoid(data, cutoff=0.75, gain=15, inv=True)
            data = data[20:108, 20:108]
            data_fft = abs(fft(data))
            all_files[i] = all_files[i].replace('.jpg', '')
            np.save(os.path.join(new_path, all_files[i]), data_fft)
        else:
            continue

# x = np.load('./1001.npy')


##For anomalous_dices

folder_path = os.path.abspath('/Users/Corty/Downloads/')
locationFiles=str(folder_path)+"/anomalous_dice/"
all_files = os.listdir(locationFiles)
new_path = os.path.join(folder_path, 'fft_arrays/fft_anomalous_dice_arrays')
os.mkdir(new_path)
text_files=[]
for i in range(len(all_files)):
    if all_files[i][-4:]=='.jpg':
        # load the image
        image = Image.open(os.path.join(locationFiles, all_files[i]))
        image = image.convert('L')
        data = asarray(image)
        data = exposure.adjust_gamma(data, gamma=1.1, gain=1.001)
        data = exposure.adjust_log(data, gain=1.001)
        data = exposure.adjust_sigmoid(data, cutoff=0.55, gain=15, inv=True)
        data = data[20:108, 20:108]
        data_fft = abs(fft(data))
        all_files[i] = all_files[i].replace('.jpg', '')
        np.save(os.path.join(new_path, all_files[i]), data_fft)
    else:
        continue
