import pandas as pd
import geopandas as gpd
import numpy as np 
import matplotlib as plt
from pyarrow import feather

test = gpd.read_feather("resources\DSM_nl_unzip\one\DHMVII_vdc_k01\DHMVII_vdc_k01.shp")
print(test)