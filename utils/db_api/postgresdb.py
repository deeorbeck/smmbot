from datetime import datetime
import asyncpg
import asyncio
from data import config



async def connect_db():
    return await asyncpg.connect(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        host=config.DB_HOST,
        port=config.DB_PORT,
    )

class User:
    def __init__(self):
        self.conn = None
        self.table_name = 'main_user'
    async def connect(self):
        self.conn = await connect_db()
        return self
    async def add_user(self, chat_id: int, name: str = None, phone: str = None, balance: float = None, lang :str = None):
        # insert user if user is not exists
        if not await self.get_user(chat_id):
            query = f"INSERT INTO {self.table_name} (chat_id, name, phone, balance, lang, created_at) VALUES ($1, $2, $3, $4, $5)"
            await self.conn.execute(query, chat_id, name, phone, balance, lang, created_at=datetime.now(timezone.utc))
            await self.conn.commit()

        elif balance and not name:
            query = f"UPDATE {self.table_name} SET balance = $1 WHERE chat_id = $2"
            await self.conn.execute(query, balance, chat_id)


    async def get_user(self, chat_id :int):
        query = f"SELECT * FROM {self.table_name} WHERE chat_id = $1"
        return await self.conn.fetchrow(query, chat_id)

    async def get_all_users(self):
        query = f"SELECT * FROM {self.table_name}"
        return await self.conn.fetch(query)


async def test():
    db = await User().connect()
    print(await db.get_user(1468429008))
    # print(await db.get_all_users())
    await db.add_user(1468429008, name="Diyorbek Ismoilov", phone="+998911091433", balance=10000, lang='uz')
    print(await db.get_user(1468429008))
asyncio.run(test())