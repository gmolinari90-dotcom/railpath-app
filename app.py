import streamlit as st
import pandas as pd
from jpype import *
from mpxj import *

st.set_page_config(page_title="RailPath", page_icon="🚆", layout="wide")
st.title("🚆 RailPath: Centrale di Controllo Progetti")
st.markdown("Carica il tuo file di progetto `.mpp` per iniziare l'analisi.")

uploaded_file = st.file_uploader(
    "Seleziona il file di baseline (.mpp)",
    type=["mpp"]
)

if uploaded_file is not None:
    with st.spinner('Analisi del file in corso... attendere prego.'):
        try:
            # Usiamo il percorso esatto della JVM che viene installata nel nostro Dockerfile
            jvm_path = "/usr/lib/jvm/java-21-openjdk-amd64/lib/server/libjvm.so"
            if not isJVMStarted():
                startJVM(jvm_path, "-ea")

            project = UniversalProjectReader().read(uploaded_file)

            st.header("📄 Informazioni Generali del Progetto")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Nome Appalto", value=project.getProjectProperties().getName())
            with col2:
                costo_totale = project.getProjectProperties().getCost()
                st.metric(label="Importo Totale Lavori", value=f"€ {costo_totale:,.2f}".replace(",", "."))

            st.header("🎯 Traguardi di Progetto (TUP e TUF)")
            milestones_list = []
            for task in project.getTasks():
                if task.getMilestone() or task.getDuration().getDuration() == 0:
                    milestones_list.append({
                        "Nome Traguardo": task.getName(),
                        "Data Inizio": task.getStart(),
                        "Data Fine": task.getFinish(),
                        "Durata (giorni)": task.getDuration().getDuration()
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
