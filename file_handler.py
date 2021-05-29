import os
import pickle


def read_binary(path):
    with open(path, 'rb') as o:
        try:
            return o.read()
        except IOError or FileNotFoundError or FileExistsError:
            print("Could not read the file!")


def write_binary(path, data):
    with open(path, 'wb') as o:
        try:
            o.write(data)
        except IOError or FileNotFoundError or FileExistsError:
            print("Could not write to file!")


def read_text(path):
    try:
        with open(path, 'r') as o:
            return o.read()
    except IOError or FileNotFoundError or FileExistsError:
        return "No commits in this repo!"


def write_text(path, data):
    try:
        with open(path, "a") as o:
            o.write(data)
    except FileExistsError:
        print("Commit file not found!")


def pickle_write(path, data):
    file = None
    try:
        file = open(path, 'wb')
        pickle.dump(data, file)
    except IOError as e:
        print(e)
    finally:
        file.close()


def pickle_read(path):
    file = None
    try:
        file = open(path, 'rb')
        data = pickle.load(file)
    except IOError:
        data = None
    finally:
        if file is not None:
            file.close()
    return data
