import os
import zlib
from base64 import b64decode, b64encode
from datetime import datetime


def encoder(_type, path):
    outputContent = ""
    if "f" in _type:
        outputContent = outputContent + "f\n" + path + "\n" + fileEncoder(path) + "\nfinish"

    elif "d" in _type:
        outputContent = outputContent + "d"
        outputContent = outputContent + directoryEncoder(path) + "\nfinish"

    return outputContent


def directoryEncoder(path):
    outputContent = ""
    for fileName in os.listdir(path):
        if os.path.isfile(path + "/" + fileName):
            tmpPath = path + "/" + fileName
            outputContent = outputContent + "\n" + tmpPath + "\n" + fileEncoder(tmpPath)
        else:
            outputContent = outputContent + directoryEncoder(path + "/" + fileName)
    return str(outputContent)


def fileEncoder(path):
    with open(path, 'rb') as inputFile:
        rawData = inputFile.read()
        encodedData = b64encode(rawData)
        compressedData = zlib.compress(encodedData, 1)
        rawDataString = ""

        for i in compressedData:
            rawDataString = rawDataString + str(i) + " "
        rawDataString = rawDataString[0:len(rawDataString) - 1]
        return rawDataString


def decoder(messageBody, basePath, commit_message=None):
    bodyList = str(messageBody).split("\n")
    recievedFiles = {}

    if "f" in bodyList[0]:
        recievedFiles[bodyList[1]] = bodyList[2]
    elif "d" in bodyList[0]:
        counter = 1
        while True:
            if "finish" in bodyList[counter]:
                break
            recievedFiles[bodyList[counter]] = bodyList[counter + 1]
            counter += 2

    for key in recievedFiles.keys():
        # print(basePath + "/" + "/".join(key.split('/')[0:-1]))
        try:
            os.makedirs(basePath + "/" + "/".join(key.split('/')[0:-1]))

            rawDataString = recievedFiles[key].split(" ")
            for i in range(len(rawDataString)):
                rawDataString[i] = int(rawDataString[i])
            compressedData = bytes(rawDataString)
            uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(uncompressedData)
            with open(basePath + "/" + key, 'wb') as outputFile:
                outputFile.write(decodedData)

        except FileExistsError:

            rawDataString = recievedFiles[key].split(" ")
            for i in range(len(rawDataString)):
                rawDataString[i] = int(rawDataString[i])

            compressedData = bytes(rawDataString)
            uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(uncompressedData)

            with open(basePath + "/" + key, 'wb') as outputFile:
                outputFile.write(decodedData)

    if commit_message is not None:
        try:
            with open(basePath + "/" + "commits.txt", "a") as o:
                o.write("{}|{}\n".format(commit_message, datetime.now()))
        except FileExistsError:
            print("Commit file not found!")
