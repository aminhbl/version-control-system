import os
import zlib
from base64 import *
from datetime import *
import file_handler


def encode(_type, path):
    outputContent = ""
    if "f" in _type:
        outputContent = outputContent + "file\n" + path + "\n" + encode_file(path) + "\ncrlf"

    elif "d" in _type:
        outputContent = 'dir' + encode_dir(path) + "\ncrlf"

    return outputContent


def encode_dir(path):
    outputContent = ""
    for fileName in os.listdir(path):
        if os.path.isfile(path + "/" + fileName):
            tmpPath = path + "/" + fileName
            outputContent = outputContent + "\n" + tmpPath + "\n" + encode_file(tmpPath)
        else:
            outputContent = outputContent + encode_dir(path + "/" + fileName)
    return str(outputContent)


def encode_file(path):
    with open(path, 'rb') as o:
        file_bytes = o.read()
        encoded_file = b64encode(file_bytes)
        comp_file = zlib.compress(encoded_file, 1)
        encoded_file_str = ""
        for part in comp_file:
            encoded_file_str = encoded_file_str + str(part) + "*"
        encoded_file_str = encoded_file_str[0:- 1]
        return encoded_file_str


def decode(message, basePath, commit_message=None):
    bodyList = str(message).split("\n")
    path_and_files = dict()

    if "file" in bodyList[0]:
        path_and_files[bodyList[1]] = bodyList[2]
    elif "dir" in bodyList[0]:
        counter = 1
        while True:
            if "crlf" in bodyList[counter]:
                break
            path_and_files[bodyList[counter]] = bodyList[counter + 1]
            counter += 2

    for path in path_and_files.keys():
        try:
            os.makedirs(basePath + "/" + "/".join(path.split('/')[0:-1]))
        except FileExistsError:
            pass
        finally:
            rawDataString = path_and_files[path].split("*")
            for i in range(len(rawDataString)):
                rawDataString[i] = int(rawDataString[i])
            compressedData = bytes(rawDataString)
            uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(uncompressedData)
            file_handler.write_binary(basePath + "/" + path, decodedData)

    if commit_message is not None:
        try:
            with open(basePath + "/" + "commits.txt", "a") as o:
                o.write("{}|{}\n".format(commit_message, datetime.now()))
        except FileExistsError:
            print("Commit file not found!")
