from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comm_version = Table('comm_version', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('version', String(length=64)),
    Column('desc', Text(length=400)),
    Column('date', DateTime),
    Column('status', SmallInteger, default=ColumnDefault(0)),
    Column('type', SmallInteger, default=ColumnDefault(0)),
    Column('bit', SmallInteger, default=ColumnDefault(2)),
    Column('func', Text(length=800)),
    Column('patch', Text(length=900)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comm_version'].columns['bit'].create()
    post_meta.tables['comm_version'].columns['func'].create()
    post_meta.tables['comm_version'].columns['patch'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comm_version'].columns['bit'].drop()
    post_meta.tables['comm_version'].columns['func'].drop()
    post_meta.tables['comm_version'].columns['patch'].drop()
