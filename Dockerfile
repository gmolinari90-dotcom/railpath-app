# 1. Partiamo da un'immagine ufficiale di Python 3.11, che è stabile.
FROM python:3.11-slim

# 2. Impostiamo la cartella di lavoro.
WORKDIR /app

# 3. Aggiorniamo la lista dei pacchetti e installiamo TUTTO il necessario in un colpo solo:
#    - 'build-essential': La nostra "cassetta degli attrezzi".
#    - 'openjdk-21-jre-headless': La versione corretta di Java.
#    - 'wget': Il programma che useremo per scaricare il file che ci manca.
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-21-jre-headless \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 4. SCARICHIAMO IL FILE PROBLEMATICO DIRETTAMENTE DENTRO AL NOSTRO AMBIENTE.
#    Questo è il link ufficiale e diretto.
RUN wget https://files.pythonhosted.org/packages/45/30/171587d549f6350f4a8677c7d428a1c93a033f2c5d18d09aa1dfd7146564/mpxjpy-1.3.1.tar.gz

# 5. Copiamo il file requirements.txt dalla tua repository.
COPY requirements.txt .

# 6. Usiamo pip per installare i requisiti. Ora troverà il file mpxjpy perché lo abbiamo appena scaricato.
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiamo il resto del codice della nostra app (app.py).
COPY . .

# 8. Esponiamo la porta che Streamlit userà per comunicare.
EXPOSE 8501

# 9. Definiamo il comando per avviare l'applicazione.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
