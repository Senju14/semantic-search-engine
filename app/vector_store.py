import os
from dotenv import load_dotenv
from app.embedding import get_embedding
from pinecone import Pinecone, ServerlessSpec
from app.clip_encoder import get_image_vector

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-west-2")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")

DIMENSION = 1024  # 384 (text) + 512 (image) + 128 (padding)
pc = Pinecone(api_key=PINECONE_API_KEY)

# Compatible handling for different Pinecone SDK list_indexes return types
_indexes = pc.list_indexes()
try:
	_index_names = _indexes.names()
except AttributeError:
	try:
		_index_names = [idx.name for idx in _indexes]
	except Exception:
		_index_names = _indexes

if PINECONE_INDEX_NAME not in _index_names:
	pc.create_index(
		name=PINECONE_INDEX_NAME,
		dimension=DIMENSION,
		metric="cosine",
		spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)
	)

index = pc.Index(PINECONE_INDEX_NAME)

def add_product_vector(product: dict):
    combined_text = f"{product['name']} {product['description']} {product['category']} {product.get('brand', '')} {product.get('color', '')} {product.get('size', '')} {' '.join(product.get('tags', []))}"
    text_vector = get_embedding(combined_text)

    image_path = product.get("image_path", None)
    image_vector = None
    # Chuyển image_path sang đường dẫn tuyệt đối nếu cần
    abs_path = None
    if image_path and isinstance(image_path, str):
        # Nếu image_path là /data/static/images/xxx.jpg thì chuyển sang đường dẫn thật
        if image_path.startswith('/data/static/images/'):
            abs_path = os.path.join(os.getcwd(), image_path.lstrip('/').replace('/', os.sep))
        elif os.path.exists(image_path):
            abs_path = image_path
    if abs_path and os.path.exists(abs_path):
        image_vector = get_image_vector(abs_path)

    if image_vector is not None:
        combined_vector = text_vector + image_vector + [0.0] * 128
    else:
        combined_vector = text_vector + [0.0] * (512 + 128)

    # Đảm bảo image_path luôn là string cho Pinecone
    img_path = product.get("image_path", "")
    if not img_path:
        img_path = ""
    elif not img_path.startswith('/data/static/images/') and not img_path.startswith('http'):
        if img_path.endswith('.jpg') or img_path.endswith('.png'):
            img_path = '/data/static/images/' + img_path.lstrip('/').split('/')[-1]

    index.upsert(vectors=[{
        "id": str(product['id']),
        "values": combined_vector,
        "metadata": {
            **product,
            "image_path": img_path or "",
            "text_vector_used": True,
            "image_vector_used": image_vector is not None,
        }
    }])

def search(query: str, top_k: int = 5, mode="text"):
    if mode == "text":
        vector = get_embedding(query)
        vector += [0.0] * 512  # pad for image part
        vector += [0.0] * 128  # pad for extra
    elif mode == "image":
        vector = get_image_vector(query)
        vector = [0.0] * 384 + vector  # pad for text part
        vector += [0.0] * 128  # pad for extra
    elif mode == "hybrid":
        text_vec = get_embedding(query)
        image_vec = get_image_vector(query)
        vector = text_vec + image_vec + [0.0] * 128
    else:
        raise ValueError("Mode must be one of: text, image, hybrid")

    result = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return result['matches']