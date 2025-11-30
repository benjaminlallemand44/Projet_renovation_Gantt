import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# --------------------
# Glossaire (définitions fournies)
GLOSSAIRE = {
    "DIAG - Diagnostic & Études d’Esquisse":
        "Cette étape établit un état des lieux, une analyse fonctionnelle, urbanistique, architecturale et technique du bâti existant ; permet d'établir un programme fonctionnel et une estimation financière pour déterminer la faisabilité.",
    "ESQ - Esquisse":
        "Proposer une ou plusieurs solutions d'ensemble traduisant les éléments majeurs du programme, indiquer délais, vérifier compatibilité avec l'enveloppe financière et la faisabilité (la mission ESQ n'apparaît pas sur le GANTT).",
    "APS - Avant-Projet Sommaire":
        "Proposer des solutions globales traduisant le programme fonctionnel, présenter dispositions techniques générales, durées prévisionnelles et estimation provisoire du coût des travaux. (min 3 semaines)",
    "APD - Avant-Projet Définitif":
        "Déterminer surfaces détaillées, plans, coupes et façades, principes constructifs, matériaux et installations ; vérifier cohérence technique et économique. (min 6 semaines)",
    "Autorisations Administratives":
        "Après validation APD, rédaction des pièces nécessaires (Permis de Construire / Déclaration Préalable) et suivi de l'instruction administrative.",
    "PRO - Études de Projet":
        "Préciser et décrire les éléments conceptuels, établir coût prévisionnel détaillé et délai global de réalisation. (min 4 semaines)",
    "ACT / AMT":
        "Assistance pour la passation des marchés : préparer la consultation, analyser les offres, vérifier conformité technique et financière.",
    "DCE":
        "Dossier de Consultation des Entreprises fourni par la maîtrise d’œuvre contenant les pièces nécessaires à la consultation.",
    "EXE":
        "Études d'exécution : documents et suivi technique pour réaliser l'ouvrage, mise à jour du calendrier par lots.",
    "AOR":
        "Assistance aux opérations de réception : suivi des réserves, validation des DOE et gestion des désordres en période de GPA."
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
# Bandeaux catégories (toujours affichés — séparés du Gantt)
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
    st.stop()  # arrête la suite tant qu'aucun choix
else:
    # --------------------
    # Champ Recherche de financement (case modifiable en début)
    st.subheader("💶 Recherche de financement")
    col_f1, col_f2 = st.columns([2,1])
    with col_f1:
        recherche_financement_weeks = st.number_input(
            "Durée Recherche de financement (semaines) — modifiable",
            min_value=0, value=6, key="financement_weeks"
        )
    with col_f2:
        include_financement = st.checkbox("Inclure la recherche de financement dans le Gantt", value=True)

    # --------------------
    # Date de début commune
    start_date = st.date_input("📅 Date de début du projet", key="date_debut")
    st.markdown("Durées exprimées en **semaines** (valeurs modifiables).")

    phases = []

    # --------------------
    # --- Audit / Études préalables ---
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique", "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)"]:
        with st.expander("📋 Études préalables", expanded=True):
            phases_audit = []
            if etat == "Nous n'avons pas encore effectué d'audit énergétique":
                # Rédaction du programme (si pas d'audit préalable) : demandé
                phases_audit += [
                    {"nom":"📝 Rédaction du programme (si pas d'audit préalable)", "duree":3, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                    {"nom":"📝 Analyse du site: faisabilité, diagnostics et audit énergétique", "duree":20, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                    {"nom":"📝 Restitution de l'audit énergétique", "duree":2, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                ]
            else:
                # si audit déjà reçu, on ne propose pas la rédaction du programme "si pas d'audit"
                phases_audit += [
                    {"nom":"📝 Analyse des comptes-rendus d'audits", "duree":2, "modifiable":True, "delai_mo":0, "groupe":"Études préalables"},
                ]

            # Étapes fixes audit (toujours visibles si choix 1 ou 2)
            phases_audit += [
                {"nom":"📝 Prise de décision des élus", "duree":0, "modifiable":False, "delai_mo":6, "groupe":"Études préalables"},
                {"nom":"📝 Rédaction du programme de travaux et validation", "duree":4, "modifiable":True, "delai_mo":2, "groupe":"Études préalables"},
            ]

            # Inputs (avec key uniques)
            for idx, phase in enumerate(phases_audit):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.write(phase["nom"])
                        # tooltip explanation inline: show small info icon linking to glossaire if available
                        # (we keep full glossary as table below)
                    with col2:
                        phase["duree"] = st.number_input(
                            "semaines",
                            min_value=0 if phase["nom"].startswith("📝 Prise") and phase["duree"]==0 else 1,
                            value=phase["duree"],
                            key=f"audit_{idx}_{phase['nom']}"
                        )
            phases += phases_audit

    # --------------------
    # --- Sélection d'un MOE (Recrutement) ---
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
    # --- MOE / Loi MOP ---
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
                "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]:
        with st.expander("🏗️ MOE (Loi MOP)", expanded=True):
            phases_mop = [
                {"nom":"DIAG - Diagnostic & Études d’Esquisse", "duree":4, "modifiable":True, "delai_mo":2, "groupe":"MOE"},
                {"nom":"ESQ - Esquisse (non affichée sur le GANTT)", "duree":0, "modifiable":False, "delai_mo":0, "groupe":"MOE"},
                {"nom":"APS - Avant-Projet Sommaire", "duree":4, "modifiable":True, "delai_mo":2, "groupe":"MOE"},
                {"nom":"APD - Avant-Projet Définitif", "duree":8, "modifiable":True, "delai_mo":3, "groupe":"MOE"},
                {"nom":"Autorisations Administratives (PC/DP)", "duree":2, "modifiable":True, "delai_mo":2, "groupe":"MOE"},
                {"nom":"PRO - Études de Projet", "duree":6, "modifiable":True, "delai_mo":3, "groupe":"MOE"},
                {"nom":"DCE - Dossier de Consultation des Entreprises", "duree":6, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
                {"nom":"ACT - Assistance passation marchés", "duree":2, "modifiable":True, "delai_mo":1, "groupe":"MOE"},
                {"nom":"VISA - Visa Etudes d’Exécution", "duree":1, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
                {"nom":"DET - Direction Exécution Travaux", "duree":8, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
                {"nom":"AOR - Assistance aux opérations de réception", "duree":4, "modifiable":True, "delai_mo":0, "groupe":"MOE"},
            ]

            # Inputs with minimum constraints for APS/APD/PRO
            for idx, phase in enumerate(phases_mop):
                if phase["modifiable"]:
                    col1, col2 = st.columns([3,1])
                    with col1:
                        # prefix icon for chantier phases
                        label = phase["nom"]
                        st.write(label)
                    with col2:
                        # apply planchers
                        min_val = 1
                        if phase["nom"].startswith("APS"):
                            min_val = 3
                        if phase["nom"].startswith("APD"):
                            min_val = 6
                        if phase["nom"].startswith("PRO"):
                            min_val = 4
                        # allow DCE/others min 1
                        phase["duree"] = st.number_input(
                            "semaines",
                            min_value=min_val,
                            value=phase["duree"],
                            key=f"mop_{idx}_{phase['nom']}"
                        )
            phases += phases_mop

    st.divider()

    # --------------------
    # Vigilance pour DET / AOR (encart)
    st.warning(
        "Vigilance (DET / AOR) : Les délais DET / AOR sont indicatifs et peuvent évoluer en fonction de la disponibilité des entreprises, des matériaux, des équipes MOE ou d'aléas de chantier."
    )

    # --------------------
    # Génération du diagramme
    if st.button("Générer le diagramme de Gantt"):
        tasks = []
        current_start = pd.to_datetime(start_date)

        # construire les tâches (phase + délai MO si applicable)
        for phase in phases:
            # ESQ has durée 0 and shouldn't be added to Gantt (per note)
            if phase["nom"].startswith("ESQ"):
                continue
            start = current_start
            end = start + timedelta(weeks=phase["duree"])
            # customdata pour hover (glossaire)
            brief_def = GLOSSAIRE.get(phase["nom"].split(" - ")[0], "")
            tasks.append(dict(Task=phase["nom"], Start=start, Finish=end, Type='Phase', Groupe=phase["groupe"], Definition=brief_def))
            if phase.get("delai_mo", 0) > 0:
                delay_start = end
                delay_end = delay_start + timedelta(weeks=phase["delai_mo"])
                tasks.append(dict(Task=phase["nom"] + " (délai MO)", Start=delay_start, Finish=delay_end, Type='Délai MO', Groupe=phase["groupe"], Definition=brief_def))
            current_start = end + timedelta(weeks=phase.get("delai_mo", 0))

        # ajouter la recherche de financement en tant que tâche modifiable au début si coché
        if include_financement:
            fin_start = pd.to_datetime(start_date)
            fin_end = fin_start + timedelta(weeks=recherche_financement_weeks)
            tasks.insert(0, dict(Task="💶 Recherche de financement", Start=fin_start, Finish=fin_end, Type="Financement", Groupe="Financement", Definition="Recherche et montage des financements (subventions, prêts, etc.)."))

        # DataFrame
        df = pd.DataFrame(tasks)
        if df.empty:
            st.info("Aucune phase à afficher.")
            st.stop()

        # Pour hover customdata : on fournit la définition et la durée en semaines
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"].fillna("") + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"

        # Plotly timeline
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Type",
            custom_data=["hover_def", "Groupe"],
            color_discrete_map={"Phase": "#0915a6", "Délai MO": "#ff5300", "Financement": "green"}
        )

        # hovertemplate : nom + définition/glossaire + groupe
        fig.update_traces(
            hovertemplate="%{y}<br>%{customdata[0]}<br>Catégorie: %{customdata[1]}<extra></extra>",
            marker_line_width=1,
            marker_line_color='black'
        )

        # inverser l'axe y pour que le début soit en haut
        fig.update_yaxes(autorange="reversed")

        # Grille/repères et unité de temps dans le titre de l'axe
        fig.update_layout(
            height=900,
            width=1400,
            margin=dict(l=50, r=50, t=120, b=80),
            title=dict(text="📅 Diagramme de Gantt du projet — unités : semaines", font=dict(size=18, color="#0915a6")),
            xaxis=dict(tickfont=dict(size=14), title="Date (unités : semaines)"),
            yaxis=dict(tickfont=dict(size=12), title="Phases"),
            plot_bgcolor="white"
        )
        # afficher une grille verticale légère pour repères temporels
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

        # ➕ Bandeaux de catégories (au-dessus du graphe) — ajout via annotations (visuels séparés)
        # calculer min/max global pour positionnement
        global_start = df["Start"].min()
        global_end = df["Finish"].max()
        groups_to_show = ["Études préalables", "Sélection MOE", "MOE", "Financement"]
        color_map_group = {"Études préalables": "#cfe3ff", "Sélection MOE": "#ffe5cc", "MOE": "#e6ccff", "Financement": "#d6f5d6"}
        y_top = len(df["Task"].unique()) + 1.2

        # ajouter rectangles via shapes (positionnées au-dessus via yref='paper')
        shapes = []
        annotations = []
        # pour chaque groupe, calculer min/max si présent
        for grp in groups_to_show:
            grp_df = df[df["Groupe"] == grp]
            if grp_df.empty:
                continue
            s = grp_df["Start"].min()
            f = grp_df["Finish"].max()
            shapes.append(dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=s,
                x1=f,
                y0=1.02,  # au-dessus du plot (paper coordinates)
                y1=1.08,
                fillcolor=color_map_group.get(grp, "#dddddd"),
                line=dict(width=0),
                opacity=0.8
            ))
            # annotation centered
            annotations.append(dict(
                x=s + (f - s) / 2,
                y=1.095,
                xref="x",
                yref="paper",
                text=f"<b>{grp}</b>",
                showarrow=False,
                align="center",
                font=dict(size=12, color="black")
            ))

        fig.update_layout(shapes=shapes, annotations=annotations)

        # ➕ Ligne verticale + € (annotation) entre Études préalables et Sélection MOE
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

        # afficher le Gantt
        st.plotly_chart(fig, use_container_width=True)

        # --------------------
        # Glossaire - tableau en dessous (Option B: survol + tableau)
        st.markdown("### 📚 Glossaire des phases")
        gloss_df = pd.DataFrame([{"Phase": k, "Définition": v} for k, v in GLOSSAIRE.items()])
        st.dataframe(gloss_df, use_container_width=True)

        # --------------------
        # Encadré vigilance déjà affiché plus haut ; répéter ou développer si besoin
        st.info("Note : les durées indiquées sont des estimations en semaines. Les planchers (APS/APD/PRO) sont imposés : APS ≥ 3, APD ≥ 6, PRO ≥ 4 semaines.")
        st.success("Export possible : prends une capture ou intègre un export personnalisé si nécessaire.")
