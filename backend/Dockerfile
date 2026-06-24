FROM python:3.14-slim

WORKDIR /main

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY main.py ./

#RUN python -m app.repository.init_db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
