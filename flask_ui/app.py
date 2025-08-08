from flask import Flask, render_template, request, send_from_directory
import requests
import json
import os
import glob

app = Flask(__name__)

FASTAPI_BASE_URL = "http://localhost:8000"

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    message = None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            product_data = {
                "id": request.form['id'],
                "name": request.form['name'],
                "description": request.form['description'],
                "category": request.form['category'],
                "price": int(request.form['price']),
                "brand": request.form['brand'],
                "color": request.form['color'],
                "size": request.form['size'],
                "tags": [tag.strip() for tag in request.form['tags'].split(',')]
            }
            # Xử lý upload ảnh
            add_image_file = request.files.get('add_image_file')
            if add_image_file and add_image_file.filename:
                # Đếm số file .jpg hiện có
                images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'static', 'images'))
                os.makedirs(images_dir, exist_ok=True)
                existing = glob.glob(os.path.join(images_dir, '*.jpg'))
                next_num = 1
                if existing:
                    nums = [int(os.path.splitext(os.path.basename(f))[0]) for f in existing if os.path.basename(f)[:-4].isdigit()]
                    if nums:
                        next_num = max(nums) + 1
                new_filename = f"{next_num}.jpg"
                save_path = os.path.join(images_dir, new_filename)
                add_image_file.save(save_path)
                product_data["image_path"] = f"/data/static/images/{new_filename}"
            # Nếu không có ảnh thì không gửi image_path
            try:
                response = requests.post(f"{FASTAPI_BASE_URL}/add_product/", json=product_data)
                if response.status_code == 200:
                    message = "✅ Sản phẩm đã được thêm!"
                else:
                    message = f"❌ Thêm thất bại: {response.text}"
            except Exception as e:
                message = f"❌ Lỗi kết nối FastAPI: {str(e)}"

        elif action == 'search':
            query = request.form.get('query', '')
            search_type = request.form.get('search_type', 'semantic')

            if search_type == 'image':
                image_file = request.files.get('image_file')
                if image_file and image_file.filename:
                    # Lưu file ảnh tạm
                    import tempfile
                    temp_dir = tempfile.gettempdir()
                    temp_path = os.path.join(temp_dir, image_file.filename)
                    image_file.save(temp_path)
                    # Gửi đường dẫn ảnh lên FastAPI (giả định backend nhận path local)
                    try:
                        response = requests.post(f"{FASTAPI_BASE_URL}/search/", json={"query": temp_path, "mode": "image"})
                        if response.status_code == 200:
                            results = response.json()
                        else:
                            message = f"❌ Lỗi tìm kiếm ảnh: {response.text}"
                    except Exception as e:
                        message = f"❌ Lỗi kết nối FastAPI: {str(e)}"
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                else:
                    message = "❌ Vui lòng chọn ảnh để tìm kiếm."
            else:
                endpoint = '/search/' if search_type == 'semantic' else '/hybrid_search/'
                try:
                    response = requests.post(f"{FASTAPI_BASE_URL}{endpoint}", json={"query": query})
                    if response.status_code == 200:
                        results = response.json()
                    else:
                        message = f"❌ Lỗi tìm kiếm: {response.text}"
                except Exception as e:
                    message = f"❌ Lỗi kết nối FastAPI: {str(e)}"

    return render_template('index.html', results=fix_image_paths(results), message=message)

@app.route('/load_mock_data')
def load_mock_data():
    try:
        with open("data/fashion_data.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        for product in products:
            response = requests.post(f"{FASTAPI_BASE_URL}/add_product/", json=product)
            print(f"Inserted: {product['name']} - Status: {response.status_code}")
        return "✅ Mock data loaded thành công!"
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

@app.route('/test_image')
def test_image():
    test_img_url = '/data/static/images/1.jpg'
    return render_template('test_image.html', test_img_url=test_img_url)

@app.route('/data/static/images/<path:filename>')
def serve_data_static_images(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))
    images_dir = os.path.join(project_root, 'data', 'static', 'images')
    return send_from_directory(images_dir, filename)

def fix_image_paths(results):
    if not results:
        return results
    for item in results:
        meta = item.get('metadata', {})
        img = meta.get('image_path', '')
        if img and not img.startswith('/data/static/images/') and not img.startswith('http'):
            # Nếu chỉ là tên file thì chuyển thành /data/static/images/xxx.jpg
            if img.endswith('.jpg') or img.endswith('.png'):
                meta['image_path'] = '/data/static/images/' + img
    return results

if __name__ == '__main__':
    app.run(debug=True)
