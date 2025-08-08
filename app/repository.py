from app.database import get_connection
import psycopg2

def save_product_to_db(product: dict):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO products (id, name, description, category, price, brand, color, size, tags, image_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """

    cur.execute(query, (
        product["id"],
        product["name"],
        product["description"],
        product["category"],
        product["price"],
        product["brand"],
        product["color"],
        product["size"],
        product["tags"],
        product.get("image_path", None),
    ))

    conn.commit()
    cur.close()
    conn.close()


def keyword_search(query: str, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, ts_rank_cd(to_tsvector('english', name || ' ' || description), plainto_tsquery(%s)) AS rank
        FROM products
        WHERE to_tsvector('english', name || ' ' || description) @@ plainto_tsquery(%s)
        ORDER BY rank DESC
        LIMIT %s;
    """, (query, query, limit))
    results = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "name": r[1], "description": r[2], "score": r[3]} for r in results]
