# label-AAL

Find AAL brain atlas region name, from World(NIfTI)/MNI coordinate input !

This procedure is embedded in brain image programs(Vinci, MRIcron), but it's hard to find codes for those who want to develop their own program.

In the meantime, yunshiuan/label4MRI was the best source that I utilized, but it was in R code. I ported it to python for making GUI program. 

I also added World(NIfTI) coordinate input to MNI coordinate transformation (by using nilearn.image.coord_transform function), while yunshiuan/label4MRI only accepts MNI coordinate input.

## Environment
python 3.8.1

pip 19.3.1

## Prerequisites
Try following commands (there could be more)
```
pip install numpy
pip install numbers
```

## How to run
```
python AAL_check_program.py
```

## Windows Standalone GUI Program
![Program Example](https://raw.githubusercontent.com/bkjung/label-AAL/master/program_example.png)

Input : World (NifT) Coordinates
Output : AAL brain region name

Windows standalone (.exe) program can be created from the .py code.

Try following commands
```
pyinstaller --onefile --noconsole AAL_check_program.py
```

If numpy error happens, add following path to Windows PATH variable
```
C:\Users\rccd\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\numpy\.libs
```

In order to execute standalone program on Windows, following items in dist folder should be in the same folder

1) data folder
2) log folder
3) AAL_check_program.exe 



