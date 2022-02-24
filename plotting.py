from pyproj import Proj, Transformer
import os
from pathlib import Path
import rasterio
import rasterio.plot
from rasterio.plot import show
from matplotlib import pyplot


class Plotting():
    """
    This class object will regroup all technical functions to 
    plot a 3D houses based on our resources. 
    """
    def __init__(self, x, y) -> None:
        """
        Have to enter x as lattitude and y as longitude.
        """
        self.x = x
        self.y = y
        self.dsm_gtif_path = os.path.join(os.path.abspath(''),Path("resources\DSM_nl_unzip\GeoTIFF"))
        self.dtm_gtif_path = os.path.join(os.path.abspath(''),Path("resources\DTM_nl_unzip\GeoTIFF"))

    def transform_coord(self) -> float:
        google_epsg = "epsg:4326"
        our_espg = "epsg:31370"
        ratio = Transformer.from_crs(google_epsg, our_espg)
        self.coord = ratio.transform(self.x, self.y)
        return self.coord
    
    def x_bounds_calc(self, slice=25):
        x = self.transform_coord()[0]
        return [x - slice, x + slice]

    def y_bounds_calc(self, slice=25):
        y = self.transform_coord()[1]
        return [y - slice, y + slice]
    
    # def zoomed_bounds(self, slice = 25):
    #     x = self.transform_coord()[0]
    #     y = self.transform_coord()[1]
    #     return ([(x - slice, y-slice),(x-slice, y+slice),(x+slice,y - slice), (x + slice, y+slice)])
    

    def wich_file(self) -> str:
        """
        Regarding the bounds of each geotiff file,
        we determine on which file our data is related.
        """
        for gtif in os.listdir(self.dsm_gtif_path):
            gtif_path = os.path.join(self.dsm_gtif_path, gtif)
            tiff = rasterio.open(gtif_path)
            if (tiff.bounds.left < self.coord[0] <tiff.bounds.right) and (tiff.bounds.bottom < self.coord[1]< tiff.bounds.top):
                print(f"Our coordinates are inside the {gtif} file.")
                self.file_ok = gtif 
                return gtif_path
    
    def plot_2d(self, slice=5):
        """
        This method is able to print a 2D of the item. 
        Slice is the size of the slicing of our item.
        """
        x_bounds = [self.coord[0] - slice, self.coord[0] + slice]
        y_bounds = [self.coord[1] - slice, self.coord[1] + slice]
        src = rasterio.open(self.wich_file())
        fig, ax = pyplot.subplots(1, figsize=(15,15))
        ax.set_xlim(x_bounds)
        ax.set_ylim(y_bounds)
        ax.set_title("Item in 2D")
        show(src.read(),transform=src.transform, cmap='terrain_r',ax=ax)
        pyplot.show()
    
    def ref_file(self) -> str:
        """
        Return the reference of the file. express in "k+nb".
        """
        file_inter = self.file_ok.replace("DHMVIIDSMRAS1m_", "")
        return file_inter[:-4]
        


addres = Plotting(50.85488630639823, 4.3579057964208685)
addres.transform_coord()
# print(addres.x_bounds())
# print(addres.y_bounds())
addres.wich_file()
# # # print(addres.ref_file())
# # addres.plot_2d(slice=250)