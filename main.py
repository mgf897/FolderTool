import os
import re
import shutil
			 
"""
Prepares project files for copying to Production Documents and the Solidworks Vault.

Scans a directory and sub-directories for files beginning with a part number
Performs a copy to a 'source' and/or 'output' folder depending on the file extensions
"""

__author__ = "Matthew Flynn"
__version__ = "0.1.0"

# Constants
REGEX_PART_NUMBER = r"(\d{3,4})-(\d{3,4})-(\d{2})"      # r at start of string need to prevent needing to escape backslashes
EXTS_SOURCE_FILES = ["ai","sldprt","slddrw","sldasm"]   # file types to be copied to source folder
EXTS_OUTPUT_FILES = ["pdf","step","stp"]                # filetypes to be copied to output folder

# Directories
project_path = r"C:\Users\310237398\OneDrive - Signify\Desktop\913703352909 DUS180WR-Faceplate-RAL1035"
target_source_path = r"C:\Users\310237398\OneDrive - Signify\Desktop\FolderTool\source"
target_output_path = r"C:\Users\310237398\OneDrive - Signify\Desktop\FolderTool\output"

# Flags
copy_source = False
copy_output = True

class File:
    def __init__(self, filename, root, size, destinations):
        self.filename = filename
        self.root = root
        self.size = size
        self.selected = False
        self.destinations = destinations


def main():
    """ Main entry point of the app """
    
    p = re.compile(REGEX_PART_NUMBER)
    
    job_files = []
    
    #
    # Scan a project path and create a list of planned file copies.
    #
    
    for root, dirs, files in os.walk(project_path): # r at start of string need to prevent unicode error
        for filename in files:
            re_part_number = p.match(filename)
            if re_part_number:
                file_ext = filename.split(".")[-1].lower()  # extract file extension 
                file_size = os.path.getsize((os.path.join(root, filename))) # filesize in bytes 
                part_number = re_part_number.group() # extract part number from regular expression match
                
                destinations = [] # destinations is a list in case a filetype is both a source and output filetype
                
                if (file_ext in EXTS_SOURCE_FILES) and copy_source:
                    destinations.append(f"{target_source_path}\{part_number}") 
                
                if (file_ext in EXTS_OUTPUT_FILES) and copy_output:
                    destinations.append(f"{target_output_path}\{part_number}")
                
                if destinations:               
                    job_files.append(File(filename,root,file_size,destinations))
                          
    #
    # Review files before copy (needs UI)
    # Mark files to be copied with the 'selected' class attribute
    #    
    
    #
    # Copy files
    #    
    for file in job_files:
        for i in range(len(file.destinations)):
            os.makedirs(file.destinations[i], exist_ok=True)
            dest = shutil.copy2(f"{file.root}\{file.filename}", f"{file.destinations[i]}\{file.filename}") # copy2 preserves metadata
            print(dest)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    
    
    
