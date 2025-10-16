# 1. Partiamo da Python 3.11.
FROM python:3.11-slim

# 2. Impostiamo la cartella di lavoro.
WORKDIR /app

# 3. Installiamo tutti gli attrezzi necessari.
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 4. === LA SOLUZIONE DEFINITIVA ===
#    Questa riga dice a Git: "Non provare MAI a chiedere una password".
#    Questo risolve l'errore "could not read Username".
ENV GIT_TERMINAL_PROMPT=0

# 5. Copiamo la lista dei requisiti.
COPY requirements.txt .

# 6. Installiamo i pacchetti. Ora il download da GitHub con https funzionerà.
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiamo il resto della nostra applicazione.
COPY . .

# 8. Esponiamo la porta.
EXPOSE 8501

# 9. Definiamo il comando di avvio.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
