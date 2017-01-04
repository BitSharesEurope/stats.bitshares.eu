from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine('sqlite:///blocks.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class BTSBlock(Base):
    __tablename__ = 'bts_blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    num_txs = Column(Integer)
    num_ops = Column(Integer)

    def __init__(self, timestamp, num_txs, num_ops):
        self.timestamp = timestamp
        self.num_txs = num_txs
        self.num_ops = num_ops
        if not session.query(BTSBlock).filter_by(timestamp=timestamp).first():
            session.add(self)
            session.commit()


class TestBlock(Base):
    __tablename__ = 'test_blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    num_txs = Column(Integer)
    num_ops = Column(Integer)

    def __init__(self, timestamp, num_txs, num_ops):
        self.timestamp = timestamp
        self.num_txs = num_txs
        self.num_ops = num_ops
        if not session.query(TestBlock).filter_by(timestamp=timestamp).first():
            session.add(self)
            session.commit()


class SteemBlock(Base):
    __tablename__ = 'steem_blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    num_txs = Column(Integer)
    num_ops = Column(Integer)

    def __init__(self, timestamp, num_txs, num_ops):
        self.timestamp = timestamp
        self.num_txs = num_txs
        self.num_ops = num_ops
        if not session.query(SteemBlock).filter_by(timestamp=timestamp).first():
            session.add(self)
            session.commit()


Base.metadata.create_all(engine)
