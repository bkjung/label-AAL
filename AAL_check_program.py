import csv
from tkinter import *
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

root = Tk()
#root.maxsize(500, 500) 
root.wm_title("AAL Check Program")

input_frame = LabelFrame(root, text="Input in World (Voxel) Coordinates") 
input_frame.grid(row=1, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
button_frame = LabelFrame(root, text="Buttons")
button_frame.grid(row=2, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
result_frame = LabelFrame(root, text="Results")
result_frame.grid(row=3, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

#Label(input_frame, text="Input in World (Voxel) Coordinates").grid(row=0, column=0, padx=5, pady=5)

#canvas1 = Canvas(root, width=500, height=500)
#canvas1.pack()

#entry1 = Entry(root)
#canvas1.create_window(210, 100, window=entry1)

#entry2 = Entry(root)
#canvas1.create_window(210, 140, window=entry2)

#entry3 = Entry(root)
#canvas1.create_window(210, 180, window=entry3)

label0 = Label(root, text='AAL Brain Region Check')
#label0.config(font=('helvetica', 20))
label0.grid(row=0, column=0, sticky='E', padx=5, pady=2)
#canvas1.create_window(200, 40, window=label0)

labelInput = Label(root, text='Input in World (Voxel) Coordinate')
labelInput.config(font=('helvetica', 12))
#canvas1.create_window(200, 70, window=labelInput)

#label1 = Label(root, text='Z:')  
#label1.config(font=('helvetica', 14))
#canvas1.create_window(100, 100, window=label1)

label_Z = Label(input_frame, text="Z:")
label_Z.grid(row=1, column=0, sticky='E', padx=5, pady=2)
#label1 = Label(input_frame, text='Z:')  
#label1.config(font=('helvetica', 14))
#label1.place(x=100, y=100)

label_X = Label(input_frame, text='X:')
label_X.grid(row=2, column=0, sticky='E', padx=5, pady=2)
#canvas1.create_window(100, 140, window=label2)

label_Y = Label(input_frame, text='Y:')
label_Y.grid(row=2, column=0, sticky='E', padx=5, pady=2)
#label_Y.config(font=('helvetica', 14))
#canvas1.create_window(100, 180, window=label3)

v = StringVar()
label4 = Label(root, textvariable = v, font=(
        'helvetica', 14, 'bold'), bg='white', width=25)
#canvas1.create_window(210, 300, window=label4)
#label4.pack()

label5 = Label(root, text='Result:')
label5.config(font=('helvetica', 14))
#canvas1.create_window(80, 300, window=label5)

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
    AAL = nifti_to_region_name(x, y, z)

    #label4 = Label(root, text=AAL, font=(
    #    'helvetica', 14, 'bold'), bg='white')
    #canvas1.create_window(210, 300, window=label4)
    v.set(AAL)
    logger.debug('INPUT Z, X, Y : %d %d %d', int(z), int(x), int(y))

# def combine_funcs(*funcs):
#     def combined_func(*args, **kwargs):
#         for f in funcs:
#             f(*args, **kwargs)
#     return combined_func

buttonCheck = Button(text='Check', command=check, bg='green',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)
#canvas1.create_window(210, 240, window=buttonCheck)

def reset():
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')
    v.set("")

buttonReset = Button(text='Reset', command=reset, bg='green',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)

#canvas1.create_window(210, 300, window=label4)

#buttonReset = Button(text='Reset', command=reset, bg='green',
#                        fg='white', font=('helvetica', 12, 'bold'), width=5)
                        
#canvas1.create_window(400, 120, window=buttonReset)

root.mainloop()
