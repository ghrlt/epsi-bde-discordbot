import sqlite3

import env
import utils


#~ ~ ~/ Initialize database
DATABASE_CONNECTION = sqlite3.connect(utils.getAbsolutePath('database.db'))
DATABASE_CURSOR = DATABASE_CONNECTION.cursor()

def setup():
    DATABASE_CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS conf (
            guild_id INTEGER NOT NULL,
            key TEXT NOT NULL,
            value TEXT
        )
    ''')
    DATABASE_CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS creds (
            user_id INTEGER NOT NULL,
            app TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT
        )
    ''')

    DATABASE_CONNECTION.commit()


#~ ~ ~/ Helper functions

def obtainConfiguration(guildId, key, ignoreError=False):
    r = DATABASE_CURSOR.execute(
        "SELECT value FROM conf WHERE guild_id = ? AND key = ?",
        (guildId, key)
    ).fetchone()

    if r is None:
        if not ignoreError:
            env.logger.exception("No configuration found for guild %i and key %s", guildId, key)
        return None

    result = r[0]
    if result.isdigit():
        result = int(result)

    return result

def setConfiguration(guildId, key, value):
    if obtainConfiguration(guildId, key, ignoreError=True) is None:
        DATABASE_CURSOR.execute(
            "INSERT INTO conf (guild_id, key, value) VALUES (?, ?, ?)",
            (guildId, key, value)
        )
    else:
        env.logger.debug("Overwriting configuration for guild %i and key %s", guildId, key)
        DATABASE_CURSOR.execute(
            "UPDATE conf SET value = ? WHERE guild_id = ? AND key = ?",
            (value, guildId, key)
        )
    
    DATABASE_CONNECTION.commit()

def deleteConfiguration(guildId, key):
    DATABASE_CURSOR.execute(
        "DELETE FROM conf WHERE guild_id = ? AND key = ?",
        (guildId, key)
    )
    DATABASE_CONNECTION.commit()


def saveCredentials(userId: int, app: str, username: str, password: str|None):
    if obtainCredentials(userId, app) is None:
        DATABASE_CURSOR.execute(
            "INSERT INTO creds (user_id, app, username, password) VALUES (?, ?, ?, ?)",
            (userId, app, username, password)
        )
    else:
        env.logger.debug("Overwriting credentials for user %i and app %s", userId, app)
        DATABASE_CURSOR.execute(
            "UPDATE creds SET username = ?, password = ? WHERE user_id = ? AND app = ?",
            (username, password, userId, app)
        )

    DATABASE_CONNECTION.commit()

def obtainCredentials(userId: int, app: str):
    r = DATABASE_CURSOR.execute(
        "SELECT username, password FROM creds WHERE user_id = ? AND app = ?",
        (userId, app)
    ).fetchone()

    if r is None:
        return None

    return r

def deleteCredentials(userId: int, app: str):
    DATABASE_CURSOR.execute(
        "DELETE FROM creds WHERE user_id = ? AND app = ?",
        (userId, app)
    )
    DATABASE_CONNECTION.commit()
