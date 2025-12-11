FROM python:3.11-slim
WORKDIR /app
# Создаем папку для uploads
RUN mkdir -p /app/uploads/perfumes /app/uploads/temp
RUN chmod 755 /app/uploads
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
VOLUME ["/app/uploads"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]