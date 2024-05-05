from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from compare import compare_images  # Asegúrate de que esta importación es correcta

app = FastAPI()

@app.post("/upload_images")
async def upload_image(image: UploadFile = File(...)):
    image_content = await image.read()
    similar_images = compare_images(image_content)
    return JSONResponse(status_code=200, content={"message": "Image received", "similar_images": similar_images})