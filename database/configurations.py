from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create sqlite engine instance
engine = create_engine("sqlite:///database/plants.db")


