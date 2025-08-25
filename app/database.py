import os
from dotenv import load_dotenv

# Support both psycopg2 (v2) and psycopg (v3) so the app can run across environments
try:
	import psycopg2 as _pg_driver
except Exception:
	try:
		import psycopg as _pg_driver
	except Exception as _e:
		raise ImportError(
			"No PostgreSQL driver found. Please install 'psycopg2-binary' or 'psycopg'."
		) from _e

load_dotenv()

def get_connection():
	return _pg_driver.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "semantic_search"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "your_password"),
        port=os.getenv("POSTGRES_PORT", 5432),
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER,
            brand TEXT,
            color TEXT,
            size TEXT,
            tags TEXT,
            image_path TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Tự động tạo bảng khi import
init_db()
 