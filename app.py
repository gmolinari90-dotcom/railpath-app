# Importiamo le librerie necessarie
import streamlit as st
import pandas as pd
from jpype import *
from mpxj import *

# --- Configurazione della Pagina ---
# Impostiamo il titolo che apparirà nella tab del browser e l'icona
st.set_page_config(page_title="RailPath", page_icon="🚆", layout="wide")

# --- Titolo e Descrizione Principale ---
st.title("🚆 RailPath: Centrale di Controllo Progetti")
st.markdown("Carica il tuo file di progetto `.mpp` per iniziare l'analisi.")

# --- Sezione di Caricamento File ---
uploaded_file = st.file_uploader(
    "Seleziona il file di baseline (.mpp)",
    type=["mpp"] # Accettiamo solo file con estensione .mpp
)

# --- Logica di Elaborazione ---
# Il codice dentro questo "if" viene eseguito solo dopo che un file è stato caricato
if uploaded_file is not None:

    # Mostra una barra di avanzamento mentre il file viene processato
    with st.spinner('Analisi del file in corso... attendere prego.'):
        try:
            # mpxj richiede l'avvio di una Java Virtual Machine (JVM)
            startJVM(getDefaultJVMPath(), "-ea")

            # Lettura del file .mpp direttamente dalla memoria
            project = UniversalProjectReader().read(uploaded_file)

            # --- 1. Estrazione Informazioni Generali ---
            st.header("📄 Informazioni Generali del Progetto")

            # Usiamo le colonne per mostrare le info affiancate
            col1, col2 = st.columns(2)

            with col1:
                # Nome dell'appalto (preso dal nome del progetto)
                st.metric(label="Nome Appalto", value=project.getProjectProperties().getName())
            
            with col2:
                # Importo totale dei lavori, formattato come valuta
                costo_totale = project.getProjectProperties().getCost()
                st.metric(label="Importo Totale Lavori", value=f"€ {costo_totale:,.2f}".replace(",", "."))

            # --- 2. Estrazione TUP e TUF (Milestone) ---
            st.header("🎯 Traguardi di Progetto (TUP e TUF)")

            milestones_list = []
            # Scansioniamo tutte le attività del progetto
            for task in project.getTasks():
                # Consideriamo "milestone" le attività con durata zero o contrassegnate come tali
                if task.getMilestone() or task.getDuration().getDuration() == 0:
                    milestones_list.append({
                        "Nome Traguardo": task.getName(),
                        "Data Inizio": task.getStart(),
                        "Data Fine": task.getFinish(),
                        "Durata (giorni)": task.getDuration().getDuration()
                    })
            
            # Se abbiamo trovato dei traguardi, li mostriamo in una tabella
            if milestones_list:
                # Convertiamo la lista in un DataFrame Pandas per una migliore visualizzazione
                df_milestones = pd.DataFrame(milestones_list)

                # Formattiamo le date per una lettura più semplice
                df_milestones['Data Inizio'] = pd.to_datetime(df_milestones['Data Inizio']).dt.strftime('%d/%m/%Y')
                df_milestones['Data Fine'] = pd.to_datetime(df_milestones['Data Fine']).dt.strftime('%d/%m/%Y')
                
                # Mostriamo la tabella interattiva
                st.dataframe(df_milestones, use_container_width=True)
            else:
                st.warning("Nessun traguardo (TUP/TUF) trovato nel file di progetto.")

        except Exception as e:
            st.error(f"Si è verificato un errore durante l'analisi del file: {e}")
        
        finally:
            # È fondamentale chiudere la JVM per liberare risorse
            shutdownJVM()

    st.success("Analisi iniziale completata! Le funzionalità avanzate sono ora disponibili.")
    st.markdown("---") # Aggiungiamo una linea di separazione

    # Qui, nei prossimi passaggi, attiveremo la Fase 2 (dashboard di analisi)
    # Per ora, mostriamo solo un messaggio.
    st.info("💡 **Prossimi Passi**: A breve qui potrai impostare il periodo di riferimento e avviare le analisi dettagliate.")
