import os
import wget
from datetime import datetime
from pathlib import Path 
import zipfile


class Download():
    """
    This class object regroup all the function to download all the needed files.
    You can download the DSM or DTM files for Flanders (it include BXL).
    /!\ BE AWARE THE FILES ARE EXTREMLY HEAVY, DO NOT DL THEM EVERYTIMES /!\ 
    Each type of file has his own directory inside a parent directory defined in the init.  
    """
    def __init__(self, dir_name='resources'):
        self.path_files_dir = os.path.join(os.path.abspath(''), f"{dir_name}")
        self.path_dsm_nl_zip = os.path.join(self.path_files_dir, "DSM_nl_zip")
        self.path_dtm_nl_zip = os.path.join(self.path_files_dir, "DTM_nl_zip")

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

    def unzip(self, type):
        if type == "dsm":
            for file in os.path.join(self.path_files_dir, Path("zip_files/DSM_NL")):
                with zipfile.ZipFile(file, 'r') as zip_file:
                    zip_file.extractall(os.path.join(self.path_files_dir, Path("unzip_files/DSM_NL")))
            

test = Download()
test.download_dsm_nl()