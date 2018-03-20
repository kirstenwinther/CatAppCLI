import os
from sys import argv
from folderreader import FolderReader

def main(folder_name, debug=False, skip=[], goto_reaction=None):
    FR = FolderReader(folder_name=folder_name, debug=debug)
    FR.write(skip=skip, goto_reaction=goto_reaction)


if __name__ == '__main__':
    folder_name = argv[1]
    main(folder_name)