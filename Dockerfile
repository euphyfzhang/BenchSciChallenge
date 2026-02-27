FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY interative_graph_v1.py .

EXPOSE 8080

CMD ["streamlit", "run", "interative_graph_v1.py", "--server.port=8080", "--server.address=0.0.0.0"]