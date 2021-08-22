from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)
from aiopg.sa import create_engine

meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False),
)

choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default="0", nullable=False),

    #relation of table choice -> question
    Column('question_id',
            Integer,
            ForeignKey('question.id', ondelete='CASCADE'))
)

async def pg_context(app):
    conf = app['config']['postgres']
    engine = await create_engine(
        database = conf['database'],
        user = conf['user'],
        password = conf['password'],
        host = conf['host'],
        port = conf['port'],
        minsize = conf['minsize'],
        maxsize = conf['maxsize'],
    )
    app['db'] = engine
    
    yield

    app['db'].close()
    await app['db'].wait_closed()