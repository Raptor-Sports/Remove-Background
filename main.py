from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from rembg import remove
from PIL import Image
import base64
import uvicorn

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://raptorsports.co",
    "https://raptor-web.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

            byteArray = output_image_bytes.getvalue()
            base64String = base64.b64encode(byteArray).decode('utf-8')

            return JSONResponse(status_code=200, content={"image": base64String})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=4000)