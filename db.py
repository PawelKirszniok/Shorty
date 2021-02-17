from configparser import ConfigParser
import psycopg2
from sqlalchemy import create_engine
import urllib.parse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Url(Base):

    __tablename__ = 'urls'

    code = Column(String, primary_key=True)

    url = Column(String)

    def __init__(self, code, url):
        self.code = code
        self.url = url



def generate_code(url):
    config_object = ConfigParser()
    config_object.read("config.ini")

    siteInfo = config_object["SITEINFO"]
    dbConfig = config_object['DATABASECONFIG']
    lastcode = siteInfo['lastcode']


    code = int(lastcode) + 1
    siteInfo['lastcode'] = str(code)
    config_object["SITEINFO"] = siteInfo

    with open('config.ini', 'w') as conf:
        config_object.write(conf)

    login_string = f"postgresql://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}/{dbConfig['dbname']}"

    engine = create_engine(login_string)
    session = sessionmaker(bind=engine)()

    record = Url(code, url)
    session.add(record)
    session.commit()
    return code


def find_code(code):
    config_object = ConfigParser()
    config_object.read("config.ini")

    dbConfig = config_object['DATABASECONFIG']
    login_string = f"postgresql://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}/{dbConfig['dbname']}"

    engine = create_engine(login_string)
    session = sessionmaker(bind=engine)()

    search = session.query(Url).filter_by(code=code).all()

    if len(search):
        result = search[0].url
        return True, result
    else:
        return False, None

