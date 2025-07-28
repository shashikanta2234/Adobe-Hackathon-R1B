FROM python:3.10-slim

WORKDIR /app
COPY ./src ./src
COPY requirements.txt .
COPY run.sh .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./src/embedding_model/')"

CMD ["bash", "run.sh"]
