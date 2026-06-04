from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from realesrgan import RealESRGAN
import torch
import uuid
import os

app = FastAPI()

# Create folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Load model
device = torch.device("cpu")  # Free Render compatible
model = RealESRGAN(device, scale=4)
model.load_weights("weights/realesr-general-x4v3.pth")

MAX_SIZE = 1024


@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):

    # Save upload
    input_path = f"uploads/{uuid.uuid4()}.png"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Open image
    image = Image.open(input_path).convert("RGB")

    # Original size save
    original_width, original_height = image.size

    # Resize for processing if larger than 1024
    process_image = image.copy()

    if max(process_image.size) > MAX_SIZE:
        process_image.thumbnail((MAX_SIZE, MAX_SIZE))

    # Enhance
    sr_image = model.predict(process_image)

    # Resize back to original size
    sr_image = sr_image.resize(
        (original_width, original_height),
        Image.LANCZOS
    )

    # Save output
    output_path = f"outputs/{uuid.uuid4()}.png"
    sr_image.save(output_path)

    return FileResponse(output_path)
