import os
import zlib
from base64 import *
import file_handler


def encode(pattern, path):
    if "f" in pattern:
        return "file&" + path + "&" + encode_file(path) + "&crlf"
    elif "d" in pattern:
        return 'dir' + encode_dir(path) + "&crlf"
    else:
        return ""


def encode_dir(path):
    coded_files = ""
    for dir_name in os.listdir(path):
        curr_path = path + "/" + dir_name
        if os.path.isfile(curr_path):
            coded_files = coded_files + "&" + curr_path + "&" + encode_file(curr_path)
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


def decode_file(coded_file, length):
    coded_file_int = list()
    for i in range(length):
        coded_file_int.append(int(coded_file[i]))
    coded_file_bytes = bytes(coded_file_int)
    uncompressed_coded_file = zlib.decompress(coded_file_bytes)
    return b64decode(uncompressed_coded_file)


def decode(message, root):
    split_message = str(message).split("&")
    path_and_files = dict()
    pattern = split_message[0]
    c = 1
    if "dir" in pattern:
        while True:
            if "crlf" in split_message[c]:
                break
            pa = split_message[c]
            file = split_message[c + 1]
            path_and_files[pa] = file
            c += 2
    elif "file" in pattern:
        pa = split_message[1]
        file = split_message[2]
        path_and_files[pa] = file

    for path in path_and_files:
        try:
            os.makedirs(root + "/" + "/".join(path.split('/')[0:-1]))
        except FileExistsError:
            pass
        finally:
            coded_file = path_and_files[path].split("*")
            decoded_file = decode_file(coded_file, len(coded_file))
            file_handler.write_binary(root + "/" + path, decoded_file)
