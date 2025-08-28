import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# --------------------
# 0️⃣ Titre et introduction
st.title("📊 Assistant Planification du Projet de Rénovation")
st.markdown("""
Bienvenue dans l'outil de planification de projet de rénovation.  
Sélectionnez l'état actuel de votre projet et la date de début, puis ajustez les durées des phases pour générer un diagramme de Gantt interactif et clair.  

Les phases sont organisées par catégories : **Audit**, **Recrutement MOE**, et **Loi MOP**.
""")
st.divider()

# --------------------
# 1️⃣ Choix de l'état du projet
etat = st.selectbox(
    "Où en êtes-vous dans votre projet de rénovation énergétique ?",
    ["-- Sélectionnez --",
     ""Nous n'avons pas encore effectué d'audit énergétique",
     "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
     "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
     "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]
)

if etat == "-- Sélectionnez --":
    st.info("Sélectionnez votre état du projet pour afficher les étapes.")
else:
    start_date = st.date_input("📅 Date de début du projet")
    phases = []

    # --------------------
    # --- Audit ---
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique", "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)"]:
        with st.expander("📋 Études préalables", expanded=True):
            phases_audit = []
            if etat == "Nous n'avons pas encore effectué d'audit énergétique":
                phases_audit += [
                    {"nom":"📝 Analyse du site: Faisabilité, diagnostics diverses et audit énergétique ", "duree":20, "modifiable":True, "delai_mo":0},
                    {"nom":"📝 Restitution de l'audit énergétique", "duree":2, "modifiable":True, "delai_mo":0},
                ]
            # Étapes fixes audit
            phases_audit += [
                {"nom":"📝 Analyse des comptes-rendus d'audits", "duree":2, "modifiable":True, "delai_mo":0},
                {"nom":"📝 Prise de décision des élus", "duree":0, "modifiable":False, "delai_mo":6},
                {"nom":"📝 Rédaction du programme de travaux et validation", "duree":4, "modifiable":True, "delai_mo":2},
            ]
            for idx, phase in enumerate(phases_audit):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.text(phase["nom"])
                    with col2:
                        phase["duree"] = st.number_input(
                            "",
                            min_value=1,
                            value=phase["duree"],
                            key=f"audit_{idx}_{phase['nom']}"
                        )
            phases += phases_audit

    # --------------------
    # --- Sélection d'un MOE ---
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique", "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)", "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre"]:
        with st.expander("🧑‍💼 Sélection d'une MOE", expanded=True):
            phases_recrut = [
                {"nom":"📝 Rédaction des cahiers des charges et lancement du marché", "duree":8, "modifiable":True, "delai_mo":0},
                {"nom":"📝 Publication, analyse du marché et sélection de la MOE", "duree":8, "modifiable":True, "delai_mo":0},
            ]
            for idx, phase in enumerate(phases_recrut):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.text(phase["nom"])
                    with col2:
                        phase["duree"] = st.number_input(
                            "",
                            min_value=1,
                            value=phase["duree"],
                            key=f"recrut_{idx}_{phase['nom']}"
                        )
            phases += phases_recrut

    # --------------------
    # --- MOE / Loi MOP ---
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique", "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)", "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
                "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]:
        with st.expander("🏗️ MOE (Loi MOP)", expanded=True):
            phases_mop = [
                {"nom":"📝 DIAG - Diagnostic & Études d’Esquisse", "duree":4, "modifiable":True, "delai_mo":2},
                {"nom":"📝 APS - Avant-Projet Sommaire", "duree":4, "modifiable":True, "delai_mo":2},
                {"nom":"📝 APD - Avant-Projet Définitif", "duree":8, "modifiable":True, "delai_mo":3},
                {"nom":"📝 Constitution Dossier Autorisation", "duree":2, "modifiable":True, "delai_mo":2},
                {"nom":"📝 PRO - Études de Projet", "duree":6, "modifiable":True, "delai_mo":3},
                {"nom":"📝 DCE - Études de Projet", "duree":6, "modifiable":True, "delai_mo":3},
                {"nom":"📝 ACT - Assistance passation marchés", "duree":2, "modifiable":True, "delai_mo":1},
                {"nom":"📝 VISA - Visa Etudes d’Exécution", "duree":1, "modifiable":True, "delai_mo":0},
                {"nom":"🚧 DET - Direction Exécution Travaux", "duree":8, "modifiable":True, "delai_mo":0},
                {"nom":"👷‍♂️👷‍♀️ AOR - Assistance aux opérations de réception", "duree":4, "modifiable":True, "delai_mo":0}
            ]
            for idx, phase in enumerate(phases_mop):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.text(phase["nom"])
                    with col2:
                        phase["duree"] = st.number_input(
                            "",
                            min_value=1,
                            value=phase["duree"],
                            key=f"mop_{idx}_{phase['nom']}"
                        )
            phases += phases_mop

    st.divider()

    # --------------------
    # Génération du diagramme
    if st.button("Générer le diagramme de Gantt"):
        tasks = []
        current_start = start_date
    
        for phase in phases:
            start = current_start
            end = start + timedelta(weeks=phase["duree"])
            tasks.append(dict(Task=phase["nom"], Start=start, Finish=end, Type='Phase'))
            if phase["delai_mo"] > 0:
                delay_start = end
                delay_end = delay_start + timedelta(weeks=phase["delai_mo"])
                tasks.append(dict(Task=phase["nom"], Start=delay_start, Finish=delay_end, Type='Délai MO'))
            current_start = end + timedelta(weeks=phase["delai_mo"])
    
        df = pd.DataFrame(tasks)
        
        # ➕ Ajout de la barre "Recherche de financement"
        if not df.empty:
            df = pd.concat([
                df,
                pd.DataFrame([{
                    "Task":"💶 Recherche de financement",
                    "Start":df["Start"].min(),
                    "Finish":df["Start"].min() + timedelta(weeks=6),
                    "Type":"Financement",
                    "Groupe":"Financement"
                }])
            ], ignore_index=True)
    
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Type",
            color_discrete_map={"Phase": "#0915a6", "Délai MO": "#ff5300", "Financement":"green"},
            title="📅 Diagramme de Gantt du projet"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_traces(marker_line_width=1, marker_line_color='black')

        # ➕ Regroupement par grandes parties
        groupe_ranges = df.groupby("Groupe").agg({"Start":"min", "Finish":"max"}).reset_index()
        for _, row in groupe_ranges.iterrows():
            if row["Groupe"] != "Financement":  # éviter de tracer au-dessus pour financement
                fig.add_trace(go.Scatter(
                    x=[row["Start"], row["Finish"]],
                    y=[len(df["Task"].unique())+1]*2,
                    mode="lines",
                    line=dict(color="black", width=8),
                    name=row["Groupe"],
                    showlegend=False,
                    hoverinfo="text",
                    text=row["Groupe"]
                ))

        # ➕ Ligne verticale entre Études préalables et Sélection MOE
        if "Études préalables" in df["Groupe"].values and "Sélection MOE" in df["Groupe"].values:
            transition_date = df[df["Groupe"] == "Études préalables"]["Finish"].max()
            fig.add_vline(x=transition_date, line_width=2, line_dash="solid", line_color="black")
            fig.add_annotation(
                x=transition_date, y=-0.5,
                text="💶",
                showarrow=False,
                font=dict(size=18, color="black"),
                yshift=-30
            )
            
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Type",
            color_discrete_map={"Phase": "#0915a6", "Délai MO": "#ff5300"},
            title="📅 Diagramme de Gantt du projet"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_traces(marker_line_width=1, marker_line_color='black')
        fig.update_layout(
            height=900,
            width=1400,
            margin=dict(l=50, r=50, t=80, b=50),
            title=dict(font=dict(size=20, color="#0915a6")),
            xaxis=dict(tickfont=dict(size=14)),
            yaxis=dict(tickfont=dict(size=12))
        )
    
        st.plotly_chart(fig, use_container_width=True)


