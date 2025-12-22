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
        RETURNING habit_id, name, description, target_frequency, frequency_unit;
    """)

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                query,
                (name, description, target_frequency, frequency_unit)
            )
            habit = cursor.fetchone()
            conn.commit()

    return habit

