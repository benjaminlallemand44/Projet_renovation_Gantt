import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

st.title("📊 Assistant Planification du Projet de Rénovation")

# 1️⃣ Choix de l'état du projet
etat = st.selectbox(
    "Où en es-tu dans ton projet de rénovation ?",
    ["-- Sélectionnez --",
     "L'audit n'est pas encore fait",
     "Nous venons de recevoir l'audit",
     "Je veux lancer mon marché de recrutement de maitrise d'oeuvre",
     "J'ai recruté mon équipe de maitrise d'oeuvre"]
)

if etat == "-- Sélectionnez --":
    st.info("Sélectionnez votre état du projet pour afficher les étapes.")
else:
    start_date = st.date_input("📅 Date de début du projet")

    phases = []

    # --- Audit ---
    if etat in ["L'audit n'est pas encore fait", "Nous venons de recevoir l'audit"]:
        with st.expander("Audit", expanded=True):
            phases_audit = []
            if etat == "L'audit n'est pas encore fait":
                phases_audit += [
                    {"nom":"Analyse du besoin", "duree":2, "modifiable":True, "delai_mo":0},
                    {"nom":"Passation du marché et analyse", "duree":3, "modifiable":True, "delai_mo":0},
                    {"nom":"Réalisation de l'étude et restitution", "duree":4, "modifiable":True, "delai_mo":0},
                ]
            # Étapes fixes audit
            phases_audit += [
                {"nom":"Analyse et restitution de l'audit", "duree":2, "modifiable":True, "delai_mo":0},
                {"nom":"Prise de décision des élus", "duree":8, "modifiable":True, "delai_mo":0},
                {"nom":"Étape de programmation", "duree":4, "modifiable":True, "delai_mo":0},
            ]
            for phase in phases_audit:
                if phase["modifiable"]:
                    phase["duree"] = st.number_input(f"{phase['nom']} (durée en semaines)", min_value=1, value=phase["duree"])
            phases += phases_audit

    # --- Recrutement MOE ---
    if etat in ["L'audit n'est pas encore fait", "Nous venons de recevoir l'audit", "Je veux lancer mon marché de recrutement de maitrise d'oeuvre"]:
        with st.expander("Recrutement de la MOE", expanded=True):
            phases_recrut = [
                {"nom":"Rédaction des cahiers des charges et lancement du marché", "duree":8, "modifiable":True, "delai_mo":0},
                {"nom":"Publication, analyse du marché et sélection de la MOE", "duree":8, "modifiable":True, "delai_mo":0},
            ]
            for phase in phases_recrut:
                if phase["modifiable"]:
                    phase["duree"] = st.number_input(f"{phase['nom']} (durée en semaines)", min_value=1, value=phase["duree"])
            phases += phases_recrut

    # --- MOE / Loi MOP ---
    if etat in ["L'audit n'est pas encore fait","Nous venons de recevoir l'audit",
                "Je veux lancer mon marché de recrutement de maitrise d'oeuvre",
                "J'ai recruté mon équipe de maitrise d'oeuvre"]:
        with st.expander("MOE (Loi MOP)", expanded=True):
            phases_mop = [
                {"nom":"DIAG - Diagnostic & Études d’Esquisse", "duree":4, "modifiable":True, "delai_mo":2},
                {"nom":"APS - Avant-Projet Sommaire", "duree":4, "modifiable":True, "delai_mo":2},
                {"nom":"APD - Avant-Projet Définitif", "duree":8, "modifiable":True, "delai_mo":3},
                {"nom":"Constitution Dossier Autorisation", "duree":2, "modifiable":True, "delai_mo":2},
                {"nom":"PRO - Études de Projet", "duree":6, "modifiable":True, "delai_mo":3},
                {"nom":"ACT - Assistance passation marchés", "duree":2, "modifiable":True, "delai_mo":1},
                {"nom":"VISA - Visa Etudes d’Exécution", "duree":1, "modifiable":True, "delai_mo":0},
                {"nom":"DET - Direction Exécution Travaux", "duree":8, "modifiable":True, "delai_mo":0},
            ]
            for phase in phases_mop:
                if phase["modifiable"]:
                    phase["duree"] = st.number_input(f"{phase['nom']} (durée en semaines)", min_value=1, value=phase["duree"])
            phases += phases_mop

   
    # -------------------
    # Génération du diagramme compact avec style amélioré
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
        fig.update_layout(
            height=900,           # hauteur du graphique
            width=1400,           # largeur du graphique
            margin=dict(l=50, r=50, t=80, b=50),
            title=dict(font=dict(size=20, color="#0915a6")),  # titre
            xaxis=dict(tickfont=dict(size=14)),               # taille des repères temporels
            yaxis=dict(tickfont=dict(size=12))                # taille des noms des tâches
        )
        fig.update_traces(marker_line_width=1, marker_line_color='black')  # contour des barres
    
        st.plotly_chart(fig, use_container_width=True)
