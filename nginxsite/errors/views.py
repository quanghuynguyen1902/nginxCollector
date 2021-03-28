from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

# Create your views here.
engine = create_engine('druid+http://localhost:8082/druid/v2/sql/')
user = Table('request', MetaData(bind=engine), autoload=True)
stmt = select('*', from_obj=user).order_by(desc(user.columns.__time))
connection = engine.connect()
