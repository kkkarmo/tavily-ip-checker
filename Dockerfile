FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tavily.py .
COPY vt_results.txt .
COPY .env .

CMD ["python", "tavily.py"]
