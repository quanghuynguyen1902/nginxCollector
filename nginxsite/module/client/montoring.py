from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
from sqlalchemy.orm import sessionmaker
import datetime 
from pymongo import MongoClient
from datetime import datetime
import calendar, time

client = MongoClient('mongodb://localhost:27017/')
db = client.app
collection = db.users
Session = sessionmaker()
engine = create_engine('druid+http://localhost:8082/druid/v2/sql/')
requestss = Table('request', MetaData(bind=engine), autoload=True)
# requestss = []
# engine = []
Session.configure(bind=engine)
session = Session()

def get_data(app_id, page=1):
    per_page = 10
    page = int(page)
    data = []
    counts = 0
    try:
        counts = session.query(requestss).count()
        querys = session.query(requestss).order_by(requestss.c.__time).limit(per_page).offset((page-1) * per_page)
        results = [{**row} for row in querys]
        for result in results:
            user = None
            if result['user_id']:
                user = collection.find_one({"$and": [{"app_id": app_id}, {"user_id": result['user_id']}]})
            del result['app_id']
            if(user):
                result['user'] = user['user']
            else:
                result['user'] = user
            data.append(result)
    except:
        print("Not found offset")
    return data, counts


def filter_data(app_id, request_method, user_id=None, url=None, time_from=None, page=1):
    data = []
    counts = 0
    per_page=10
    
    querys = session.query(requestss).filter(requestss.c.request_method==request_method)
    if(user_id):
        querys = querys.filter(requestss.c.user_id==user_id)
    if(url):
        querys = querys.filter(requestss.c.url==url)
    if(time_from):
        convert_time_format = time_from + ' 00:00:00'
        time_from_miliseconds = calendar.timegm(time.strptime(convert_time_format, '%Y-%m-%d %H:%M:%S'))
        querys = querys.filter(requestss.c.created_at >= int(time_from_miliseconds))
    
    counts = querys.count()
    querys = querys.limit(per_page).offset((page-1)*per_page)
    results = [{**row} for row in querys]
    for result in results:
        user = None
        if result['user_id']:
            user = collection.find_one({"$and": [{"app_id": app_id}, {"user_id": result['user_id']}]})
        del result['app_id']
        if(user):
            result['user'] = user['user']
        else:
            result['user'] = user
        data.append(result)
    # except:
    #     print("Not found page")
    return data, counts


def get_users(app_id):
    users_raw = collection.find({"app_id": app_id})
    users = []
    keys = []
    for user in users_raw:
        user_dict = {}
        keys = list(user['user'].keys())
        user_dict['user_id'] = user['user_id']
        for key in keys:  
            user_dict[key] = user['user'][key]
        users.append(user_dict)
    return keys, users

def request_of_user(app_id, user_id):
    methods = []
    get_method_count = 0
    post_method_count = 0
    put_method_count = 0
    delete_method_count = 0
    options_method_count = 0
    total = 0
    try: 
        querys = session.query(requestss).filter(requestss.c.app_id==app_id).filter(requestss.c.user_id==user_id)
        total = querys.count()
    except:
        print("Not found user_id")
    try:
        get_method_count = querys.filter(requestss.c.request_method=="GET").count()
    except:
        print("Not found get method")
    try:
        post_method_count = querys.filter(requestss.c.request_method=="POST").count()
    except: 
        print("Not found post method")
    try:
        put_method_count = querys.filter(requestss.c.request_method=="PUT").count()
    except: 
        print("Not found put method")
    try:
        delete_method_count = querys.filter(requestss.c.request_method=="DELETE").count()
    except:
        print("Not found delete method")
    methods.append({"name": "GET", "count": get_method_count})
    methods.append({"name": "POST", "count": post_method_count})
    methods.append({"name": "PUT", "count": put_method_count})
    methods.append({"name": "DELETE", "count": delete_method_count})
    
    return total, methods
    

def get_user_detail(app_id, user_id, page=1):
    data = []
    total = 0
    per_page = 10
    page = int(page)
    try: 
        querys = session.query(requestss).filter(requestss.c.app_id==app_id).filter(requestss.c.user_id==user_id)
        total = querys.count()
        querys = querys.order_by(requestss.c.__time).limit(per_page).offset((page-1) * per_page)
        user = collection.find_one({"$and": [{"app_id": app_id}, {"user_id": user_id}]})
        results = [{**row} for row in querys]
        for result in results:
            del result['app_id']
            if(user):
                result['user'] = user['user']
            else:
                result['user'] = user
            data.append(result)
    except:
        print("Not found user_id")


    return total, data
    
    