# Importiamo le librerie necessarie. Nota la nuova libreria!
import streamlit as st
import pandas as pd
from msproject.reader import MppReader

# --- Configurazione della Pagina ---
st.set_page_config(page_title="RailPath", page_icon="🚆", layout="wide")

# --- Titolo e Descrizione Principale ---
st.title("🚆 RailPath: Centrale di Controllo Progetti")
st.markdown("Carica il tuo file di progetto `.mpp` per iniziare l'analisi.")

# --- Sezione di Caricamento File ---
uploaded_file = st.file_uploader(
    "Seleziona il file di baseline (.mpp)",
    type=["mpp"]
)

# --- Logica di Elaborazione ---
if uploaded_file is not None:
    with st.spinner('Analisi del file in corso... attendere prego.'):
        try:
            # === LA SVOLTA: LEGGERE IL FILE CON LA NUOVA LIBRERIA ===
            # Non c'è più bisogno di avviare Java. È tutto Python.
            project = MppReader(uploaded_file)

            # --- 1. Estrazione Informazioni Generali ---
            st.header("📄 Informazioni Generali del Progetto")

            # Accediamo alle proprietà del progetto.
            # Nota: la libreria potrebbe non leggere il costo totale direttamente.
            # Lo calcoleremo noi sommando i costi delle attività principali.
            nome_progetto = project.properties.title or "Progetto senza nome"
            costo_totale = sum(task.cost for task in project.tasks if task.outline_level == 1)

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Nome Appalto", value=nome_progetto)
            with col2:
                st.metric(label="Importo Totale Lavori", value=f"€ {costo_totale:,.2f}".replace(",", "."))

            # --- 2. Estrazione TUP e TUF (Milestone) ---
            st.header("🎯 Traguardi di Progetto (TUP e TUF)")

            milestones_list = []
            for task in project.tasks:
                if task.is_milestone or task.duration == 0:
                    milestones_list.append({
                        "Nome Traguardo": task.name,
                        "Data Inizio": task.start_date,
                        "Data Fine": task.finish_date,
                        "Durata (giorni)": task.duration
                    })

            if milestones_list:
                df_milestones = pd.DataFrame(milestones_list)
                df_milestones['Data Inizio'] = pd.to_datetime(df_milestones['Data Inizio']).dt.strftime('%d/%m/%Y')
                df_milestones['Data Fine'] = pd.to_datetime(df_milestones['Data Fine']).dt.strftime('%d/%m/%Y')
                st.dataframe(df_milestones, use_container_width=True)
            else:
                st.warning("Nessun traguardo (TUP/TUF) trovato nel file di progetto.")

        except Exception as e:
            st.error(f"Si è verificato un errore durante l'analisi del file: {e}")

    st.success("Analisi iniziale completata! Le funzionalità avanzate sono ora disponibili.")
    st.markdown("---")
    st.info("💡 **Prossimi Passi**: A breve qui potrai impostare il periodo di riferimento e avviare le analisi dettagliate.")
