from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLite db created in the same directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./plants.db"


# engine to connect to SQLite db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

# represents database session; class itself != a database session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# returns a class to create Base class; later -> inherit form this class to create each db modeles/classes
Base = declarative_base()


def init_db():
    Base.metadata.create_all(engine)


# used to create independent db session for each request and close it afterwards
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
