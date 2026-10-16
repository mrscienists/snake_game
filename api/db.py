import sqlite3
from contextlib import closing

DB_PATH = "game.db"

def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    """Создаёт таблицу, если её ещё нет."""
    with closing(_connect()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                score INTEGER NOT NULL
            )
            """
        )

def save_score(player: str, score: int) -> None:
    """Сохраняет результат игрока."""
    with closing(_connect()) as conn, conn:
        conn.execute(
            "INSERT INTO scores (player, score) VALUES (?, ?)",
            (player, score),
        )

def delete_score(player: str) -> int:
    """Удаляет все записи игрока по нику. Возвращает число удалённых строк."""
    with closing(_connect()) as conn, conn:
        cursor = conn.execute("DELETE FROM scores WHERE player = ?", (player,))
        return cursor.rowcount

def get_all_scores() -> list[dict]:
    """Возвращает все записи, от большего счёта к меньшему."""
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT player, score FROM scores ORDER BY score DESC"
        ).fetchall()
    return [{"player": player, "score": score} for player, score in rows]
