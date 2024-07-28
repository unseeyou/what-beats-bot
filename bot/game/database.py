import aiosqlite

from bot.errors import DatabaseNotConnectedError


class Database:
    def __init__(self, conn: aiosqlite.Connection) -> None:
        self.__conn = conn
        if not self.__conn.is_alive():
            raise DatabaseNotConnectedError

    async def add_word(self, word: str, opponent: str) -> None:
        await self.__conn.execute(
            "CREATE TABLE IF NOT EXISTS words.? (opponent TEXT PRIMARY KEY)",
            (word, opponent),
        )
        await self.__conn.execute("INSERT INTO words.? VALUES (?)", (word, opponent))
        await self.__conn.commit()

    async def check_opponent_exists(self, word: str, opponent: str) -> bool:
        cursor = await self.__conn.execute(
            "SELECT * FROM words.? WHERE opponent = ?",
            (word, opponent),
        )
        opponents = await cursor.fetchall()
        return opponent in opponents
