"""
Tests pour la génération du diagramme de Gantt.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from gantt import generer_taches, generer_figure_gantt


class TestGenererFigureGantt:
    """Tests pour la fonction generer_figure_gantt."""
    
    def test_figure_valide(self):
        """Test la génération d'une figure valide."""
        # Créer un DataFrame de test
        data = {
            "Task": ["Tâche 1", "Tâche 2"],
            "Start": [datetime(2023, 1, 1), datetime(2023, 1, 8)],
            "Finish": [datetime(2023, 1, 7), datetime(2023, 1, 14)],
            "Type": ["Phase", "Phase"],
            "Groupe": ["MOE", "MOE"],
            "Definition": ["Définition 1", "Définition 2"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier que la figure a été générée
        assert fig is not None
        
    def test_figure_avec_df_vide(self):
        """Test la génération d'une figure avec un DataFrame vide."""
        df = pd.DataFrame()
        
        # Vérifier que la fonction lève une exception
        with pytest.raises(ValueError, match="DataFrame vide ou None"):
            generer_figure_gantt(df)
            
    def test_figure_avec_df_none(self):
        """Test la génération d'une figure avec un DataFrame None."""
        # Vérifier que la fonction lève une exception
        with pytest.raises(ValueError, match="DataFrame vide ou None"):
            generer_figure_gantt(None)
    
    def test_figure_avec_types_taches(self):
        """Test la génération d'une figure avec différents types de tâches."""
        # Créer un DataFrame avec différents types
        data = {
            "Task": ["Tâche 1", "Tâche 2", "Tâche 3"],
            "Start": [datetime(2023, 1, 1), datetime(2023, 1, 8), datetime(2023, 1, 15)],
            "Finish": [datetime(2023, 1, 7), datetime(2023, 1, 14), datetime(2023, 1, 21)],
            "Type": ["Phase", "Délai MO", "Financement"],
            "Groupe": ["MOE", "MOE", "Financement"],
            "Definition": ["Définition 1", "Définition 2", "Définition 3"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier que la figure a été générée
        assert fig is not None
        
    def test_figure_avec_groupes(self):
        """Test la génération d'une figure avec différents groupes."""
        # Créer un DataFrame avec différents groupes
        data = {
            "Task": ["Tâche 1", "Tâche 2", "Tâche 3", "Tâche 4"],
            "Start": [datetime(2023, 1, 1), datetime(2023, 1, 8), datetime(2023, 1, 15), datetime(2023, 1, 22)],
            "Finish": [datetime(2023, 1, 7), datetime(2023, 1, 14), datetime(2023, 1, 21), datetime(2023, 1, 28)],
            "Type": ["Phase", "Phase", "Phase", "Phase"],
            "Groupe": ["Études préalables", "Sélection MOE", "MOE", "Financement"],
            "Definition": ["Définition 1", "Définition 2", "Définition 3", "Définition 4"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier que la figure a été générée
        assert fig is not None
        
    def test_figure_layout(self):
        """Test que le layout de la figure est correct."""
        # Créer un DataFrame de test
        data = {
            "Task": ["Tâche 1"],
            "Start": [datetime(2023, 1, 1)],
            "Finish": [datetime(2023, 1, 7)],
            "Type": ["Phase"],
            "Groupe": ["MOE"],
            "Definition": ["Définition 1"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier les propriétés du layout
        assert fig.layout.height == 900
        assert fig.layout.width == 1400
        assert fig.layout.title.text == "📅 Diagramme de Gantt du projet — unités : semaines"
        
    def test_figure_axes(self):
        """Test que les axes de la figure sont corrects."""
        # Créer un DataFrame de test
        data = {
            "Task": ["Tâche 1"],
            "Start": [datetime(2023, 1, 1)],
            "Finish": [datetime(2023, 1, 7)],
            "Type": ["Phase"],
            "Groupe": ["MOE"],
            "Definition": ["Définition 1"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier les propriétés des axes
        assert fig.layout.xaxis.title.text == "Date"
        assert fig.layout.yaxis.title.text == "Phases"
        assert fig.layout.yaxis.autorange == "reversed"


class TestIntegration:
    """Tests d'intégration pour le Gantt complet."""
    
    def test_gantt_complet_etat_audit_non_effectue(self):
        """Test la génération complète du Gantt pour l'état 'audit non effectué'."""
        from gantt import generer_phases
        
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date, include_financement=True)
        fig = generer_figure_gantt(df)
        
        # Vérifier que tout a été généré correctement
        assert df is not None
        assert not df.empty
        assert fig is not None
        
    def test_gantt_complet_etat_equipe_selectionnee(self):
        """Test la génération complète du Gantt pour l'état 'équipe sélectionnée'."""
        from gantt import generer_phases
        
        etat = "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date, include_financement=False)
        fig = generer_figure_gantt(df)
        
        # Vérifier que tout a été généré correctement
        assert df is not None
        assert not df.empty
        assert fig is not None
        
        # Vérifier que le financement n'est pas inclus
        taches = df["Task"].tolist()
        assert not any("Recherche de financement" in tache for tache in taches)


class TestCouleursGantt:
    """Tests pour les couleurs du Gantt."""
    
    def test_couleurs_types_taches(self):
        """Test que les couleurs des types de tâches sont correctes."""
        # Créer un DataFrame avec différents types
        data = {
            "Task": ["Tâche Phase", "Tâche Délai MO", "Tâche Financement"],
            "Start": [datetime(2023, 1, 1), datetime(2023, 1, 8), datetime(2023, 1, 15)],
            "Finish": [datetime(2023, 1, 7), datetime(2023, 1, 14), datetime(2023, 1, 21)],
            "Type": ["Phase", "Délai MO", "Financement"],
            "Groupe": ["MOE", "MOE", "Financement"],
            "Definition": ["Définition 1", "Définition 2", "Définition 3"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier que la figure a été générée
        assert fig is not None
        
    def test_couleurs_groupes(self):
        """Test que les couleurs des groupes sont correctes."""
        # Créer un DataFrame avec différents groupes
        data = {
            "Task": ["Tâche 1", "Tâche 2", "Tâche 3", "Tâche 4"],
            "Start": [datetime(2023, 1, 1), datetime(2023, 1, 8), datetime(2023, 1, 15), datetime(2023, 1, 22)],
            "Finish": [datetime(2023, 1, 7), datetime(2023, 1, 14), datetime(2023, 1, 21), datetime(2023, 1, 28)],
            "Type": ["Phase", "Phase", "Phase", "Phase"],
            "Groupe": ["Études préalables", "Sélection MOE", "MOE", "Financement"],
            "Definition": ["Définition 1", "Définition 2", "Définition 3", "Définition 4"]
        }
        df = pd.DataFrame(data)
        df["Duration_weeks"] = (pd.to_datetime(df["Finish"]) - pd.to_datetime(df["Start"])).dt.days / 7
        df["hover_def"] = df["Definition"] + "<br>Durée: " + df["Duration_weeks"].round(1).astype(str) + " semaines"
        
        # Générer la figure
        fig = generer_figure_gantt(df)
        
        # Vérifier que la figure a été générée
        assert fig is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
