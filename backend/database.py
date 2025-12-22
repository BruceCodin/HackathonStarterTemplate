from os import environ as ENV
from psycopg2 import connect
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
import os 


def get_db_connection() -> connection:
    # return connect(
    #     dbname=os.environ["DB_NAME"],
    #     user=os.environ["DB_USER"],
    #     password=os.environ["DB_PASSWORD"],
    #     host=os.environ.get("DB_HOST"),
    #     port=os.environ.get("DB_PORT", 5432)
    # )
    ...


def create_habit(habit_name: str, description: str, target_frequency: int, frequency_unit: str) -> dict:
    query = sql.SQL("""
        INSERT INTO habit (habit_name, description, target_frequency, frequency_unit)
        VALUES (%s, %s, %s, %s)
        RETURNING habit_id, habit_name, description, target_frequency, frequency_unit;
    """)

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                query,
                (habit_name, description, target_frequency, frequency_unit)
            )
            habit = cursor.fetchone()
            conn.commit()

    return habit


def get_all_habits_with_tamagochis() -> list[dict]:
    query = sql.SQL("""
        SELECT
            h.habit_id,
            h.habit_name,
            h.description,
            h.target_frequency,
            h.frequency_unit,
            h.is_active,
            h.created_at,

            t.tamagotchi_id,
            t.habit_id,
            t.name,
            t.happiness_level,
            t.size_level,
            t.created_at
        FROM habit h
        LEFT JOIN tamagotchi t
            ON h.habit_id = t.habit_id
        ORDER BY h.habit_id;
    """)

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

    return results


def get_habit_by_id(habit_id: int) -> dict:
    query = """
        SELECT
            h.habit_id,
            h.habit_name,
            h.description,
            h.target_frequency,
            h.frequency_unit,
            h.is_active,
            h.created_at,

            t.tamagotchi_id,
            t.habit_id,
            t.name,
            t.happiness_level,
            t.size_level,
            t.created_at
        FROM habit h
        LEFT JOIN tamagotchi t
            ON h.habit_id = t.habit_id
        WHERE h.habit_id = %s;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (habit_id,))
            return cursor.fetchone()


def delete_habit(habit_id: int) -> bool:
    query = """
        UPDATE habit h
        SET is_active = FALSE
        WHERE h.habit_id = %s;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (habit_id,))
            rows_affected = cursor.rowcount
            conn.commit()

    return rows_affected > 0


def get_tamagotchi_by_id(habit_id: int) -> dict | None:
    query = """
        SELECT
            t.tamagotchi_id,
            t.habit_id,
            t.name,
            t.happiness_level,
            t.size_level,
            t.created_at
        FROM tamagotchi t
        WHERE t.habit_id = %s;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (habit_id,))
            return cursor.fetchone()
