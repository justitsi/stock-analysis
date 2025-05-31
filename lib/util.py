import os

def tryMakeDir(dirPath):
    try:
        os.mkdir(dirPath)
    except FileExistsError:
        pass