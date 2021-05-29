import os
import zlib
from base64 import *
from datetime import *
import file_handler


def encode(pattern, path):
    if "f" in pattern:
        return "file\n" + path + "\n" + encode_file(path) + "\ncrlf"
    elif "d" in pattern:
        return 'dir' + encode_dir(path) + "\ncrlf"
    else:
        return ""


def encode_dir(path):
    coded_files = ""
    for dir_name in os.listdir(path):
        curr_path = path + "/" + dir_name
        if os.path.isfile(curr_path):
            coded_files = coded_files + "\n" + curr_path + "\n" + encode_file(curr_path)
        else:
            coded_files = coded_files + encode_dir(curr_path)
    return coded_files


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


def decode_file(coded_file):
    for i in range(len(coded_file)):
        coded_file[i] = int(coded_file[i])
    coded_file_bytes = bytes(coded_file)
    uncompressed_coded_file = zlib.decompress(coded_file_bytes)
    return b64decode(uncompressed_coded_file)


def decode(message, root, commit_message=None):
    split_message = str(message).split("\n")
    path_and_files = dict()

    if "file" in split_message[0]:
        path_and_files[split_message[1]] = split_message[2]
    elif "dir" in split_message[0]:
        counter = 1
        while True:
            if "crlf" in split_message[counter]:
                break
            path_and_files[split_message[counter]] = split_message[counter + 1]
            counter += 2

    for path in path_and_files:
        try:
            os.makedirs(root + "/" + "/".join(path.split('/')[0:-1]))
        except FileExistsError:
            pass
        finally:
            coded_file = path_and_files[path].split("*")
            decoded_file = decode_file(coded_file)
            file_handler.write_binary(root + "/" + path, decoded_file)

    if commit_message is not None:
        try:
            with open(root + "/" + "commits.txt", "a") as o:
                o.write("{}|{}\n".format(commit_message, datetime.now()))
        except FileExistsError:
            print("Commit file not found!")
