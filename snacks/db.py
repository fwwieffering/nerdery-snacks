from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from snacks import properties


engine = create_engine("postgresql://{}:{}@{}:5432/{}".format(
    properties.db_user,
    properties.db_pass,
    properties.db_host,
    properties.db_name
))

Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# initialize tables
# not very pep8 but don't want to define everything in one file
from snacks.models.users import User
from snacks.models.vote import Vote

Base.metadata.create_all(engine)
