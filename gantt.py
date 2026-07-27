"""
Module pour la génération du diagramme de Gantt.
"""

import pandas as pd
from datetime import timedelta
import plotly.express as px
from config import GLOSSAIRE, GLOSSAIRE_COMPLET


def generer_phases(etat, include_financement=True, recherche_financement_weeks=6):
    """
    Génère la liste des phases en fonction de l'état du projet.
    
    Args:
        etat (str): État actuel du projet
        include_financement (bool): Inclure la phase de financement
        recherche_financement_weeks (int): Durée de la recherche de financement
        
    Returns:
        list: Liste des phases avec leurs propriétés
    """
    phases = []
    
    # Études préalables
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique", 
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)"]:
        phases_audit = []
        if etat == "Nous n'avons pas encore effectué d'audit énergétique":
            phases_audit += [
                {"nom": "📝 Rédaction du programme (si pas d'audit préalable)", "duree": 3, "modifiable": True, "delai_mo": 0, "groupe": "Études préalables"},
                {"nom": "📝 Analyse du site: faisabilité, diagnostics et audit énergétique", "duree": 20, "modifiable": True, "delai_mo": 0, "groupe": "Études préalables"},
                {"nom": "📝 Restitution de l'audit énergétique", "duree": 2, "modifiable": True, "delai_mo": 0, "groupe": "Études préalables"},
            ]
        else:
            phases_audit += [
                {"nom": "📝 Analyse des comptes-rendus d'audits", "duree": 2, "modifiable": True, "delai_mo": 0, "groupe": "Études préalables"},
            ]
        phases_audit += [
            {"nom": "📝 Prise de décision des élus", "duree": 0, "modifiable": False, "delai_mo": 6, "groupe": "Études préalables"},
            {"nom": "📝 Rédaction du programme de travaux et validation", "duree": 4, "modifiable": True, "delai_mo": 2, "groupe": "Études préalables"},
        ]
        phases += phases_audit
    
    # AMO PROGRAMMISTE
    if etat in [
        "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
        "Nous souhaitons faire intervenir un AMO Programmiste"
    ]:
        phases_amo = [
            {"nom": "🏢 Choix de l'AMO Programmiste", "duree": 6, "modifiable": True, "groupe": "AMO"},
            {"nom": "🏢 Déroulement AMO et analyse CR", "duree": 8, "modifiable": True, "groupe": "AMO"},
        ]
        phases += phases_amo
    
    # Sélection MOE
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre"]:
        phases_recrut = [
            {"nom": "📝 Rédaction des cahiers des charges et lancement du marché", "duree": 8, "modifiable": True, "delai_mo": 0, "groupe": "Sélection MOE"},
            {"nom": "📝 Publication, analyse du marché et sélection de la MOE", "duree": 8, "modifiable": True, "delai_mo": 0, "groupe": "Sélection MOE"},
            {"nom": "📝 Commission d'appel d'offres", "duree": 2, "modifiable": True, "delai_mo": 0, "groupe": "Sélection MOE"},
            {"nom": "📝 Signature des marchés", "duree": 1, "modifiable": True, "delai_mo": 0, "groupe": "Sélection MOE"},
        ]
        phases += phases_recrut
    
    # MOE / Loi MOP
    if etat in ["Nous n'avons pas encore effectué d'audit énergétique",
                "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)",
                "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre",
                "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"]:
        phases_mop = [
            {"nom": "📝 DIAG - Diagnostic & Études d'Esquisse", "duree": 4, "modifiable": True, "delai_mo": 2, "groupe": "MOE"},
            {"nom": "📝 ESQ - Esquisse (non affichée sur le GANTT)", "duree": 0, "modifiable": False, "delai_mo": 0, "groupe": "MOE"},
            {"nom": "📝 APS - Avant-Projet Sommaire", "duree": 4, "modifiable": True, "delai_mo": 2, "groupe": "MOE"},
            {"nom": "📝 APD - Avant-Projet Définitif", "duree": 8, "modifiable": True, "delai_mo": 3, "groupe": "MOE"},
            {"nom": "📝 Constitution Dossier Autorisation", "duree": 2, "modifiable": True, "delai_mo": 2, "groupe": "MOE"},
            {"nom": "📝 PRO - Études de Projet", "duree": 6, "modifiable": True, "delai_mo": 3, "groupe": "MOE"},
            {"nom": "📝 DCE - Études de Projet", "duree": 6, "modifiable": True, "delai_mo": 3, "groupe": "MOE"},
            {"nom": "📝 ACT - Assistance passation marchés", "duree": 2, "modifiable": True, "delai_mo": 1, "groupe": "MOE"},
            {"nom": "📝 VISA - Visa Études d'Exécution", "duree": 1, "modifiable": True, "delai_mo": 0, "groupe": "MOE"},
            {"nom": "🏗️ DET - Direction Exécution Travaux", "duree": 8, "modifiable": True, "delai_mo": 0, "groupe": "MOE"},
            {"nom": "🏳️‍🌈 AOR - Assistance aux opérations de réception", "duree": 4, "modifiable": True, "delai_mo": 0, "groupe": "MOE"},
        ]
        phases += phases_mop
    
    return phases


def generer_taches(phases, start_date, include_financement=True, recherche_financement_weeks=6):
    """
    Génère les tâches pour le diagramme de Gantt.
    
    Args:
        phases (list): Liste des phases
        start_date (datetime): Date de début du projet
        include_financement (bool): Inclure la phase de financement
        recherche_financement_weeks (int): Durée de la recherche de financement
        
    Returns:
        pd.DataFrame: DataFrame contenant les tâches
    """
    try:
        tasks = []
        current_start = pd.to_datetime(start_date)
        
        # Recherche de financement
        if include_financement:
            fin_start = current_start
            fin_end = fin_start + timedelta(weeks=recherche_financement_weeks)
            tasks.append(dict(
                Task="💰 Recherche de financement", 
                Start=fin_start, 
                Finish=fin_end,
                Type="Financement", 
                Groupe="Financement", 
                Definition="Recherche et montage des financements (subventions, prêts, etc.)."
            ))
        
        # Ajouter les phases
        for phase in phases:
            if phase["nom"].startswith("ESQ"):
                continue  # n'apparaît pas sur le Gantt
            
            start = current_start
            dur = phase["duree"]
            delay = phase.get("delai_mo", 0)
            end_phase = start + timedelta(weeks=dur)
            
            tasks.append(dict(
                Task=phase["nom"], 
                Start=start, 
                Finish=end_phase,
                Type='Phase', 
                Groupe=phase["groupe"], 
                Definition=GLOSSAIRE.get(phase["nom"].split(" - ")[0], "")
            ))
            
            if delay > 0:
                end_delay = end_phase + timedelta(weeks=delay)
                tasks.append(dict(
                    Task=phase["nom"], 
                    Start=end_phase, 
                    Finish=end_delay,
                    Type='Délai MO', 
                    Groupe=phase["groupe"], 
                    Definition=GLOSSAIRE.get(phase["nom"].split(" - ")[0], "")
                ))
                current_start = end_delay
            else:
                current_start = end_phase
        
        df = pd.DataFrame(tasks)
        
        if df.empty:
            return None
        
        # Calculer la durée en semaines
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"].fillna("") + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        return df
        
    except Exception as e:
        raise ValueError(f"Erreur lors de la génération des tâches: {str(e)}")


def generer_figure_gantt(df):
    """
    Génère la figure Plotly pour le diagramme de Gantt.
    
    Args:
        df (pd.DataFrame): DataFrame contenant les tâches
        
    Returns:
        plotly.graph_objects.Figure: Figure du Gantt
    """
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame vide ou None")
        
        fig = px.timeline(
            df, 
            x_start="Start", 
            x_end="Finish", 
            y="Task", 
            color="Type",
            custom_data=["hover_def", "Groupe"],
            color_discrete_map={"Phase": "#0915a6", "Délai MO": "#ff5300", "Financement": "green"}
        )
        
        fig.update_traces(
            hovertemplate="%{y}<br>%{customdata[0]}<br>Catégorie: %{customdata[1]}<extra></extra>",
            marker_line_width=1, 
            marker_line_color='black'
        )
        
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            height=900, 
            width=1400,
            margin=dict(l=50, r=50, t=120, b=80),
            title=dict(text="📅 Diagramme de Gantt du projet — unités : semaines", font=dict(size=18, color="#0915a6")),
            xaxis=dict(tickfont=dict(size=14), title="Date"),
            yaxis=dict(tickfont=dict(size=12), title="Phases"),
            plot_bgcolor="white"
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
        
        # Ajouter les bandeaux catégories
        groups_to_show = ["Études préalables", "Sélection MOE", "MOE", "Financement"]
        color_map_group = {
            "Études préalables": "#cfe3ff", 
            "Sélection MOE": "#ffe5cc", 
            "MOE": "#e6ccff", 
            "Financement": "#d6f5d6"
        }
        
        shapes = []
        annotations = []
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
                y0=1.02, 
                y1=1.08,
                fillcolor=color_map_group.get(grp, "#dddddd"), 
                line=dict(width=0), 
                opacity=0.8
            ))
            annotations.append(dict(
                x=s + (f-s)/2, 
                y=1.095, 
                xref="x", 
                yref="paper",
                text=f"<b>{grp}</b>", 
                showarrow=False, 
                align="center", 
                font=dict(size=12, color="black")
            ))
        
        fig.update_layout(shapes=shapes, annotations=annotations)
        
        return fig
        
    except Exception as e:
        raise ValueError(f"Erreur lors de la génération de la figure: {str(e)}")
