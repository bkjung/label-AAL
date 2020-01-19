import csv
import tkinter as tk
from tkinter import messagebox
import numpy as np
import math
import numbers
import logging
#import os, errno
from datetime import datetime


AAL, z, x, y = "", 0, 0, 0
warning_check = ""
flag_checked = False
flag_coordinates_changed_after_check = False

logger = logging.getLogger('MainLogger')
logging.basicConfig(level=logging.DEBUG)

#try:
#    os.makedirs('log')
#except OSError as e:
#    if e.errno != errno.EEXIST:
#        raise

fh = logging.FileHandler('log/{:%Y%m%d_%H%M%S}.log'.format(datetime.now()))
formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)
#logger.debug("Coordinate Logging Start")

root = tk.Tk()
root.title("AAL Check Program")

c = tk.Canvas(root, width=450, height=420)
c.pack()

label_title = tk.Label(root, text='Coordinate - AAL check')
label_title.config(font=('helvetica', 20))
c.create_window(220, 30, window=label_title)

label_subtitle = tk.Label(root, text='(Type z,x,y in Voxel Coordinates)')
label_subtitle.config(font=('helvetica', 15))
c.create_window(220, 60, window=label_subtitle)

label_patient_no = tk.Label(root, text='Patient #')
label_patient_no.config(font=('helvetica', 11))
c.create_window(40, 110, window=label_patient_no)

entry_patient_no = tk.Entry(root)
entry_patient_no.config(width=10)
c.create_window(115, 110, window=entry_patient_no)

label_severity = tk.Label(root, text='Severity')
label_severity.config(font=('helvetica', 11))
c.create_window(190, 110, window=label_severity)

entry_severity = tk.Entry(root)
entry_severity.config(width=10)
c.create_window(265, 110, window=entry_severity)

label_area = tk.Label(root, text='Area')
label_area.config(font=('helvetica', 11))
c.create_window(340, 110, window=label_area)

entry_area = tk.Entry(root)
entry_area.config(width=10)
c.create_window(400, 110, window=entry_area)

label_z = tk.Label(root, text='z')
label_z.config(font=('helvetica', 12))
c.create_window(50, 170, window=label_z)

label_x = tk.Label(root, text='x')
label_x.config(font=('helvetica', 12))
c.create_window(50, 210, window=label_x)

label_y = tk.Label(root, text='y')
label_y.config(font=('helvetica', 12))
c.create_window(50, 250, window=label_y)

def callback_change(sv):
    global flag_coordinates_changed_after_check, warning_check
    flag_coordinates_changed_after_check = True
    warning_check = "좌표값 변경 감지\nCheck 버튼 눌러야함"
    warning_check_var.set(warning_check)


sv_z = tk.StringVar()
sv_z.trace("w", lambda name, index, mode, sv_z=sv_z: callback_change(sv_z))
entry_z = tk.Entry(root, textvariable=sv_z)
entry_z.pack()
c.create_window(150, 170, window=entry_z)

sv_x = tk.StringVar()
sv_x.trace("w", lambda name, index, mode, sv_x=sv_x: callback_change(sv_x))
entry_x = tk.Entry(root, textvariable=sv_x)
entry_x.pack()
c.create_window(150, 210, window=entry_x)

sv_y = tk.StringVar()
sv_y.trace("w", lambda name, index, mode, sv_y=sv_y: callback_change(sv_y))
entry_y = tk.Entry(root, textvariable=sv_y)
entry_y.pack()
c.create_window(150, 250, window=entry_y)

label_AAL = tk.Label(root, text='AAL:')
label_AAL.config(font=('helvetica', 12))
c.create_window(50, 320, window=label_AAL)

AAL_var = tk.StringVar()
label_AAL_value = tk.Label(root, textvariable = AAL_var, font=(
        'helvetica', 12, 'bold'), bg='white', width=30)
c.create_window(230, 320, window=label_AAL_value)

warning_check_var = tk.StringVar()
label_warning_check = tk.Label(root, textvariable = warning_check_var, font=(
        'helvetica', 10, 'bold'), width=15)
c.create_window(350, 270, window=label_warning_check)

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
def voxel_to_mni(x, y, z):
    affine = [[-2.,    0.,    0.,   90.], 
    [0.,    2.,    0., -126.],
    [0.,    0.,    2.,  -72.],
    [0.,    0.,    0.,    1.]]
    

    #squeeze = (not hasattr(x, '__iter__'))
    #return_number = isinstance(x, numbers.Number)
    x = np.asanyarray(x)
    #shape = x.shape
    coords = np.c_[np.atleast_1d(x).flat,
                   np.atleast_1d(y).flat,
                   np.atleast_1d(z).flat,
                   np.ones_like(np.atleast_1d(z).flat)].T

    coords = coords.astype(np.float)

    #affine = map(lambda x: float(x), affine)
    #coords = map(lambda x: float(x), coords)
    
    _x, _y, _z, _ = np.dot(affine, coords)
    #if return_number:
    #print("mni coordinate :", _x.item(), _y.item(), _z.item())
    return _x.item(), _y.item(), _z.item()
    #if squeeze:
    #    return _x.squeeze(), _y.squeeze(), _z.squeeze()
    #return np.reshape(_x, shape), np.reshape(_y, shape), np.reshape(_z, shape)


def voxel_to_region_name(x, y, z):
    (_x, _y, _z) = voxel_to_mni(x, y, z)

    return (mni_to_region_name(_x, _y, _z))

def check():
    global z, x, y, flag_checked, flag_coordinates_changed_after_check, warning_check
    z = entry_z.get()
    x = entry_x.get()
    y = entry_y.get()

    if z=='' or x=='' or y=='':
        messagebox.showinfo("Warning", "좌표값이 비어있음")

    else:        
        flag_checked = True
        flag_coordinates_changed_after_check = False
        warning_check = ""

        #print("INPUT voxel coordinate : ", x, y, z)
        global AAL
        AAL = voxel_to_region_name(x, y, z)

        #label4 = tk.Label(root, text=AAL, font=(
        #    'helvetica', 14, 'bold'), bg='white')
        #c.create_window(210, 300, window=label4)
        AAL_var.set(AAL)
        warning_check_var.set(warning_check)
        #logger.debug('INPUT Z, X, Y : %d %d %d', int(z), int(x), int(y))

# def combine_funcs(*funcs):
#     def combined_func(*args, **kwargs):
#         for f in funcs:
#             f(*args, **kwargs)
#     return combined_func

def save():
    #AAL = voxel_to_region_name(x, y, z)
    patient_no = entry_patient_no.get()
    severity = entry_severity.get()
    area = entry_area.get()

    if patient_no=='' or severity=='' or area=='':
        messagebox.showinfo("Warning", "환자 정보가 비어있음")

    elif not flag_checked or flag_coordinates_changed_after_check:
        messagebox.showinfo("Warning", "좌표값이 비어있거나, Check 버튼을 누르지 않았음")

    else:
        logger.debug(' PATIENT# %d / SEVERITY %s / AREA %s / INPUT_Z,X,Y %d %d %d / AAL %s', int(patient_no), severity, area, int(z), int(x), int(y), AAL)
        reset()
        

def reset():
    global z, x, y, flag_checked, flag_coordinates_changed_after_check, warning_check, AAL
    entry_z.delete(0, 'end')
    entry_x.delete(0, 'end')
    entry_y.delete(0, 'end')
    entry_patient_no.delete(0, 'end')
    entry_severity.delete(0, 'end')
    entry_area.delete(0, 'end')

    z, x, y, flag_checked, flag_coordinates_changed_after_check, warning_check, AAL = 0, 0, 0, False, False, "", ""
    
    AAL_var.set("")
    warning_check_var.set(warning_check)

buttonCheck = tk.Button(text='Check', command=check, bg='green',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)
c.create_window(350, 230, window=buttonCheck)

buttonReset = tk.Button(text='Reset', command=reset, bg='grey',
                        fg='white', font=('helvetica', 12, 'bold'), width=5)                        
c.create_window(350, 180, window=buttonReset)

buttonSave = tk.Button(text='Save & Reset', command=save, bg='blue',
                        fg='white', font=('helvetica', 12, 'bold'), width=13)
c.create_window(210, 370, window=buttonSave)

root.mainloop()
