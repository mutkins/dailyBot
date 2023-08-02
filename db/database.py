from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, time
import logging
from Trello import lists, boards
from sqlalchemy.types import Boolean

logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

# Declarative method
engine = create_engine("sqlite:///db/daily.db", echo=True)
Base = declarative_base()


# Describing class(table) with chat members
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(250), unique=True)
    trello_key = Column(String(250))
    trello_token = Column(String(250))
    board_id = Column(String(250))
    todolist_id = Column(String(250))
    donelist_id = Column(String(250))
    notice_time = Column(String(250))
    is_notice_on = Column(Boolean)

    def __init__(self, chat_id, trello_key, trello_token):
        self.chat_id = chat_id
        self.trello_key = trello_key
        self.trello_token = trello_token
        self.board_id = boards.get_daily_board_id(token=self.trello_token, key=self.trello_key)
        self.todolist_id = lists.get_list_id_by_name(board_id=self.board_id, token=self.trello_token, key=self.trello_key, name='To Do')
        self.donelist_id = lists.get_list_id_by_name(board_id=self.board_id, token=self.trello_token, key=self.trello_key, name='Done')
        self.is_notice_on = True
        self.notice_time = '09:00'

    def get_trello_key(self):
        return self.trello_key

    def get_trello_token(self):
        return self.trello_token

    def get_todolist_id(self):
        return self.todolist_id

    def get_donelist_id(self):
        return self.donelist_id

    def get_chat_id(self):
        return self.chat_id

    def get_notice_time(self):
        return self.notice_time

    def get_notice_state(self):
        return self.is_notice_on

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
        # session.expire_on_commit = False
        try:
            return session.query(Users).filter_by(chat_id=chat_id).one()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


def get_users():
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            return session.query(Users)
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


def switch_notice_state(chat_id, val=True):
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            user = session.query(Users).filter_by(chat_id=chat_id).one()
            user.is_notice_on = val
            session.commit()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


def set_notice_time(chat_id, n_time='09:00'):
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            user = session.query(Users).filter_by(chat_id=chat_id).one()
            user.notice_time = n_time
            session.commit()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


# def get_notice_time(chat_id):
#     with Session(engine) as session:
#         session.expire_on_commit = False
#         try:
#             user = session.query(Users).filter_by(chat_id=chat_id).one()
#             return user.get_notice_time
#         except exc.IntegrityError as e:
#             # return error if something went wrong
#             session.rollback()
#             log.error(e)
#             return e.args
#
#
# def get_notice_state(chat_id):
#     with Session(engine) as session:
#         session.expire_on_commit = False
#         try:
#             user = session.query(Users).filter_by(chat_id=chat_id).one()
#             return user.get_notice_state
#         except exc.IntegrityError as e:
#             # return error if something went wrong
#             session.rollback()
#             log.error(e)
#             return e.args