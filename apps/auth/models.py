from datetime import datetime
import sqlalchemy as sa

metadata = sa.MetaData()


auth_table = sa.Table(
    'auths', metadata,

    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('first_name', sa.String(128), nullable=True),
    sa.Column('last_name', sa.String(128), nullable=True),
    sa.Column('email', sa.String(64), index=True, unique=True),
    sa.Column('username', sa.String(32), index=True, unique=True),
    sa.Column('password', sa.String(128), nullable=True),
    sa.Column('insert_time', sa.DateTime, default=datetime.utcnow),
    sa.Column('update_time', sa.DateTime, default=datetime.utcnow),

    sa.Column('title', sa.String(16), nullable=True),
    sa.Column('status', sa.String(32), nullable=True),

    sa.Column('address', sa.String(64), nullable=True),
)


class DBHelper():
    def __init__(self, db_pool):
        self.db_pool = db_pool
    
    def get_table(self):
        raise NotImplementedError

    def get_pk(self):
        return self.get_table().c.id

    def get_order_by(self):
        return self.get_table().c.insert_time

    def columns(self):
        return self.get_table().columns.keys()

    def serialize(self, row):
        if not row:
            raise Exception('Not found')
        
        # ser = {key: getattr(row, key, None) for key in self.columns()}
        ser = {key: row[key] for key in self.columns()}
        
        ser.pop('password', None)
        if ser['insert_time']:
            ser['insert_time'] = ser['insert_time'].isoformat()
        if ser['update_time']:
            ser['update_time'] = ser['update_time'].isoformat()
        return ser

    def serialize_insert(self, row):
        return self.serialize(row)

    async def insert(self, values, tuple=True, **kwargs):
        async with self.db_pool.acquire() as conn:
            query = self.get_table().insert().values(**values)
            if tuple:
                query = query.returning(sa.literal_column('*'))
            
            res = await conn.execute(query)
            res = await res.fetchone()
            if tuple:
                return self.serialize_insert(res)
            return res
    
    async def get(self, username, serialize=True):
        async with self.db_pool.acquire() as conn:
            query = 'SELECT * FROM auths WHERE username=%s'
            result = await conn.execute(query, (username,))
            res = await result.fetchone()
            if serialize:
                return self.serialize(res)
            return res

    async def health(self):
        async with self.db_pool.acquire() as conn:
            query = 'SELECT count(id) FROM auths WHERE false;'
            result = await conn.execute(query)
            res = await result.fetchone()
            return res

class AuthDbHelper(DBHelper):
    def get_table(self):
        return auth_table
