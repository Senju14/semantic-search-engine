import json
import requests
import os

with open("data/mock_fashion.json") as f:
    products = json.load(f)

for product in products:
    if product.get("image_path"):
        # Nếu chỉ là tên file hoặc không bắt đầu bằng /data/static/images/ thì chuẩn hóa lại
        img = product["image_path"]
        if not img.startswith('/data/static/images/') and not img.startswith('http'):
            if img.endswith('.jpg') or img.endswith('.png'):
                img = '/data/static/images/' + img.lstrip('/').split('/')[-1]
        # Kiểm tra file tồn tại
        image_abs_path = os.path.join(os.getcwd(), img.lstrip('/'))
        if not os.path.exists(image_abs_path):
            print(f"⚠️ Image not found: {image_abs_path}")
            continue
        product["image_path"] = img

    try:
        res = requests.post("http://localhost:8000/add_product/", json=product)
        res.raise_for_status()  # Ném lỗi nếu HTTP status != 200
        print(res.json())       # In kết quả nếu là JSON hợp lệ
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"Response content: {res.text}")
    except requests.exceptions.JSONDecodeError:
        print("❌ Response is not JSON. Raw content:")
        print(res.text)
