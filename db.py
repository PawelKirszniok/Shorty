from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Url(Base):

    __tablename__ = 'urls'

    code = Column(Integer, primary_key=True)

    url = Column(String)

    def __init__(self, code, url):
        self.code = code
        self.url = url


class DatabaseManager:

    def __init__(self):

        config_object = ConfigParser()
        config_object.read("config.ini")

        dbConfig = config_object['DATABASECONFIG']
        login_string = f"postgresql://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}/{dbConfig['dbname']}"

        engine = create_engine(login_string)
        self.session = sessionmaker(bind=engine)()

    def save_code(self, url: str, code:int ):

        record = Url(code, url)
        self.session.add(record)
        self.session.commit()
        return code

    def find_url(self, url: str) -> int:

        search = self.session.query(Url).filter_by(url=url).all()

        if len(search):
            result = search[0].code
            return True, result
        else:
            return False, None

    def find_code(self, code: int) -> (bool, int):

        search = self.session.query(Url).filter_by(code=code).all()

        if len(search):
            result = search[0].url
            return True, result
        else:
            return False, None

    def get_last_code(self):

        search = self.session.query(Url).all()
        return len(search)

