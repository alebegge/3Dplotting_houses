from plotting import Plotting
from affine import Affine
import xarray as xr 
import geopandas as gpd
import matplotlib.pyplot as plt
import rioxarray

test_wo = Plotting(50.83330365407295, 4.486695401854129)
test_wo.transform_coord()

path_gtif = test_wo.wich_file()

# da = xr.open_rasterio(path_gtif)
da = rioxarray.open_rasterio(path_gtif)
transform = Affine.from_gdal(*da.attrs["transform"])

fig = plt.figure(figsize=(15,15))
ax = fig.add_subplot(111)
ax.imshow(da.variable.data[0])
ax.set_xlim(test_wo.x_bounds_calc(slice=250))
ax.set_ylabel(test_wo.y_bounds_calc(slice=250))
plt.show()

