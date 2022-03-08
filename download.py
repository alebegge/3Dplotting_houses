import os
import wget
from datetime import datetime
from pathlib import Path 
from zipfile import ZipFile


class Download():
    """
    This class object regroup all the function to download all the needed files.
    You can download the DSM or DTM files for Flanders (it include BXL).
    /!\ BE AWARE THE FILES ARE EXTREMLY HEAVY, DO NOT DL THEM EVERYTIMES /!\ 
    Each type of file has his own directory inside a parent directory defined in the init.  
    """
    def __init__(self, dir_name='resources'):
        self.dir_name = dir_name
        self.path_files_dir = os.path.join(os.path.abspath(''), f"{self.dir_name}")
        self.path_dsm_nl_zip = os.path.join(self.path_files_dir, "DSM_nl_zip")
        self.path_dsm_nl_unzip = os.path.join(self.path_files_dir, "DSM_nl_unzip")
        self.path_dtm_nl_zip = os.path.join(self.path_files_dir, "DTM_nl_zip")
        self.path_dtm_nl_unzip = os.path.join(self.path_files_dir, "DTM_nl_unzip")
    
    def paths_creating(self):
        """
        Check if the directory are existing. If not, create them.
        """
        if not os.path.exists(self.path_dsm_nl_zip):
            os.makedirs(self.path_dsm_nl_zip)
            os.makedirs(self.path_dtm_nl_zip)
            print(f"--- All directory created ---")
        if not os.path.exists(self.path_dsm_nl_unzip):
            os.makedirs(self.path_dsm_nl_unzip)
            os.makedirs(self.path_dtm_nl_unzip)
            print(f"--- All directory created ---")
        elif os.path.exists(self.path_files_dir):
            print(f"--- All directory already exists ---")
        else:
            print("Error. Unable to create directories.")

    def download_dsm_nl(self, start=1, end=43):
        """
        Allow us to download all DSM files for NL.
        """
        start_time = datetime.now()
        count = 0
        for i in range(start, (end + 1)):
            if i < 10:
                file_name = f"DSM_NL_0{i}.zip"
                path_file = os.path.join(self.path_dsm_nl_zip, file_name)
                if not os.path.isfile(path_file):
                    wget.download(f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_k0{i}.zip", path_file)
                    count += 1
            if i >= 10:
                file_name = f"DSM_NL_{i}.zip"
                path_file = os.path.join(self.path_dsm_nl_zip, file_name)
                if not os.path.isfile(path_file):
                    wget.download(f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_k{i}.zip", path_file)
                    count += 1
        print("\n")
        print(f"All files downloaded. It tooks {(datetime.now() - start_time )} hours to get thoses {count} files.")

    def download_dtm_nl(self, start=1, end=43):
        """
        Allow us to download all DTM files for NL.
        """
        start_time = datetime.now()
        count = 0
        for i in range(start, (end + 1)):
            if i < 10:
                file_name = f"DTM_NL_0{i}.zip"
                path_file = os.path.join(self.path_dtm_nl_zip, file_name)
                if not os.path.isfile(path_file):
                    wget.download(f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_k0{i}.zip", path_file)
                    count += 1
            if i >= 10:
                file_name = f"DTM_NL_{i}.zip"
                path_file = os.path.join(self.path_dtm_nl_zip, file_name)
                if not os.path.isfile(path_file):
                    wget.download(f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_k{i}.zip", path_file) 
                    count += 1
        print("\n")
        print(f"All files downloaded. It tooks {(datetime.now() - start_time )} hours to get thoses {count} files.")

    def unzip(self, dsm=0, dtm=0):
        """
        Allow us to unzip the files. Extract all shapefile and geotiff before removing the zip folder.
        """
        if dsm == 1:
            for dirz in os.listdir(self.path_dsm_nl_zip):
                os.chdir(self.path_dsm_nl_zip)
                with ZipFile(dirz,'r') as zipdir:
                    list_files = zipdir.namelist()
                    zipdir.extractall(path=self.path_dsm_nl_unzip)
                    print(f"------ All Files from {dirz} extracted ----- ")
            for shpdir in os.listdir(self.path_dsm_nl_unzip):
                os.chdir(self.path_dsm_nl_unzip)
                if shpdir.endswith('.zip'):
                    with ZipFile(shpdir, 'r') as shpzip:
                        shpzip.extractall()
                        print(f"{shpdir} correctly extracted.")
                    os.remove(shpdir)
            print("######## ALL DATA EXTRACTED ########")

        if dtm == 1:
            for dirz in os.listdir(self.path_dtm_nl_zip):
                os.chdir(self.path_dtm_nl_zip)
                with ZipFile(dirz,'r') as zipdir:
                    list_files = zipdir.namelist()
                    zipdir.extractall(path= self.path_dtm_nl_unzip)
                    print(f"------ All Files from {dirz} extracted ----- ")
            for shpdir in os.listdir(self.path_dtm_nl_unzip):
                os.chdir(self.path_dtm_nl_unzip)
                if shpdir.endswith('.zip'):
                    with ZipFile(shpdir, 'r') as shpzip:
                        shpzip.extractall()
                        print(f"{shpdir} correctly extracted.")
                    os.remove(shpdir)
            print("######## ALL DATA EXTRACTED ########")
            
        if dsm == 0 and dtm ==  0:
            print("Please enter which data you would like to extract.")
            print("If you would like to extract dsm files, please enter 'dsm=1'.")
            print("If you would like to extract dtm files, please enter 'dtm=1'.")