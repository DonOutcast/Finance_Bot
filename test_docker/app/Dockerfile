FROM python:3.9-slim-bullseye as compile-image
WORKDIR /code
ADD requirements.txt requirements.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get update \
 && apt-get install -y gcc \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY app.py app.py
CMD ["python", "-u", "app.py"]
