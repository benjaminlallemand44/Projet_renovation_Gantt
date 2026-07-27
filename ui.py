"""
Module pour l'interface utilisateur Streamlit.
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from config import LOGO_BASE64, GLOSSAIRE, GLOSSAIRE_COMPLET
from gantt import generer_phases, generer_taches, generer_figure_gantt


def afficher_logo():
    """Affiche le logo en base64."""
    st.markdown(
        f'<img src="data:image/png;base64,{LOGO_BASE64}" width="450">',
        unsafe_allow_html=True
    )


def afficher_titre():
    """Affiche le titre et l'introduction."""
    st.set_page_config(layout="wide")
    st.title("📅 Assistant Planification du Projet de Rénovation")
    st.markdown("""
    Bienvenue dans l'outil de planification de projet de rénovation.  
    Sélectionnez l'état actuel de votre projet et la **date de début**, puis ajustez les durées des phases (en **semaines**) pour générer un diagramme de Gantt interactif et clair.  
    
    Les phases sont organisées par catégories : **Études préalables**, **AMO Programmiste**, **Sélection MOE**, **MOE (Loi MOP)**.
    """)
    st.divider()


def afficher_bandeaux_categories():
    """Affiche les bandeaux des catégories."""
    cat_col1, cat_col2, cat_col3, cat_col4 = st.columns([1, 1, 1, 1])
    
    with cat_col1:
        st.markdown("**🏠 Études préalables**")
    
    with cat_col2:
        st.markdown("**🏢 AMO Programmiste**")
    
    with cat_col3:
        st.markdown("**📋 Sélection MOE**")
    
    with cat_col4:
        st.markdown("**🏗️ MOE (Loi MOP)**")
    
    st.markdown("---")


def selection_etat():
    """
    Affiche le sélecteur d'état du projet.
    
    Returns:
        str: État sélectionné
    """
    etat = st.selectbox(
        "Où en êtes-vous dans votre projet de rénovation énergétique ?",
        ["-- Sélectionnez --",
         "Nous n'avons pas encore effectué d'audit énergétique",
         "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
         "Nous souhaitons faire intervenir un AMO Programmiste",
         "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
         "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]
    )
    return etat


def selection_financement():
    """
    Affiche les options de financement.
    
    Returns:
        tuple: (recherche_financement_weeks, include_financement)
    """
    st.subheader("💰 Recherche de financement")
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f1:
        recherche_financement_weeks = st.number_input(
            "Durée Recherche de financement (semaines) — modifiable",
            min_value=0, 
            value=6, 
            key="financement_weeks"
        )
    
    with col_f2:
        include_financement = st.checkbox("Inclure la recherche de financement dans le Gantt", value=True)
    
    return recherche_financement_weeks, include_financement


def selection_date_debut():
    """
    Affiche le sélecteur de date de début.
    
    Returns:
        datetime: Date de début sélectionnée
    """
    start_date = st.date_input("📅 Date de début du projet", key="date_debut")
    st.markdown("Durées exprimées en **semaines** (valeurs modifiables).")
    return start_date


def afficher_phases_etapes(etat, phases):
    """
    Affiche les sections des phases et permet de modifier les durées.
    
    Args:
        etat (str): État actuel du projet
        phases (list): Liste des phases à afficher
        
    Returns:
        list: Liste des phases avec durées mises à jour
    """
    try:
        # Études préalables
        if etat in ["Nous n'avons pas encore effectué d'audit énergétique", 
                    "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)"]:
            with st.expander("📂 Études préalables", expanded=True):
                for idx, phase in enumerate([p for p in phases if p["groupe"] == "Études préalables"]):
                    if phase["modifiable"]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(phase["nom"])
                        with col2:
                            min_val = 0 if phase["nom"].startswith("📝 Prise") else 1
                            phase["duree"] = st.number_input(
                                "semaines",
                                min_value=min_val,
                                value=phase["duree"],
                                key=f"audit_{idx}_{phase['nom']}"
                            )
        
        # AMO Programmiste
        if etat in [
            "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
            "Nous souhaitons faire intervenir un AMO Programmiste"
        ]:
            with st.expander("🏢 AMO Programmiste", True):
                for i, p in enumerate([p for p in phases if p["groupe"] == "AMO"]):
                    p["duree"] = st.number_input(p["nom"], 1, 52, p["duree"], key=f"amo{i}")
        
        # Sélection MOE
        if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                    "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                    "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre"]:
            with st.expander("📋 Sélection d'une MOE", expanded=True):
                for idx, phase in enumerate([p for p in phases if p["groupe"] == "Sélection MOE"]):
                    if phase["modifiable"]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(phase["nom"])
                        with col2:
                            phase["duree"] = st.number_input(
                                "semaines",
                                min_value=1,
                                value=phase["duree"],
                                key=f"recrut_{idx}_{phase['nom']}"
                            )
        
        # MOE / Loi MOP
        if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                    "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                    "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
                    "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]:
            with st.expander("🏗️ MOE (Loi MOP)", expanded=True):
                for idx, phase in enumerate([p for p in phases if p["groupe"] == "MOE"]):
                    col1, col2 = st.columns([3, 1])
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
        
        return phases
        
    except Exception as e:
        st.error(f"Erreur lors de l'affichage des phases: {str(e)}")
        return phases


def afficher_avertissement():
    """Affiche l'avertissement pour les phases DET/AOR."""
    st.divider()
    st.warning("Vigilance (DET / AOR) : Les délais DET / AOR sont indicatifs et peuvent évoluer selon disponibilité des entreprises, matériaux et équipes MOE.")


def afficher_gantt(df, fig):
    """
    Affiche le diagramme de Gantt.
    
    Args:
        df (pd.DataFrame): DataFrame des tâches
        fig (plotly.graph_objects.Figure): Figure du Gantt
    """
    try:
        if df is None or df.empty:
            st.info("Aucune phase à afficher.")
            return
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur lors de l'affichage du Gantt: {str(e)}")


def main():
    """Fonction principale de l'application."""
    try:
        # Affichage initial
        afficher_logo()
        afficher_titre()
        afficher_bandeaux_categories()
        
        # Sélection de l'état
        etat = selection_etat()
        
        if etat == "-- Sélectionnez --":
            st.info("Sélectionnez votre état du projet pour afficher les étapes.")
            st.stop()
        
        # Sélection des options
        recherche_financement_weeks, include_financement = selection_financement()
        start_date = selection_date_debut()
        
        # Génération des phases
        phases = generer_phases(etat, include_financement, recherche_financement_weeks)
        
        # Affichage et modification des phases
        phases = afficher_phases_etapes(etat, phases)
        
        # Avertissement
        afficher_avertissement()
        
        # Génération et affichage du Gantt
        if st.button("Générer le diagramme de Gantt"):
            try:
                df = generer_taches(phases, start_date, include_financement, recherche_financement_weeks)
                fig = generer_figure_gantt(df)
                afficher_gantt(df, fig)
            except Exception as e:
                st.error(f"Erreur lors de la génération du Gantt: {str(e)}")
        
    except Exception as e:
        st.error(f"Erreur inattendue: {str(e)}")


if __name__ == "__main__":
    main()
