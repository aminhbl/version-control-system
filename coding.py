import os
import zlib
from base64 import b64decode, b64encode
from datetime import datetime


def encode(_type, path):
    outputContent = ""
    if "f" in _type:
        file_bytes = read_binary(path)
        outputContent = "f\n" + path + "\n" + encode_file(file_bytes) + "\ncrlf"

    elif "d" in _type:
        outputContent = outputContent + "d"
        outputContent = outputContent + encode_dir(path) + "\ncrlf"

    return outputContent


def encode_dir(path):
    coded_files = ""
    for dir_name in os.listdir(path):
        if os.path.isfile(path + "/" + dir_name):
            file_bytes = read_binary(path + "/" + dir_name)
            coded_files = coded_files + "\n" + path + "/" + dir_name + "\n" + encode_file(file_bytes)
        else:
            coded_files = coded_files + encode_dir(path + "/" + dir_name)
    return str(coded_files)


def encode_file(file_bytes):
    encoded_file = b64encode(file_bytes)
    # compressed_file = zlib.compress(encoded_file, 1)

    encoded_file_str = ""
    for part in encoded_file:
        encoded_file_str = encoded_file_str + str(part) + "*"
    encoded_file_str = encoded_file_str[0:- 1]
    return encoded_file_str


def decode(messageBody, basePath, commit_message=None):
    bodyList = str(messageBody).split("\n")
    recievedFiles = {}

    if "f" in bodyList[0]:
        recievedFiles[bodyList[1]] = bodyList[2]
    elif "d" in bodyList[0]:
        counter = 1
        while True:
            if "crlf" in bodyList[counter]:
                break
            recievedFiles[bodyList[counter]] = bodyList[counter + 1]
            counter += 2

    for key in recievedFiles.keys():
        # print(basePath + "/" + "/".join(key.split('/')[0:-1]))
        try:
            os.makedirs(basePath + "/" + "/".join(key.split('/')[0:-1]))

            rawDataString = recievedFiles[key].split("*")
            for i in range(len(rawDataString)):
                rawDataString[i] = int(rawDataString[i])
            compressedData = bytes(rawDataString)
            uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(uncompressedData)
            with open(basePath + "/" + key, 'wb') as outputFile:
                outputFile.write(decodedData)

        except FileExistsError:

            rawDataString = recievedFiles[key].split("*")
            for i in range(len(rawDataString)):
                rawDataString[i] = int(rawDataString[i])

            compressedData = bytes(rawDataString)
            # uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(compressedData)

            with open(basePath + "/" + key, 'wb') as outputFile:
                outputFile.write(decodedData)

    if commit_message is not None:
        try:
            with open(basePath + "/" + "commits.txt", "a") as o:
                o.write("{}|{}\n".format(commit_message, datetime.now()))
        except FileExistsError:
            print("Commit file not found!")


def read_binary(path):
    with open(path, 'rb') as inputFile:
        try:
            return inputFile.read()
        except IOError:
            print("Could not read the file!")

def write_binary(path):
    pass