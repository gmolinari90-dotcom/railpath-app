# 1. Partiamo da un'immagine ufficiale di Python 3.11. È tutto ciò che ci serve.
FROM python:3.11-slim

# 2. Impostiamo la cartella di lavoro.
WORKDIR /app

# 3. Copiamo la nostra nuova, semplice lista dei requisiti.
COPY requirements.txt .

# 4. Installiamo i pacchetti. Sarà un'operazione pulita e veloce.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamo il resto del codice della nostra app.
COPY . .

# 6. Esponiamo la porta di Streamlit.
EXPOSE 8501

# 7. Definiamo il comando di avvio.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
