import json

# Đọc dữ liệu từ file
with open("mock_fashion.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Thêm trường image_path cho mỗi item
for item in data:
    item["image_path"] = f"/images/{item['id']}.jpg"

# Ghi đè lại file với field mới
with open("mock_fashion.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Đã thêm field 'image_path' vào mock_fashion.json.")
