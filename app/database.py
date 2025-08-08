import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
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
 