from sqlalchemy import create_engine, desc
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import config
Base = declarative_base()
engine = create_engine(config["sql_database"])
Session = sessionmaker(bind=engine)
session = Session()


class BTSBlock(Base):
    __tablename__ = 'bts_blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    block_num = Column(Integer)
    num_txs = Column(Integer)
    num_ops = Column(Integer)

    def __init__(self, timestamp, block_num, num_txs, num_ops):
        self.block_num = block_num
        self.timestamp = timestamp
        self.num_txs = num_txs
        self.num_ops = num_ops
        if not session.query(BTSBlock).filter_by(timestamp=timestamp).first():
            session.add(self)
            session.commit()

    @staticmethod
    def recent(n=100):
        return session.query(BTSBlock).order_by(desc(BTSBlock.timestamp)).limit(n).all()


class TestBlock(Base):
    __tablename__ = 'test_blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    block_num = Column(Integer)
    num_txs = Column(Integer)
    num_ops = Column(Integer)

    def __init__(self, timestamp, block_num, num_txs, num_ops):
        self.block_num = block_num
        self.timestamp = timestamp
        self.num_txs = num_txs
        self.num_ops = num_ops
        if not session.query(TestBlock).filter_by(timestamp=timestamp).first():
            session.add(self)
            session.commit()

    @staticmethod
    def recent(n=100):
        return session.query(TestBlock).order_by(desc(TestBlock.timestamp)).limit(n).all()


class SteemBlock(Base):
    __tablename__ = 'steem_blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    block_num = Column(Integer)
    num_txs = Column(Integer)
    num_ops = Column(Integer)

    def __init__(self, timestamp, block_num, num_txs, num_ops):
        self.block_num = block_num
        self.timestamp = timestamp
        self.num_txs = num_txs
        self.num_ops = num_ops
        if not session.query(SteemBlock).filter_by(timestamp=timestamp).first():
            session.add(self)
            session.commit()

    @staticmethod
    def recent(n=100):
        return session.query(SteemBlock).order_by(desc(SteemBlock.timestamp)).limit(n).all()


Base.metadata.create_all(engine)
