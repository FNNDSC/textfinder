from fastapi import FastAPI, UploadFile, File, HTTPException
from dicom_utils import dicom_to_uint8
import easyocr
import numpy as np
import cv2
import pydicom
import io

app = FastAPI()

# Initialize once per worker
reader = easyocr.Reader(
    ["en"],
    gpu=True,
    model_storage_directory="/models",
    download_enabled=False  # CRITICAL
)


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    # DICOMs usually have application/dicom or octet-stream
    if file.content_type not in {
        "application/dicom",
        "application/octet-stream"
    }:
        raise HTTPException(400, "Only DICOM files supported")

    dicom_bytes = await file.read()
    ds = pydicom.dcmread(
        io.BytesIO(dicom_bytes),
        force=True
    )
    if not hasattr(ds, "PixelData"):
        raise ValueError("DICOM has no pixel data")

    img = dicom_to_uint8(ds)
    
    # Resize large images for speed
    h, w = img.shape[:2]
    if max(h, w) > 1600:
        scale = 1600 / max(h, w)
        img = np.array(
            np.resize(img, (int(h * scale), int(w * scale)))
        )

    # OCR (detail=0 = fastest)
    text = reader.readtext(img, detail=0)

    return {"text": text}

