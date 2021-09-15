import os
import re
import shutil
import win32com.client
			 
"""
Prepares project files for copying to Production Documents and the Solidworks Vault.

Scans a directory and sub-directories for files beginning with a part number
Performs a copy to a 'source' and/or 'output' folder depending on the file extensions
"""

__author__ = "Matthew Flynn"
__version__ = "0.1.0"

# Constants
# ==================
#
# Use r before string to prevent needing to escape backslashes
# Regular expression tested with https://regexr.com/ and "sample part numbers.txt"
#
#REGEX_PART_NUMBER = r"(\d{3,4})-(\d{3,4})-(\d{2})"      # all part numbers
REGEX_PART_NUMBER = r"(^((1050|1100|2[2,5-8][0-9])-((\d{3,4}-\d{2})|\d{3,4}))|(9137)\d{8})" # Mechanical partnumbers and Dynalite 12NCs

# Mechanical files
# 220
# 250
# 260 - Metal parts
# 262 - Metal assemblies
# 265 - Engravings
# 268 - 
# 270 - 
# 280 - Plastic parts
# 282 - Plastic assemblies
# 285 - Glass
# 1050 - Labels
# 1100 - Cartons
# 12NC - Top level products

EXTS_SOURCE_FILES = ["ai","sldprt","slddrw","sldasm","x_t","pdf","step","stp"]  # file types to be copied to source folder
EXTS_OUTPUT_FILES = ["pdf","step","stp"]                                        # filetypes to be copied to output folder

# Directories
# ==================

# Directory to be searched
project_path = r"C:\Users\310237398\OneDrive - Signify\Desktop\PDR8E"

# Destination for files matching EXTS_SOURCE_FILES filetypes
target_source_path = r"C:\Users\310237398\OneDrive - Signify\Desktop\FolderTool\source"

# Destination for files matching EXTS_OUTPUT_FILES filetypes
target_output_path = r"C:\Users\310237398\OneDrive - Signify\Desktop\FolderTool\output"


# Flags
# ==================

flag_find_source_files = True
flag_find_output_files = False
flag_create_copy_note_per_file = True
flag_create_shortcut = False
flag_copy_files = False
flag_create_hardlink = True
flag_log_duplicates = True


class File:
    def __init__(self, filename, root, size, destinations,part_number,part_code):
        self.filename = filename
        self.root = root
        self.size = size
        self.selected = False
        self.destinations = destinations
        self.part_number = part_number
        self.part_code = part_code


def create_hardlink(job_files):
    print("Creating hardlinks")
    for file in job_files:
        for i in range(len(file.destinations)):
            os.makedirs(file.destinations[i], exist_ok=True)
            file_source = target = os.path.join(file.root,file.filename)
            file_dest = os.path.join(file.destinations[i],file.filename)
            try:
                os.link(file_source,file_dest)
                print(f"Hardlink created: {file.filename}")
                if flag_create_copy_note_per_file:
                    f = open(f"{file.destinations[i]}\log.txt", "a+")
                    f.write(f"'{file.filename}' hardlinked from original at: '{file.root}'\n")
                    f.close()
            except FileExistsError as e:
                print(f"Hardlink already exists. Skipping: {file.filename}")

            
def log_duplicates(job_files):
    filenames = []
    duplicates = []
    for file in job_files:
        filenames.append(file.filename) # create list of filenames with indexes matched to job_files
    for idx, file in enumerate(filenames):
        if filenames.count(file) > 1:       # if filename appears in list more than once it is duplicated
            duplicates.append(job_files[idx])   # add file class with same index to list of duplicates
    
    duplicates.sort(key=lambda file: file.filename, reverse=True) # sort duplicates by filename
    
    f = open(f"duplicate_files.csv", "a+")  # write to csv
    f.write(f"'filename, path\n")
    for file in duplicates:
        f.write(f"{file.filename},{file.root}'\n")
    f.close()       
    
    
    
    #animals =["cat", "dog", "fish", "fish","cat", "parrot"]
    #for animal in animals:
     #   if animals.count(animal) > 1:
     #       print(f"{animal} is a duplicate")
       
def create_shortcut(job_files):
    print("Creating shortcuts")
    for file in job_files:
        for i in range(len(file.destinations)):
            os.makedirs(file.destinations[i], exist_ok=True)
           
            target = os.path.join(file.root,file.filename)
           
            new_name = file.filename + ".lnk"  
            path = os.path.join(file.destinations[i],new_name)
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.save()
 
 
def copy_files(job_files):
    for file in job_files:
        for i in range(len(file.destinations)):
            os.makedirs(file.destinations[i], exist_ok=True)
            try:
                dest = shutil.copy2(f"{file.root}\{file.filename}", f"{file.destinations[i]}\{file.filename}") # copy2() preserves metadata
                print(dest)
            
                if flag_create_copy_note_per_file:
                    f = open(f"{file.destinations[i]}\log.txt", "a+")
                    f.write(f"'{file.filename}' Copied from original at: '{file.root}'\n")
                    f.close()
            except Exception as e:
                print(f"Error copying {file.name}. {e}")


def find_files():
    """ Scan project folder and create a list of file class objects to be moved, copied or linked """
    
    p = re.compile(REGEX_PART_NUMBER)
    job_files = []
    
    for root, dirs, files in os.walk(project_path): # r at start of string need to prevent unicode error
        for filename in files:
            re_part_number = p.match(filename)
            if re_part_number:
                file_ext = filename.split(".")[-1].lower()  # extract file extension 
                file_size = os.path.getsize((os.path.join(root, filename))) # filesize in bytes 
                
                part_number = re_part_number.group() # extract part number from regular expression match
                part_code = part_number.split("-")[0]
                
                destinations = [] # destinations is a list in case a filetype is both a source and output filetype
                
                if (file_ext in EXTS_SOURCE_FILES) and flag_find_source_files:
                    destinations.append(os.path.join(target_source_path,part_code,part_number)) 
                
                if (file_ext in EXTS_OUTPUT_FILES) and flag_find_output_files:
                    destinations.append(os.path.join(target_source_path,part_code,part_number)) 
                
                if destinations:               
                    job_files.append(File(filename,root,file_size,destinations,part_number,part_code))
                    print(f"Found: {filename}")
                          
    return job_files
               

if __name__ == "__main__":
 
    job_files = find_files()
    
    if not job_files:
        quit()
    
    if flag_log_duplicates:
        log_duplicates(job_files)
    if flag_create_shortcut:
        create_shortcut(job_files)
    if flag_copy_files:
        copy_files(job_files)
    if flag_create_hardlink:
        create_hardlink(job_files)

    
    
    
    
