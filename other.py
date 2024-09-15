import psycopg2

from psycopg2.extras import RealDictCursor

while True:
    conn = None
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port=5432,
            database="testing",
            cursor_factory=RealDictCursor,
        )
        print("Database connection successfully!")
        break
    except Exception as err:
        print(err)
    finally:
        if conn is not None:
            conn.close()
