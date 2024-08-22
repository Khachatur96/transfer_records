from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

dev_connection_string = config('DEV_DB_URL')
prod_connection_string = config('PROD_DB_URL')

dev_engine = create_engine(dev_connection_string)
prod_engine = create_engine(prod_connection_string)

DevSession = sessionmaker(bind=dev_engine)
ProdSession = sessionmaker(bind=prod_engine)
