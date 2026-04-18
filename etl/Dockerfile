FROM python:3.14-slim

WORKDIR /wd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y xvfb
RUN playwright install-deps chromium
RUN playwright install chromium

COPY app ./etl/app
COPY app.py ./etl/
COPY backend_connect.py ./etl/

#"xvfb-run"
CMD ["xvfb-run", "uvicorn", "etl.backend_connect:app", "--host", "0.0.0.0", "--port", "8080"]
