import os

"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

class File:
    def __init__(self, filename, root, size):
        self.filename = filename
        self.root = root
        self.size = size
        self.selected = False

def main():
    """ Main entry point of the app """
    myFiles = []
    for root, dirs, files in os.walk("/Users/matthewflynn/Documents/FolderTool/Sample files/"):
        for filename in files:
            #print(os.path.join(root, file))
            
            filesize = os.path.getsize((os.path.join(root, filename))) # filesize in bytes
            #print(filename, filesize)
            myFiles.append(File(filename,root,filesize))

    for file in myFiles:
        print(file.filename, file.size)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()