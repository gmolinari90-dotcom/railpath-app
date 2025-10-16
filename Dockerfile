# 1. Partiamo da un'immagine ufficiale di Python 3.11.
FROM python:3.11-slim

# 2. Impostiamo la cartella di lavoro.
WORKDIR /app

# 3. Installiamo TUTTI gli attrezzi necessari in un colpo solo.
#    - 'git': Per scaricare il codice da GitHub.
#    - 'build-essential': Per "montare" mpxjpy.
#    - 'openjdk-21-jre-headless': Il nostro Java.
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamo la nostra nuova lista dei requisiti.
COPY requirements.txt .

# 5. Installiamo i pacchetti. Ora pip scaricherà mpxjpy da GitHub e lo compilerà.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamo il resto del codice della nostra app.
COPY . .

# 7. Esponiamo la porta di Streamlit.
EXPOSE 8501

# 8. Definiamo il comando di avvio.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
