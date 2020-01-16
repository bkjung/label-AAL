import csv
import tkinter as tk
import numpy as np
import math
import numbers
import logging
from datetime import datetime

logger = logging.getLogger('MainLogger')
logging.basicConfig(level=logging.DEBUG)

fh = logging.FileHandler('log/{:%Y%m%d_%H%M%S}.log'.format(datetime.now()))
formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.debug("Coordinate Logging Start")

root = tk.Tk()

root.title("AAL Check Program")

canvas1 = tk.Canvas(root, width=450, height=350)
canvas1.pack()

entry1 = tk.Entry(root)
canvas1.create_window(210, 100, window=entry1)

entry2 = tk.Entry(root)
canvas1.create_window(210, 140, window=entry2)

entry3 = tk.Entry(root)
canvas1.create_window(210, 180, window=entry3)

label0 = tk.Label(root, text='Coordinate - AAL check')
label0.config(font=('helvetica', 20))
canvas1.create_window(200, 30, window=label0)

label00 = tk.Label(root, text='(Type z,x,y in World(Voxel) Coordinates)')
label00.config(font=('helvetica', 15))
canvas1.create_window(200, 60, window=label00)

label1 = tk.Label(root, text='Z:')
label1.config(font=('helvetica', 14))
canvas1.create_window(100, 100, window=label1)

label2 = tk.Label(root, text='X:')
label2.config(font=('helvetica', 14))
canvas1.create_window(100, 140, window=label2)

label3 = tk.Label(root, text='Y:')
label3.config(font=('helvetica', 14))
canvas1.create_window(100, 180, window=label3)

v = tk.StringVar()
label4 = tk.Label(root, textvariable = v, font=(
        'helvetica', 14, 'bold'), bg='white', width=25)
canvas1.create_window(210, 300, window=label4)
label4.pack()

label5 = tk.Label(root, text='Result:')
label5.config(font=('helvetica', 14))
canvas1.create_window(50, 300, window=label5)

AAL = ""

with open('data/coordinate_list.csv', 'r') as f:
    reader = csv.reader(f)
    coordinate_list = np.array(list(reader))[[1, 2, 3], :].astype(np.integer)
    coordinate_list = coordinate_list[:, 1:]

with open('data/coordinate_label.csv', 'r') as f:
    reader = csv.reader(f)
    coordinate_label = np.array(list(reader))[1:, 1]

with open('data/region_name.csv', 'r') as f:
    reader = csv.reader(f)
    # First row is meaningless, but I left it to match the indexes properly
    region_name = np.array(list(reader))[:,1]
    

# def mni_to_region_index(x, y, z, distance=True):
def mni_to_region_index(x, y, z):
    matrix_index = (np.where(coordinate_list[0] == x))[0]
    matrix_index = np.extract(
        coordinate_list[1][matrix_index] == y, matrix_index)
    matrix_index = np.extract(
        coordinate_list[2][matrix_index] == z, matrix_index)

    if (len(matrix_index) != 0):
        index_num = matrix_index[0]  # starting from 0
        # Coordinate_label "real value" starts from 1, but its python index number starts from 0)
        r_index = int(coordinate_label[index_num])
        #r_distance = 0 if distance else "NULL"
        r_distance = 0

    else:
        # if (distance):
        target_point = np.array((x, y, z))
        subtracted_matrix = np.array(list(zip(*coordinate_list)))-target_point
        d2_list = np.linalg.norm(subtracted_matrix, axis=1)
        r_index = int(coordinate_label[np.argmin(d2_list)])
        r_distance = d2_list[r_index]

        #
        # else:
        #  r_index = "NULL"
        #  r_distance = "NULL"

    return(r_index, r_distance)


# def mni_to_region_name(x, y, z, distance = True):
def mni_to_region_name(x, y, z):
    x = round(x)
    y = round(y)
    z = round(z)

    (r_index, r_distance) = mni_to_region_index(x, y, z)
    # df_region_index_name <- label4mri_metadata[[.template]]$label

    return region_name[r_index]

# I revised and used nilearn.image.coord_transform function.
def nifti_to_mni(x, y, z):
    affine = [[-2.,    0.,    0.,   90.], 
    [0.,    2.,    0., -126.],
    [0.,    0.,    2.,  -72.],
    [0.,    0.,    0.,    1.]]
    

    #squeeze = (not hasattr(x, '__iter__'))
    #return_number = isinstance(x, numbers.Number)
    x = np.asanyarray(x)
    shape = x.shape
    coords = np.c_[np.atleast_1d(x).flat,
                   np.atleast_1d(y).flat,
                   np.atleast_1d(z).flat,
                   np.ones_like(np.atleast_1d(z).flat)].T

    coords = coords.astype(np.float)

    #affine = map(lambda x: float(x), affine)
    #coords = map(lambda x: float(x), coords)
    
    _x, _y, _z, _ = np.dot(affine, coords)
    #if return_number:
    #print("MNI coordinate :", _x.item(), _y.item(), _z.item())
    return _x.item(), _y.item(), _z.item()
    #if squeeze:
    #    return _x.squeeze(), _y.squeeze(), _z.squeeze()
    #return np.reshape(_x, shape), np.reshape(_y, shape), np.reshape(_z, shape)


def nifti_to_region_name(x, y, z):
    (_x, _y, _z) = nifti_to_mni(x, y, z)

    return (mni_to_region_name(_x, _y, _z))

def check():
    z = entry1.get()
    x = entry2.get()
    y = entry3.get()

    #print("INPUT nifti coordinate : ", x, y, z)
    global AAL
    AAL = nifti_to_region_name(x, y, z)

    #label4 = tk.Label(root, text=AAL, font=(
    #    'helvetica', 14, 'bold'), bg='white')
    #canvas1.create_window(210, 300, window=label4)
    v.set(AAL)
    #logger.debug('INPUT Z, X, Y : %d %d %d', int(z), int(x), int(y))

# def combine_funcs(*funcs):
#     def combined_func(*args, **kwargs):
#         for f in funcs:
#             f(*args, **kwargs)
#     return combined_func

buttonCheck = tk.Button(text='Check', command=check, bg='green',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)
canvas1.create_window(210, 240, window=buttonCheck)

def save():
    z = entry1.get()
    x = entry2.get()
    y = entry3.get()

    #AAL = nifti_to_region_name(x, y, z)

    logger.debug('INPUT Z, X, Y : %d %d %d / AAL region : %s', int(z), int(x), int(y), AAL)

buttonSave = tk.Button(text='Save', command=save, bg='blue',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)
canvas1.create_window(400, 240, window=buttonSave)

def reset():
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')
    v.set("")

buttonReset = tk.Button(text='Reset', command=reset, bg='grey',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)

canvas1.create_window(210, 300, window=label4)

#buttonReset = tk.Button(text='Reset', command=reset, bg='green',
#                        fg='white', font=('helvetica', 12, 'bold'), width=5)
                        
canvas1.create_window(400, 120, window=buttonReset)

root.mainloop()
