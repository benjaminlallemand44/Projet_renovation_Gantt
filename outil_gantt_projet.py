import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# --------------------
# Glossaire simplifié pour affichage dans les inputs (tooltips)
GLOSSAIRE = {
    "DIAG": "Analyse fonctionnelle, urbanistique et technique du bâti existant, estimation financière et faisabilité.",
    "ESQ": "Proposer des solutions d'ensemble, vérifier faisabilité et compatibilité financière (n’apparaît pas sur le GANTT).",
    "APS": "Proposer solutions traduisant le programme fonctionnel, dispositions techniques générales et estimation coût (min 3 semaines).",
    "APD": "Déterminer surfaces détaillées, plans, façades, principes constructifs et cohérence technique et économique (min 6 semaines).",
    "Autorisations Administratives": "Rédaction des documents nécessaires aux autorisations (Permis de Construire / Déclaration Préalable).",
    "PRO": "Préciser les éléments conceptuels, établir coût prévisionnel et délai global de réalisation (min 4 semaines).",
    "ACT / AMT": "Assistance pour la passation des marchés : préparer la consultation, analyser les offres, vérifier conformité.",
    "DCE": "Dossier de Consultation des Entreprises fourni par la maîtrise d’œuvre pour consultation des entreprises.",
    "EXE": "Études d'exécution : documents et suivi technique pour réaliser l'ouvrage, mise à jour du calendrier.",
    "AOR": "Assistance aux opérations de réception : suivi des réserves, validation des DOE et gestion des désordres en GPA."
}

# Glossaire complet pour affichage sous le Gantt
GLOSSAIRE_COMPLET = {
    "DIAG": "Phase DIAG : Cette étape de la mission conception a pour objet d'établir “un état des lieux, de fournir une analyse fonctionnelle, urbanistique, architecturale et technique du bâti existant et ainsi de permettre d'établir un programme fonctionnel d'utilisation du bâtiment ainsi qu'une estimation financière et d'en déduire la faisabilité de l'opération.",
    "ESQ": "Phase ESQ : cette étape de la mission conception a pour objet de “proposer une ou plusieurs solutions d'ensemble, traduisant les éléments majeurs du programme, d'en indiquer les délais de réalisation, d'examiner leur compatibilité avec la partie de l'enveloppe financière prévisionnelle retenue par le maître d'ouvrage et affectée aux travaux, ainsi que de vérifier la faisabilité de l'opération au regard des différentes contraintes du programme et du site. (la mission n’apparaît pas sur le GANTT d’ailleurs)",
    "APS": "Phase APS : cette étape de la mission conception a pour objet de proposer des solutions traduisant le programme fonctionnel, d'en présenter les dispositions générales techniques, d'indiquer des durées prévisionnelles et d'établir une estimation provisoire du coût prévisionnel des travaux.",
    "APD": "Phase APD : déterminer les surfaces détaillées de tous les éléments du programme, arrêter plans, coupes et façades, définir principes constructifs, matériaux et installations et vérifier cohérence technique et économique.",
    "Autorisations Administratives": "Lorsque l’APD est validé, rédiger les documents nécessaires à l’obtention des autorisations administratives et suivre l’instruction auprès des services administratifs.",
    "PRO": "Phase PRO : préciser, déterminer, décrire les éléments de conception des phases précédentes, établir un coût prévisionnel et un délai global de réalisation.",
    "ACT / AMT": "Assistance pour préparer la consultation des entreprises, analyser les offres et vérifier leur conformité technique et financière.",
    "DCE": "Fournir le dossier de consultation des entreprises comportant les pièces nécessaires à la consultation et les choix du maître d’ouvrage.",
    "EXE": "Réaliser l’ouvrage en suivant les plans et études préalables, actualiser le calendrier et suivre les lots.",
    "AOR": "Assurer le suivi des réserves jusqu’à levée, valider les DOE et examiner les désordres pendant la période de GPA."
}

# --------------------
# 0️⃣ Titre et introduction
st.set_page_config(layout="wide")
st.title("📊 Assistant Planification du Projet de Rénovation")
st.markdown("""
Bienvenue dans l'outil de planification de projet de rénovation.  
Sélectionnez l'état actuel de votre projet et la **date de début**, puis ajustez les durées des phases (en **semaines**) pour générer un diagramme de Gantt interactif et clair.  

Les phases sont organisées par catégories : **Études préalables**, **Sélection MOE**, **MOE (Loi MOP)**.
""")
st.divider()

# --------------------
# Bandeaux catégories
cat_col1, cat_col2, cat_col3 = st.columns([1,1,1])
with cat_col1:
    st.markdown("**🟦 Études préalables**")
with cat_col2:
    st.markdown("**🟧 Sélection MOE**")
with cat_col3:
    st.markdown("**🟪 MOE (Loi MOP)**")

st.markdown("---")

# --------------------
# 1️⃣ Choix de l'état du projet
etat = st.selectbox(
    "Où en êtes-vous dans votre projet de rénovation énergétique ?",
    ["-- Sélectionnez --",
     "Nous n'avons pas encore effectué d'audit énergétique",
     "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
     "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
     "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]
)

if etat == "-- Sélectionnez --":
    st.info("Sélectionnez votre état du projet pour afficher les étapes.")
    st.stop()
else:
    # Recherche de financement
    st.subheader("💶 Recherche de financement")
    col_f1, col_f2 = st.columns([2,1])
    with col_f1:
        recherche_financement_weeks = st.number_input(
            "Durée Recherche de financement (semaines) — modifiable",
            min_value=0, value=6, key="financement_weeks"
        )
    with col_f2:
        include_financement = st.checkbox("Inclure la recherche de financement dans le Gantt", value=True)

    # Date de début
    start_date = st.date_input("📅 Date de début du projet", key="date_debut")
    st.markdown("Durées exprimées en **semaines** (valeurs modifiables).")

    phases = []

    # --------------------
    # Études préalables
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique", 
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)"]:
        with st.expander("📋 Études préalables", expanded=True):
            phases_audit = []
            if etat == "Nous n'avons pas encore effectué d'audit énergétique":
                phases_audit += [
                    {"nom":"📝 Rédaction du programme (si pas d'audit préalable)", "duree":3, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                    {"nom":"📝 Analyse du site: faisabilité, diagnostics et audit énergétique", "duree":20, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                    {"nom":"📝 Restitution de l'audit énergétique", "duree":2, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                ]
            else:
                phases_audit += [
                    {"nom":"📝 Analyse des comptes-rendus d'audits", "duree":2, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                ]
            phases_audit += [
                {"nom":"📝 Prise de décision des élus", "duree":0, "modifiable":False, "delai_mo":6, "groupe":"Études préalables"},
                {"nom":"📝 Rédaction du programme de travaux et validation", "duree":4, "modifiable":True, "delai_mo":2, "groupe":"Études préalables"},
            ]
            for idx, phase in enumerate(phases_audit):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.write(phase["nom"])
                    with col2:
                        phase["duree"] = st.number_input(
                            "semaines",
                            min_value=0 if phase["nom"].startswith("📝 Prise") else 1,
                            value=phase["duree"],
                            key=f"audit_{idx}_{phase['nom']}"
                        )
            phases += phases_audit

    # --------------------
    # Sélection MOE
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre"]:
        with st.expander("🧑‍💼 Sélection d'une MOE", expanded=True):
            phases_recrut = [
                {"nom":"📝 Rédaction des cahiers des charges et lancement du marché", "duree":8, "modifiable":True, "delai_mo":0, "groupe":"Sélection MOE"},
                {"nom":"📝 Publication, analyse du marché et sélection de la MOE", "duree":8, "modifiable":True, "delai_mo":0, "groupe":"Sélection MOE"},
                {"nom":"📝 Commission d'appel d'offres", "duree":2, "modifiable":True, "delai_mo":0, "groupe":"Sélection MOE"},
                {"nom":"📝 Signature des marchés", "duree":1, "modifiable":True, "delai_mo":0, "groupe":"Sélection MOE"},
            ]
            for idx, phase in enumerate(phases_recrut):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.write(phase["nom"])
                    with col2:
                        phase["duree"] = st.number_input(
                            "semaines",
                            min_value=1,
                            value=phase["duree"],
                            key=f"recrut_{idx}_{phase['nom']}"
                        )
            phases += phases_recrut

    # --------------------
    # MOE / Loi MOP
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
                "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]:
        with st.expander("🏗️ MOE (Loi MOP)", expanded=True):
            phases_mop = [
                {"nom":"📝 DIAG - Diagnostic & Études d’Esquisse", "duree":4, "modifiable":True, "delai_mo":2, "groupe":"MOE"},
                {"nom":"📝 ESQ - Esquisse (non affichée sur le GANTT)", "duree":0, "modifiable":False, "delai_mo":0, "groupe":"MOE"},
                {"nom":"📝 APS - Avant-Projet Sommaire", "duree":4, "modifiable":True, "delai_mo":2, "groupe":"MOE"},
                {"nom":"📝 APD - Avant-Projet Définitif", "duree":8, "modifiable":True, "delai_mo":3, "groupe":"MOE"},
                {"nom":"📝 Constitution Dossier Autorisation", "duree":2, "modifiable":True, "delai_mo":2, "groupe":"MOE"},
                {"nom":"📝 PRO - Études de Projet", "duree":6, "modifiable":True, "delai_mo":3, "groupe":"MOE"},
                {"nom":"📝 DCE - Études de Projet", "duree":6, "modifiable":True, "delai_mo":3, "groupe":"MOE"},
                {"nom":"📝 ACT - Assistance passation marchés", "duree":2, "modifiable":True, "delai_mo":1, "groupe":"MOE"},
                {"nom":"📝 VISA - Visa Etudes d’Exécution", "duree":1, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
                {"nom":"🚧 DET - Direction Exécution Travaux", "duree":8, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
                {"nom":"👷‍♂️👷‍♀️ AOR - Assistance aux opérations de réception", "duree":4, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
            ]
            for idx, phase in enumerate(phases_mop):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(phase["nom"])
                    brief_def = GLOSSAIRE.get(phase["nom"].split(" - ")[0].split(" ")[-1], "")
                    if brief_def:
                        st.caption(brief_def)
                with col2:
                    min_val = 1
                    if "APS" in phase["nom"]:
                        min_val = 3
                    elif "APD" in phase["nom"]:
                        min_val = 6
                    elif "PRO" in phase["nom"]:
                        min_val = 4
                    if phase["modifiable"]:
                        phase["duree"] = st.number_input(
                            "semaines",
                            min_value=min_val,
                            value=phase["duree"],
                            key=f"mop_{idx}_{phase['nom']}"
                        )
            phases += phases_mop

    st.divider()
    st.warning("Vigilance (DET / AOR) : Les délais DET / AOR sont indicatifs et peuvent évoluer selon disponibilité des entreprises, matériaux et équipes MOE.")

    # --------------------
    # Génération Gantt
    if st.button("Générer le diagramme de Gantt"):
        tasks = []
        current_start = pd.to_datetime(start_date)

        # Recherche financement
        if include_financement:
            fin_start = current_start
            fin_end = fin_start + timedelta(weeks=recherche_financement_weeks)
            tasks.append(dict(Task="💶 Recherche de financement", Start=fin_start, Finish=fin_end,
                              Type="Financement", Groupe="Financement", Definition="Recherche et montage des financements (subventions, prêts, etc.)."))
            current_start = fin_end

        for phase in phases:
            if phase["nom"].startswith("ESQ"):
                continue  # n'apparait pas sur le Gantt
            start = current_start
            dur = phase["duree"]
            delay = phase.get("delai_mo",0)
            end_phase = start + timedelta(weeks=dur)
            tasks.append(dict(Task=phase["nom"], Start=start, Finish=end_phase,
                              Type='Phase', Groupe=phase["groupe"], Definition=GLOSSAIRE.get(phase["nom"].split(" - ")[0], "")))
            if delay > 0:
                end_delay = end_phase + timedelta(weeks=delay)
                tasks.append(dict(Task=phase["nom"], Start=end_phase, Finish=end_delay,
                                  Type='Délai MO', Groupe=phase["groupe"], Definition=GLOSSAIRE.get(phase["nom"].split(" - ")[0], "")))
                current_start = end_delay
            else:
                current_start = end_phase

        df = pd.DataFrame(tasks)
        if df.empty:
            st.info("Aucune phase à afficher.")
            st.stop()

        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"].fillna("") + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"

        fig = px.timeline(
            df, x_start="Start", x_end="Finish", y="Task", color="Type",
            custom_data=["hover_def","Groupe"],
            color_discrete_map={"Phase":"#0915a6","Délai MO":"#ff5300","Financement":"green"}
        )
        fig.update_traces(
            hovertemplate="%{y}<br>%{customdata[0]}<br>Catégorie: %{customdata[1]}<extra></extra>",
            marker_line_width=1, marker_line_color='black'
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=900,width=1400,
                          margin=dict(l=50,r=50,t=120,b=80),
                          title=dict(text="📅 Diagramme de Gantt du projet — unités : semaines", font=dict(size=18,color="#0915a6")),
                          xaxis=dict(tickfont=dict(size=14),title="Date"),
                          yaxis=dict(tickfont=dict(size=12),title="Phases"),
                          plot_bgcolor="white")
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

        # Bandeaux catégories
        groups_to_show = ["Études préalables","Sélection MOE","MOE","Financement"]
        color_map_group = {"Études préalables":"#cfe3ff","Sélection MOE":"#ffe5cc","MOE":"#e6ccff","Financement":"#d6f5d6"}
        shapes = []
        annotations = []
        for grp in groups_to_show:
            grp_df = df[df["Groupe"]==grp]
            if grp_df.empty: continue
            s = grp_df["Start"].min()
            f = grp_df["Finish"].max()
            shapes.append(dict(type="rect", xref="x", yref="paper", x0=s, x1=f, y0=1.02, y1=1.08,
                               fillcolor=color_map_group.get(grp,"#dddddd"), line=dict(width=0), opacity=0.8))
            annotations.append(dict(x=s + (f-s)/2, y=1.095, xref="x", yref="paper",
                                    text=f"<b>{grp}</b>", showarrow=False, align="center", font=dict(size=12,color="black")))
        fig.update_layout(shapes=shapes, annotations=annotations)

        # Ligne verticale € entre Études préalables et Sélection MOE
        if "Études préalables" in df["Groupe"].values and "Sélection MOE" in df["Groupe"].values:
            transition_date = df[df["Groupe"]=="Études préalables"]["Finish"].max()
            fig.add_vline(x=transition_date,line_width=2,line_dash="solid",line_color="black")
            fig.add_annotation(x=transition_date,y=-0.5,text="💶",showarrow=False,font=dict(size=18,color="black"),yshift=-30)

        st.plotly_chart(fig,use_container_width=True)

      
        # Tableau HTML coloré et scrollable
        color_map = {
            "DIAG":"#cfe3ff",
            "ESQ":"#cfe3ff",
            "APS":"#cfe3ff",
            "APD":"#cfe3ff",
            "Autorisations Administratives":"#ffe5cc",
            "PRO":"#e6ccff",
            "ACT / AMT":"#e6ccff",
            "DCE":"#e6ccff",
            "EXE":"#e6ccff",
            "AOR":"#e6ccff"
        }
        
        html_gloss = """
        <div style='max-height:600px; overflow-y:auto;'>
        <table style='border-collapse: collapse; width: 100%;'>
        <tr><th style='border: 1px solid black; padding:5px;'>Phase</th>
        <th style='border: 1px solid black; padding:5px;'>Définition</th></tr>
        """
        
        for phase, def_text in GLOSSAIRE_COMPLET.items():
            color = color_map.get(phase,"#ffffff")
            html_gloss += f"""
            <tr style='background-color:{color};'>
                <td style='border: 1px solid black; padding:5px; vertical-align: top; font-weight:bold;'>{phase}</td>
                <td style='border: 1px solid black; padding:5px; vertical-align: top;'>{def_text}</td>
            </tr>
            """
        
        html_gloss += "</table></div>"
        
        st.markdown("### 📚 Glossaire des phases", unsafe_allow_html=True)
        st.markdown(html_gloss, unsafe_allow_html=True)

