
import schedule
import time
import requests
import json
import re
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

path_access_log = os.getenv('path_access_log')
COLLECTION_INTERVAL = os.getenv('collection_interval')
NUMBERS_REQUEST = os.getenv('numbers_request')
url = os.getenv('collector_url')
app_key = os.getenv('app_key')

print(NUMBERS_REQUEST)

def post_data():
    global mylist
    global app_key
    global url
    print(len(mylist))
    if len(mylist) > 0:
        print(mylist)
        url = os.getenv('collector_url')
        app_key = os.getenv('app_key')
        data = {
            "data": mylist
        }
        headers = {'content-type': 'application/json', "app-key": app_key}
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            
        print("time out done")
        mylist = []

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

def findIndexString(s, chars):
    return [pos for pos, char in enumerate(s) if char == chars]

def replaceIndexString(s, array, new_char):
    for i in array:
        s = replacer(s, new_char, i)
    return s




mylist = []

schedule.every(int(COLLECTION_INTERVAL)).seconds.do(post_data)

with open(path_access_log, 'r') as f:
    f.seek(0, 2)  # seek to eof
    while True:
        line = f.readline()
        schedule.run_pending()
        if not line:
            time.sleep(0.1)  # sleep briefly before trying again
            continue
        array = findIndexString(line, '"')
        line = re.sub("'", '"', line)
        if(len(array) > 0):
            line = replaceIndexString(line, array, "'")
        line = json.loads(line)
        mylist.append(line)
        if(len(mylist) == int(NUMBERS_REQUEST)):
            post_data()
            print("done")
 
    
    process(line)
