import time
import json
import requests
import os 
from pathlib import Path
from  pymongo import MongoClient
from random_object_id import generate
import random
import datetime
import json
from bson import json_util
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

now = datetime.datetime.now()

#connect mongod
client = MongoClient(os.getenv('mongo'))
db = client.app
collection = db.users

# path save name of file which store data
dirs = "/app/dataStore/file"
dirs_errors = "/app/dataStore/file_error"
# path file to save data which send to druid

api_get_infor_of_app = os.getenv('api_get_infor_of_app')

# api send notification when api identify is error
api_send_notification = os.getenv('api_send_notification')
producer = KafkaProducer(bootstrap_servers='kafka:9092')

token_collect = []
map_user = {}



def generator_file():
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    return date_time

def save_user_mongo(map_user, collection):
    for user in map_user.values(): 
        user_exist = collection.find_one({"$and":[{"user": user}, {"app_id": app_id}]})
        user_id = generate()
        if user_exist == None:
            data = {
                "user_id": user_id,
                "user": user,
                "app_id": app_id
            }
            collection.insert_one(data)

def push_data_kafka(authorization_field, collection, map_user, app_id):
    for data in datas:
        data = json.loads(data.rstrip())
        json_data = {}
        json_data['timestamp'] = datetime.datetime.utcfromtimestamp(float(data['timestamp'])).isoformat() + 'Z'
        json_data['created_at'] = float(data['timestamp'])
        json_data['user_agent'] = data['user_agent']
        json_data['url'] = data['url']
        json_data['request_method'] = data['request_method']
        json_data['request_time'] = data['request_time']
        json_data['upstream_connect_time'] = data['upstream_connect_time']
        json_data['upstream_header_time'] = data['upstream_header_time']
        json_data['upstream_response_time'] = data['upstream_response_time']
        json_data['status'] = data['status']
        json_data['size'] = data['size']
        json_data['app_id'] = app_id
        if(authorization_field in data['headers']):
            user = map_user[data['headers'][authorization_field]]
            user_id = collection.find_one({"user": user})['user_id']
            json_data['user_id'] = user_id
        else:
            json_data['user_id'] = None
        producer.send('requests', json.dumps(json_data, default=json_util.default).encode('utf-8'))
        producer.flush()

        
while True:
    paths = sorted(Path(os.path.abspath(dirs)).iterdir(), key=os.path.getmtime)
    filename=''
    if(len(paths) > 0):
        filename = os.path.abspath(paths[0])
    if(filename):
        with open(filename) as f:
            filename_data = f.readline().rstrip()
            app_key = filename_data.split("/")[-2]
        headers_processor = {'content-type': 'application/json', 'app-key': app_key}
        app = requests.get(api_get_infor_of_app, headers=headers_processor).json()
        app_id, authorization_field, api_identify = app['app_id'], app['authorization_field'], app['api_identify']
        api_identify = 'http://eae8b572e88a.ngrok.io/api/nginx/decode'
        with open(filename_data) as file_data:
            datas = file_data.read().splitlines(True)

        
        # read data nginx and group by user
        for data in datas:
            data = json.loads(data.rstrip())
            if(authorization_field in data['headers']):
                if data['headers'][authorization_field] not in token_collect:
                    token_collect.append(data['headers'][authorization_field])
    
        # get user infor from client app  
        try:  
            headers =  {'content-type': 'application/json'}        
                
            if(len(token_collect) > 0):
                for token in token_collect:
                    data = {
                        authorization_field: token
                    }
                    response = requests.post(api_identify, data=json.dumps(data), headers=headers)
                    map_user[token] = response.json()['user']

            # save user info in mongodb
            save_user_mongo(map_user, collection)
                    
            # save data and push to druid
            push_data_kafka(authorization_field, collection, map_user, app_id)
        except:
            messages = {"content": "Your api identify is not working"}
            requests.post(api_send_notification, data=json.dumps(messages), headers=headers_processor)

            filename_error = os.path.abspath(dirs_errors + '/' + generator_file() + '.txt')
            with open(filename_error, "w") as files:
                files.write(filename_data)
            if os.path.exists(filename):
                os.remove(filename)
            break
        
        #remove file data nginx 
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(filename_data):
            os.remove(filename_data)
        # except:
            
    # else:
    #     print("Not data")
    #     break


