import json
import os
import string
import random
from datetime import datetime
from pathlib import Path

now = datetime.now()
folder_data = "dataStore/raw/"
folder_file = "dataStore/file/"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generator_file():
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    return id_generator()+date_time

def write_data(datas, app_key):
    directory = os.path.abspath(folder_data + app_key)
    try:
        os.stat(directory)
    except: 
        os.mkdir(directory)   
    file_data = os.path.abspath(folder_data + app_key + '/' + generator_file() + '.json')
    while (len(datas) > 0):
        with open(file_data, "a") as out:
            data = datas.pop()
            json.dump(data, out)
            out.write("\n")
            if(os.stat(file_data).st_size > 1024*64):
                filename = os.path.abspath(folder_file + generator_file() + '.txt')
                with open(filename, "w") as file:
                    file.write(file_data)
                file_data = os.path.abspath(folder_data + app_key + '/' + generator_file() + '.json')
    filename = os.path.abspath(folder_file  + generator_file() + '.txt')
    with open(filename, "w") as file:
        file.write(file_data)
