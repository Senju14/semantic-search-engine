# app/main.py
from fastapi import FastAPI, Request
from app.schemas import Product, SearchQuery
from app.vector_store import add_product_vector, search as vector_search
from app.repository import save_product_to_db, keyword_search

app = FastAPI()

@app.post("/add_product/")
def add_product(product: Product):
    product_dict = product.dict()
    save_product_to_db(product_dict)
    add_product_vector(product_dict)
    return {"message": "Product added", "product_id": product.id}

@app.post("/search/")
async def search_products(request: Request):
    data = await request.json()
    query = data.get("query", "")
    mode = data.get("mode", "text")
    results = vector_search(query, mode=mode)
    return [
        {
            "id": r['id'],
            "score": r['score'],
            "metadata": r['metadata']
        }
        for r in results
    ]

@app.post("/hybrid_search/")
def hybrid_search(query: SearchQuery):
    vector_results = vector_search(query.query)
    keyword_results = keyword_search(query.query)

    merged = {}
    for item in vector_results:
        merged[item["id"]] = {
            "id": item["id"],
            "metadata": item["metadata"],
            "vector_score": item["score"],
            "keyword_score": 0,
        }

    for item in keyword_results:
        if item["id"] in merged:
            merged[item["id"]]["keyword_score"] = item["score"]
        else:
            merged[item["id"]] = {
                "id": item["id"],
                "metadata": {
                    "name": item["name"],
                    "description": item["description"],
                    "brand": None,
                    "price": None,
                    "category": None,
                },
                "vector_score": 0,
                "keyword_score": item["score"],
            }

    for v in merged.values():
        v["hybrid_score"] = v["vector_score"] + v["keyword_score"]

    sorted_results = sorted(merged.values(), key=lambda x: x["hybrid_score"], reverse=True)

    return sorted_results[:5]
