from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///test.db", echo=False)

engine = create_engine("postgresql+psycopg2://postgres:123abc@localhost:5432/postgres")
DBSession = sessionmaker(bind=engine)
session = DBSession()
