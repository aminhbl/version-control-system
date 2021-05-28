import os


def read_binary(path):
    with open(path, 'rb') as o:
        try:
            return o.read()
        except IOError and FileNotFoundError and FileExistsError:
            print("Could not read the file!")


def write_binary(path, data):
    with open(path, 'wb') as o:
        try:
            o.write(data)
        except IOError and FileNotFoundError and FileExistsError:
            print("Could not write to file!")


def read_text(path):
    with open(path, 'r') as o:
        try:
            return o.read()
        except IOError and FileNotFoundError and FileExistsError:
            return "Commit file not found!"
