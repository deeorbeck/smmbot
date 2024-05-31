import sqlite3
import os




con = sqlite3.connect('database.db')
class Surveyers:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'surveyers'
    async def create(self):
        self.cur.execute(
                f"""
                create table if not exists {self.name}(
                    chat_id int
                    
                )
                """)

        self.con.commit()
        self.con.close()

    async def adduser(self, chat_id):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    {chat_id}
                )
            """
            )

            self.con.commit()
            self.con.close()

    async def search(self, chat_id=None):
        if chat_id:
            response = self.cur.execute(
                f"""
                    select * from {self.name} where chat_id='{chat_id}'
                """).fetchall()
            if response:
                return response[0]
            return False
    async def delete(self,  chat_id):
        self.cur.execute(f"""
         delete from {self.name} where chat_id=?
        """, (str(chat_id), ))
        self.con.commit()
        self.con.close()

class UsersTable:
    def __init__(self, name="database"):
        self.con = con
        self.cur = self.con.cursor()
        self.name = 'users'
    async def create(self):
        self.cur.execute(
                f"""
                create table if not exists {self.name}(
                    chat_id int,
                    lang text,
                    access int,
                    reffer_by int
                )
                """)

        self.con.commit()




    async def delete(self,  chat_id):
        self.cur.execute(f"""
         delete from {self.name} where chat_id=?
        """, (str(chat_id), ))
        self.con.commit()


    async def adduser(self, chat_id, lang=None, access=None, reffer_by=None):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    ?, ?, ?, ?
                )
            """, (
                chat_id,
                lang,
                access,
                reffer_by
                )
            )

            self.con.commit()


        elif lang:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  lang=? where chat_id=?  
                """, (lang, chat_id))
            self.con.commit()

        elif access is not None:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  access=? where chat_id=?  
                """, (access, chat_id))
            self.con.commit()


    async def search(self, chat_id=None, all=None, reffer_by=None, count=None):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {self.name} where chat_id='{chat_id}'
            """).fetchall()
            if response:
                return response[0]
            return False
        elif reffer_by:
            response = self.cur.execute(
                f"""
                       select count(*) from {self.name} where reffer_by={reffer_by}
                   """).fetchone()
            return response
        elif count:
            response = self.cur.execute(
                f"""
                                   select count(*) from {self.name}
                               """).fetchone()
            return response[0]

        else:
            return None

class ExtraTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'extrausers'
    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                chat_id int,
                name text,
                last_usage date,
                usage_count int
                )
                    """)

        self.con.commit()
        self.con.close()



    async def delete(self,  chat_id):
        self.cur.execute(f"""
         delete from {self.name} where chat_id=?
        """, (str(chat_id), ))
        self.con.commit()
        self.con.close()

    async def adduser(self, chat_id, name=None, last_usage=None, usage_count=None):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    ?, ?, ?, ?
                )
            """, (
                chat_id,
                name,
                last_usage,
                usage_count
                )
            )

            self.con.commit()
            self.con.close()

        elif last_usage:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  last_usage=? where chat_id=?  
                """, (last_usage, chat_id))
            self.con.commit()
            self.con.close()
        elif usage_count:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  usage_count=? where chat_id=?  
                """, (usage_count, chat_id))
            self.con.commit()
            self.con.close()

    async def search(self, chat_id=None, all=None):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {self.name} where chat_id='{chat_id}'
            """).fetchall()
            if response:
                return response[0]
            return False
        return None

class TariffsTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'tariffs'

    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                title text,
                days text,
                price text
                )
                    """)

        self.con.commit()
        self.con.close()
    async def delete(self,  days):
        self.cur.execute(f"""
        delete from {self.name} where days={days}
        """)
        self.con.commit()
        self.con.close()

    async def add(self, title, days, price):
        if not await self.search(days):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    '{title}','{days}', '{price}'
                )
            """)
            self.con.commit()
            self.con.close()
    async def search(self, days=None, title=None, all=False):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif title:
            response = self.cur.execute(
                f"""
                select * from {self.name} where title='{title}'
            """).fetchall()
            if response:
                return response[0]
            return False
        elif days:
            response = self.cur.execute(
                f"""
                select * from {self.name} where days={days}
            """).fetchall()
            if response:
                return response[0]
            return False
        return []

class TokensTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'tokens'

    async def create(self):
        self.cur.execute(
            f"""
                   create table if not exists {self.name} (
                   token text,
                   days text
                   )
                       """)
        self.con.commit()
        self.con.close()
    async def delete(self,  token):
        self.cur.execute(f"""
        delete from {self.name} where token='{token}'
        """)
        self.con.commit()
        self.con.close()

    async def search(self, token=None, days=None, all=False):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif token:
            response = self.cur.execute(
                f"""
                select * from {self.name} where token='{token}'
            """).fetchall()
            if response:
                return response[0]
            return False
        elif days:
            response = self.cur.execute(
                f"""
                select * from {self.name} where days='{days}'
            """).fetchall()

            return response
        return []
    async def add(self, token, days):
        if not await self.search(token=token):
            self.cur.execute(
                f"""
                insert into tokens values(
                    '{token}','{days}'
                )
            """)

            self.con.commit()
            self.con.close()


class ChannelsTable:
    def __init__(self, name="channels"):
        self.name = name
        self.con = con
        self.cur = self.con.cursor()
        self.users = 'users'

    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                chat_id text
                )
                    """)

        self.con.commit()

    async def addchannel(self, chat_id):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    '{chat_id}'
                )
            """)

            self.con.commit()

    async def search(self, chat_id=None, all=False):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {self.name} where chat_id={chat_id}
            """).fetchall()
            if response:
                return response[0]
            return False
        else:
            return None

    async def delete(self, chat_id):
        self.cur.execute(f"""
        delete from {self.name} where chat_id='{chat_id}'
        """)
        self.con.commit()

async def setup_tables():
    await UsersTable().create()
    await ExtraTable().create()
    await TariffsTable().create()
    await TokensTable().create()
    await ChannelsTable().create()
    await Surveyers().create()
