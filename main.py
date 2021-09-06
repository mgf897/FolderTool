import os
import re
			 
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


REGEX_PART_NUMBER = r"(\d{3,4})-(\d{3,4})-(\d{2})"  # r at start of string need to prevent needing to escape backslashes
EXTS_SOURCE_FILES = ["ai","sldprt","slddrw","sldasm"]
EXTS_OUTPUT_FILES = ["pdf","step","stp"]

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
        
    for root, dirs, files in os.walk(r"C:\Users\310237398\OneDrive - Signify\DUS360CR"): # r at start of string need to prevent unicode error
        for filename in files:
            if p.match(filename):
                file_ext = filename.split(".")[-1].lower()
                file_size = os.path.getsize((os.path.join(root, filename))) # filesize in bytes 
                print(file_ext)
                
                destinations = []
                
                if file_ext in EXTS_SOURCE_FILES:
                    destinations.append("source") 
                
                elif file_ext in EXTS_OUTPUT_FILES:
                    destinations.append("outputs")
                
                else:
                    return # if no source or output file ext match
                
                job_files.append(File(filename,root,file_size,destinations))
                
                
    
    for file in job_files:
        print(file.filename, file.size, file.destinations)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    
    
    
