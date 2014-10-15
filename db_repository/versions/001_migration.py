from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
app_version = Table('app_version', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('version', String(length=64)),
    Column('desc', Text(length=400)),
    Column('date', DateTime),
    Column('status', SmallInteger, default=ColumnDefault(1)),
    Column('type', SmallInteger, default=ColumnDefault(0)),
    Column('id_comm_version', Integer),
)

comm_version = Table('comm_version', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('version', String(length=64)),
    Column('desc', Text(length=400)),
    Column('date', DateTime),
    Column('status', SmallInteger, default=ColumnDefault(0)),
    Column('type', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['app_version'].create()
    post_meta.tables['comm_version'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['app_version'].drop()
    post_meta.tables['comm_version'].drop()
