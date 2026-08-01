# 1. Immagine di partenza
FROM python:3.12-slim

# 2. Comportamento di Python dentro un container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/alarms.db

# 3. Cartella di lavoro dentro l'immagine
WORKDIR /app

# 4. Dipendenze PRIMA del codice (sfrutta la cache dei layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Il codice dell'applicazione
COPY . .

# 6. Utente non-root + cartella dati
RUN useradd --create-home appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /data /app
USER appuser

# 7. Documenta la porta
EXPOSE 5000

# 8. Comando di avvio
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
