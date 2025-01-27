# Gunakan Python sebagai base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi
COPY ./app ./app

# Expose port
EXPOSE 8000

# Jalankan aplikasi dengan Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]