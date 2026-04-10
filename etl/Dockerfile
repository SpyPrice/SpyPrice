FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y xvfb chromium

COPY app.py ./app.py
COPY get_price ./get_price
#port 725

CMD [ "xvfb-run", "python", "app.py"]
