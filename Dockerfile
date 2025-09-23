FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["sh", "-c", "streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --logger.level=info"]