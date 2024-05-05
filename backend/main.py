from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from compare import compare_images
import numpy as np
import cv2
import json

app = FastAPI()

class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for NumPy data types to ensure they can be JSON serialized."""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert NumPy arrays to list
        return json.JSONEncoder.default(self, obj)

@app.post("/upload_images")
async def upload_image(image: UploadFile = File(...)):
    image_content = await image.read()
    # Convert the raw image bytes into a NumPy array
    npimg = np.frombuffer(image_content, dtype=np.uint8)
    # Decode the image as a color image
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # Now pass this decoded image to your comparison function
    similar_images = compare_images(img)
    # Create the JSON response using the custom encoder for NumPy arrays
    content = json.dumps({"message": "Image received", "similar_images": similar_images}, cls=NumpyEncoder)
    return JSONResponse(status_code=200, content=content)