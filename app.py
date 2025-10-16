import streamlit as st
import pandas as pd
import prb # <-- LA NUOVA LIBRERIA!

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
            # === MODIFICA CRUCIALE ===
            # Leggiamo il file .mpp usando la nuova libreria 'prb'.
            # È molto più semplice e non richiede Java.
            project = prb.read(uploaded_file)

            # --- 1. Estrazione Informazioni Generali ---
            st.header("📄 Informazioni Generali del Progetto")

            col1, col2 = st.columns(2)

            with col1:
                # Accediamo alle proprietà del progetto con una sintassi più pulita
                st.metric(label="Nome Appalto", value=project.name)

            with col2:
                # Formattiamo il costo
                costo_totale = project.cost
                st.metric(label="Importo Totale Lavori", value=f"€ {costo_totale:,.2f}".replace(",", "."))

            # --- 2. Estrazione TUP e TUF (Milestone) ---
            st.header("🎯 Traguardi di Progetto (TUP e TUF)")

            milestones_list = []
            # Scansioniamo tutte le attività
            for task in project.tasks:
                # La logica per identificare le milestone è simile
                if task.milestone or task.duration == 0:
                    milestones_list.append({
                        "Nome Traguardo": task.name,
                        "Data Inizio": task.start,
                        "Data Fine": task.finish,
                        "Durata (giorni)": task.duration
                    })

            if milestones_list:
                df_milestones = pd.DataFrame(milestones_list)
                # La formattazione delle date rimane uguale
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
