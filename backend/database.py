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
    #     port=os.environ.get("DB_PORT")
    # )
    ...


def create_habit(habit_name: str, habit_description: str, target_frequency: int, frequency_unit: str) -> dict:
    query = sql.SQL("""
        INSERT INTO habit (habit_name, habit_description, target_frequency, frequency_unit)
        VALUES (%s, %s, %s, %s)
        RETURNING habit_id, habit_name, habit_description, target_frequency, frequency_unit;
    """)

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                query,
                (habit_name, habit_description, target_frequency, frequency_unit)
            )
            habit = cursor.fetchone()
            conn.commit()

    return habit


def get_all_habits_with_tamagochis() -> list[dict]:
    query = sql.SQL("""
        SELECT
            h.habit_id,
            h.habit_name,
            h.habit_description,
            h.target_frequency,
            h.frequency_unit,
            h.is_active,
            h.created_at,

            t.tamagotchi_id,
            t.habit_id,
            t.tamagotchi_name,
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
            h.habit_description,
            h.target_frequency,
            h.frequency_unit,
            h.is_active,
            h.created_at,

            t.tamagotchi_id,
            t.habit_id,
            t.tamagotchi_name,
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

# Tamagotchi functions:

def get_tamagotchi_by_id(habit_id: int) -> dict | None:
    query = """
        SELECT
            t.tamagotchi_id,
            t.habit_id,
            t.tamagotchi_name,
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
        

def update_tamagotchi_happiness(tamagotchi_id: int, happiness: int) -> bool:
    query = """
        UPDATE tamagotchi t
        SET happiness_level = %s
        WHERE t.tamagotchi_id = %s;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (happiness, tamagotchi_id))
            rows_affected = cursor.rowcount
            conn.commit()

    return rows_affected > 0


def calculate_tamagotchi_state(habit_id: int) -> str | None:
    query = """
        SELECT
            t.happiness_level
        FROM tamagotchi t
        WHERE t.habit_id = %s;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (habit_id,))
            row = cursor.fetchone()

    if row is None:
        return None

    happiness = row["happiness_level"]

    if happiness >= 7:
        return "happy"
    elif happiness >= 4:
        return "neutral"
    else:
        return "sad"
    

# Completion Functions

def add_completion(habit_id: int) -> dict:
    query = """
        INSERT INTO habit_completion (
            habit_id,
            completion_date,
            completed_at
        )
        VALUES (
            %s,
            CURRENT_DATE,
            NOW()
        )
        RETURNING
            completion_id,
            habit_id,
            completion_date,
            completed_at;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (habit_id,))
            completion = cursor.fetchone()
            conn.commit()

    return completion


def get_completions_by_id(habit_id: int, days: int = 7) -> list[dict]:
    query = """
        SELECT
            hc.completion_id,
            hc.habit_id,
            hc.completion_date,
            hc.completed_at
        FROM habit_completion hc
        WHERE hc.habit_id = %s
          AND hc.completion_date >= CURRENT_DATE - (%s * INTERVAL '1 day')
        ORDER BY hc.completion_date DESC;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (habit_id, days))
            return cursor.fetchall()


def get_last_completion(habit_id: int) -> dict:
    query = """
        SELECT
            hc.completion_id,
            hc.habit_id,
            hc.completion_date,
            hc.completed_at
        FROM habit_completion hc
        WHERE hc.habit_id = %s
        ORDER BY hc.completed_at DESC
        LIMIT 1;
    """

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (habit_id,))
            return cursor.fetchone()


def has_completed_today(habit_id: int) -> bool:
    query = """
        SELECT 1
        FROM habit_completion hc
        WHERE hc.habit_id = %s
          AND hc.completion_date = CURRENT_DATE
        LIMIT 1;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (habit_id,))
            return cursor.fetchone() is not None


def check_and_apply_decay() -> int:
    """
    Applies happiness decay to tamagotchis whose habits
    have not been completed today.

    Returns the number of tamagotchis updated.
    """

    select_query = """
        SELECT
            t.tamagotchi_id,
            t.happiness_level
        FROM tamagotchi t
        LEFT JOIN habit_completion hc
            ON t.habit_id = hc.habit_id
            AND hc.completion_date = CURRENT_DATE
        WHERE hc.completion_id IS NULL;
    """

    update_query = """
        UPDATE tamagotchi t
        SET happiness_level = %s
        WHERE t.tamagotchi_id = %s;
    """

    updated_count = 0

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(select_query)
            tamagotchis = cursor.fetchall()

            for t in tamagotchis:
                new_happiness = max(t["happiness_level"] - 1, 0)

                cursor.execute(
                    update_query,
                    (new_happiness, t["tamagotchi_id"])
                )
                updated_count += 1

        conn.commit()

    return updated_count
