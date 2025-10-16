# 1. Partiamo da un'immagine ufficiale di Python 3.11, che è stabile.
FROM python:3.11-slim

# 2. Impostiamo la cartella di lavoro all'interno del nostro computer virtuale.
WORKDIR /app

# 3. Aggiorniamo la lista dei pacchetti e installiamo GLI "ATTREZZI" E LA VERSIONE CORRETTA DI JAVA.
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamo il nostro file dei requisiti Python.
COPY requirements.txt .

# 5. Usiamo pip per installare i requisiti.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamo il resto del codice della nostra app (app.py).
COPY . .

# 7. Esponiamo la porta che Streamlit userà per comunicare.
EXPOSE 8501

# 8. Definiamo il comando per avviare l'applicazione.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
