import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session


DSN = "postgresql://postgres:1@localhost:5432/vk_db"
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()
# схема БД
metadata = MetaData()
Base = declarative_base()

class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)



# добавление записи в бд


    def add_in_db(self, profile_id,worksheet_id):
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            to_bd = Viewed(profile_id=1, worksheet_id=1)
            session.add(to_bd)
            session.commit()
# извлечение записей из БД
    def extract_from_db(self):
        with Session(engine) as session:
            from_bd = session.query(Viewed).filter(Viewed.profile_id==1).all()
            for item in from_bd:
                print(item.worksheet_id)
        return Viewed.profile_id, item.worksheet_id
