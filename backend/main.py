from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from compare import compare_images
import numpy as np
import cv2
import json
import base64

app = FastAPI()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.post("/upload_images")
async def upload_image(image: UploadFile = File(...)):
    image_content = await image.read()
    npimg = np.frombuffer(image_content, dtype=np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    similar_images = compare_images(img)
    print("Output from compare_images:", similar_images)  # Debugging output

    similar_images_base64 = []
    for data in similar_images:
        if isinstance(data, tuple) and len(data) == 2:
            try:
                similarity, img_path = data
                with open(img_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                    similar_images_base64.append([similarity, encoded_string])
            except Exception as e:
                print(f"Error processing image at {img_path}: {e}")
        else:
            print(f"Unexpected data format: {data}")

    content = json.dumps({"message": "Image received", "similar_images": similar_images_base64}, cls=NumpyEncoder)
    print(content)  # Debugging print
    return JSONResponse(status_code=200, content=content)