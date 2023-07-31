from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, time
import logging
from Trello import lists, boards

logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

# Declarative method
engine = create_engine("sqlite:///db/daily.db", echo=True)
Base = declarative_base()


# Describing class(table) with chat members
class Members(Base):
    __tablename__ = 'Members'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(250), unique=True)
    trello_key = Column(String(250))
    trello_token = Column(String(250))
    board_id = Column(String(250))
    todolist_id = Column(String(250))
    donelist_id = Column(String(250))

    def __init__(self, chat_id, trello_key, trello_token):
        self.chat_id = chat_id
        self.trello_key = trello_key
        self.trello_token = trello_token
        self.board_id = boards.get_daily_board_id(token=self.trello_token, key=self.trello_key)
        self.todolist_id = lists.get_list_id_by_name(board_id=self.board_id, token=self.trello_token, key=self.trello_key, name='To Do')
        self.donelist_id = lists.get_list_id_by_name(board_id=self.board_id, token=self.trello_token, key=self.trello_key, name='Done')

    def get_trello_key(self):
        return self.trello_key

    def get_trello_token(self):
        return self.trello_token

    def get_todolist_id(self):
        return self.todolist_id

    def get_donelist_id(self):
        return self.donelist_id

    def add_member(self):
        # Create a table. If the table exists - the class is connected to it
        Base.metadata.create_all(engine)
        #  Add new member to the table
        with Session(engine) as session:
            session.expire_on_commit = False
            try:
                session.add(self)
                session.commit()
                return None
            except exc.IntegrityError as e:
                # return error if something went wrong
                session.rollback()
                log.error(e)
                return e.args


def get_user_by_chat_id(chat_id):
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            return session.query(Members).filter_by(chat_id=chat_id).first()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


