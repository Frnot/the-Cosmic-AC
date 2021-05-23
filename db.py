import os
import aiosqlite
import asyncio
import sys
import logging
log = logging.getLogger(__name__)



db_filename = 'data.db'
init_tables = {
    "snitch":"CREATE TABLE IF NOT EXISTS 'snitch' (guild_id INT PRIMARY KEY, hook_channel_id INT);",
    "blacklist":"CREATE TABLE IF NOT EXISTS 'blacklist' (guild_id INT PRIMARY KEY, blacklist_set TEXT);",
    "voting":"CREATE TABLE IF NOT EXISTS 'voting' (guild_id INT PRIMARY KEY, voting_role_id INT);",
}


### "Constructor"
async def load():
    global conn

    log.info("Initializing database")
    if os.path.exists(db_filename):
        conn = await connect()
        await reload_tables(conn)
    else:
        log.info("Creating new database")
        conn = await new_db()
    log.info("database loaded")

def exit():
    log.info("Closing database connection.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(conn.close())



async def new_db():
    conn = await connect()

    log.info("Setting up database tables")
    for key, value in init_tables.items():
        log.debug(f"Creating database table {key}")
        await conn.execute(value)

    await conn.commit()
    return conn



async def connect():
    try:
        conn = await aiosqlite.connect(db_filename)
    except Exception as e:
        print(e)
        sys.exit("database error")
    return conn



async def reload_tables(conn):
    log.info("Updating database tables")
    for key, value in init_tables.items():
        log.debug(f"Updating database table {key}")
        await conn.execute(value)
    
    await conn.commit()



async def select(row, table, symbol, value):
    sql = f"SELECT {row} FROM {table} WHERE {symbol}={value}"
    log.debug(f"Sending query: '{sql}' to database")

    try:
        cursor = await conn.execute(sql)
    except Exception as e:
        log.error(f"SQL query failed: {e}")
        return None

    result = await cursor.fetchone()
    log.debug(f"Query result: {result}")

    if result is None:
        return result
    else:
        return result[0]



# TODO: make the (?, ?) parameter variable length based on data rows
async def insert(table, data):
    sql = f"INSERT INTO {table} ({', '.join(str(row[0]) for row in data)}) VALUES (?, ?)"
    payload = [row[1] for row in data]

    log.debug(f"Sending query: '{sql}, ({', '.join(str(word) for word in payload)})' to database")
    try:
        await conn.execute(sql, payload)
        await conn.commit()
    except Exception as e:
        log.error(f"SQL query failed: {e}")



# TODO: make the (?, ?) parameter variable length based on data rows
async def update(table, data):
    sql = f"UPDATE {table} SET ({', '.join(str(row[0]) for row in data)}) = (?, ?)"
    payload = [row[1] for row in data]

    log.debug(f"Sending query: '{sql}, ({', '.join(str(word) for word in payload)})' to database")
    try:
        await conn.execute(sql, payload)
        await conn.commit()
    except Exception as e:
        log.error(f"SQL query failed: {e}")



async def delete(table, data):
    sql = f"DELETE FROM {table} WHERE {data[0]} = {data[1]}"
    log.debug(f"Sending query: '{sql}' to database")
    try:
        await conn.execute(sql)
        await conn.commit()
    except Exception as e:
        log.error(f"SQL query failed: {e}")
