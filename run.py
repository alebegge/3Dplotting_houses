from download import Download
from plotting import Plotting

def asking(type):
    input_raw = input(f'Do you want to {type} ? (Y/N)\n').upper()
    if input_raw == 'Y' or input_raw == 'YES':
        return True
    else:
        return False
print("#"*60)
print("Welcome to our 3D plotting software!\n")
print("In order to work properly, we need first to download some heavy files and it may take a lot of time.")
print("#"*60)

test = Download()
if asking('download and extract all files'):
    test.paths_creating()
    test.download_dsm_nl()
    test.download_dtm_nl()
    test.unzip(dsm=1, dtm=1)

general_loop = True
while general_loop:
    house = Plotting()
    house.transform_coord()
    if asking('show a 2d plan'):
        house.plot_2d(slice=150)

    if asking('show a 3d modelisation'):
        slice = int(input("Which size if your input ? (Enter an integer)\n"))
        house.plot_3d(slice=slice)
    general_loop = asking('find another house/building')

