from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from rembg import remove
from PIL import Image

app = FastAPI()


@app.post('/removeBackground')
async def remove_background(image: UploadFile):
    try:
        if not image:
            raise HTTPException(
                status_code=400, detail='No image file uploaded')

        with BytesIO() as temp_image:
            temp_image.write(await image.read())
            temp_image.seek(0)

            input_image = Image.open(temp_image)
            output_image = remove(input_image)

            output_image_bytes = BytesIO()
            output_image.save(output_image_bytes, format="PNG")
            output_image_bytes.seek(0)

            return StreamingResponse(output_image_bytes, media_type='image/png')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
