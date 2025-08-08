import torch
from PIL import Image
import torchvision.transforms as T
import os
import open_clip

# Load model
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def get_image_vector(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)

    return image_features.cpu().numpy().tolist()[0]
