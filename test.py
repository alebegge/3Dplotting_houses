from plotting import Plotting
from affine import Affine
import xarray as xr 
import geopandas as gpd
import matplotlib.pyplot as plt
import rioxarray

# test_wo = Plotting(50.83330365407295, 4.486695401854129)
# test_wo.transform_coord()

# path_gtif = test_wo.wich_file()

# # da = xr.open_rasterio(path_gtif)
# da = rioxarray.open_rasterio(path_gtif)
# transform = Affine.from_gdal(*da.attrs["transform"])

# fig = plt.figure(figsize=(15,15))
# ax = fig.add_subplot(111)
# ax.imshow(da.variable.data[0])
# ax.set_xlim(test_wo.x_bounds_calc(slice=250))
# ax.set_ylabel(test_wo.y_bounds_calc(slice=250))
# plt.show()

import fiona
import rasterio
import shapely.geometry
import numpy as np

from rasterstats.io import Raster
from PIL import Image

test=Plotting()
test.transform_coord()


tif_filename = test.wich_file()
dtm_file = test.dtm_path()
shape_file = test.shapefile_path()
with Raster(tif_filename, band=1) as dsm_file:
    with Raster(dtm_file, band=1) as dtm_file:
        index = 0
        for feat in fiona.open(shape_file):
            polygon_geometry = feat['geometry']
            polygon = shapely.geometry.Polygon(polygon_geometry['coordinates'][0])
            polygon_bounds = polygon.bounds

            raster_subset_1 = dsm_file.read(bounds=polygon_bounds)
            polygon_mask = rasterio.features.geometry_mask(geometries=[polygon_geometry],
                                                out_shape=(raster_subset_1.shape[0],raster_subset_1.shape[1]),
                                                transform=raster_subset_1.affine,
                                                all_touched=False,
                                                invert=True)

            raster_subset_2 = dtm_file.read(bounds=polygon_bounds)


            masked_1 = raster_subset_1.array * polygon_mask
            masked_2 = raster_subset_2.array * polygon_mask

            masked_all = np.dstack([masked_1, masked_2])

            img = Image.fromarray(masked_all[:, :, :].astype('uint8'), 'RGB')
            img.save('out/' + str(index) + '.jpg')
            index += 1