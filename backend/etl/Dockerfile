FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "-c", "python misp_etl.py & python otx_etl.py & python vt_etl.py & python siem_etl.py"]
