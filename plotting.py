from pyproj import Proj, Transformer
import os
from pathlib import Path
import rasterio
import rasterio.plot
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from geopy.geocoders import Nominatim
import fiona
import shapely.geometry
import geopandas as gpd

class Plotting():
    """
    This class object will regroup all technical functions to 
    plot a 3D houses based on our resources. 
    """
    def __init__(self) -> None:
        """
        Have to enter x as lattitude and y as longitude.
        """
        location = self.asking_address()
        self.x = location.latitude
        self.y = location.longitude
        self.left = 0
        self.bottom = 0
        self.right = 0
        self.top = 0
        self.dsm_gtif_path = os.path.join(os.path.abspath(''),Path("resources\DSM_nl_unzip\GeoTIFF"))
        self.dtm_gtif_path = os.path.join(os.path.abspath(''),Path("resources\DTM_nl_unzip\GeoTIFF"))
    
    def asking_address(self):
        """
        asking for an adress to the user and getting the gps coord from geopy.
        should add a full loop + if statement for when adderess == None.
        """
        geolocator = Nominatim(user_agent='3Dplotting')
        address_input = input("Enter an adress in Flanders or Brussels: ")
        print(geolocator.geocode(address_input))
        return geolocator.geocode(address_input)
        # return self.location.latitude, self.location.longitude

    def transform_coord(self) -> float:
        """
        transform the coord from gps to lambert
        """
        google_epsg = "epsg:4326"
        our_espg = "epsg:31370"
        ratio = Transformer.from_crs(google_epsg, our_espg)
        self.coord = ratio.transform(self.x, self.y)
        return self.coord
    
    def window_bounds(self, slice=25):
        """
        Create the 4 borders of our window.
        To not display the hole file. 
        """
        x = self.coord[0]
        y = self.coord[1]
        self.left = (x - slice)
        self.right = (x + slice)
        self.top = (y + slice)
        self.bottom = (y - slice)

    def wich_file(self) -> str:
        """
        Regarding the bounds of each geotiff file,
        we determine on which file our data is related.
        """
        for gtif in os.listdir(self.dsm_gtif_path):
            gtif_path = os.path.join(self.dsm_gtif_path, gtif)
            tiff = rasterio.open(gtif_path)
            if (tiff.bounds.left < self.coord[0] <tiff.bounds.right) and (tiff.bounds.bottom < self.coord[1]< tiff.bounds.top):
                # print(f"Our coordinates are inside the {gtif} file.")
                self.file_ok = gtif 
                return gtif_path
    
    def plot_2d(self, slice=25):
        """
        This method is able to print a 2D of the item. 
        Based on the window range difined by our slice.
        """
        self.window_bounds(slice=slice)
        tif_file_path = self.wich_file()
        with rasterio.open(tif_file_path) as src:
            w = src.read(1, window=rasterio.windows.from_bounds(self.left, self.bottom, self.right, self.top, transform=src.transform))
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111)
        ax.imshow(w)
        ax.set_title("Item in 2D")
        plt.show()

    def plot_3d(self, slice=25):
        """
        Allow to plot a 3D modelisation based on DSM and DTM files.
        """
        self.window_bounds(slice=slice)
        tif_file_path = self.wich_file()
        with rasterio.open(tif_file_path) as src_dsm:
            window = rasterio.windows.from_bounds(self.left, self.bottom, self.right, self.top, transform=src_dsm.transform)
            # window = rasterio.windows.from_bounds(self.shapefile_bounds())
            # window = rasterio.windows.bounds(self.shapefile_bounds(), transform=src_dsm.transform)
            fd_dsm = src_dsm.read(1, window=window)
        with rasterio.open(self.dtm_path()) as src_dtm:
            fd_dtm = src_dtm.read(1, window=window)
        cols, row = np.meshgrid(np.arange(fd_dsm.shape[1]), np.arange(fd_dsm.shape[0]))
        fig = go.Figure(data=[go.Surface(y=cols, x=row, z=(fd_dsm+fd_dtm))])
        pio.renderers.default = 'browser'
        fig.show()

    def ref_file(self) -> str:
        """
        Return the reference of the file. express in "k+nb".
        """
        file_inter = self.file_ok.replace("DHMVIIDSMRAS1m_", "")
        return file_inter[:-4]

    def shapefile_path(self) ->str:
        ref = self.ref_file()
        if ref == "k05":
            ref = "k5"
        unzip_path = os.path.join(os.path.abspath(''),Path("resources\DSM_nl_unzip"))
        return os.path.join(unzip_path, f"DHMVII_vdc_{ref}.shp")

    def dtm_path(self):
        # self.wich_file()
        dtm_file_name = self.file_ok.replace("DHMVIIDSMRAS1m_", "DHMVIIDTMRAS1m_")
        dtm_path = os.path.join(self.dtm_gtif_path, dtm_file_name)
        return dtm_path
    
    # def shapefile_bounds(self):
    #     """
    #     Taking the polygon value of our adderess coord. 
    #     """
    #     shape = gpd.read_file(self.shapefile_path())
    #     shape_bounds = shape.cx[self.left:self.right, self.bottom:self.top]
    #     polygon = shapely.geometry.Polygon(shape_bounds["geometry"])
    #     return polygon.bounds

        



addres = Plotting()
addres.transform_coord()
addres.wich_file()
# # # print(addres.x_bounds())
# # # print(addres.y_bounds())
print(addres.shapefile_path())
addres.plot_3d(slice=100)

# # # # print(addres.ref_file())
# # # addres.plot_2d(slice=250)