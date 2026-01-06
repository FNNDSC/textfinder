FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download EasyOCR models at build time
RUN python - <<EOF
import easyocr
easyocr.Reader(
    ['en'],
    gpu=True,
    model_storage_directory='/models'
)
EOF

COPY . .

CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8000"]

