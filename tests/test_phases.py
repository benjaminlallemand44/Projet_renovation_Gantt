"""
Tests pour la génération des phases.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from gantt import generer_phases, generer_taches


class TestGenererPhases:
    """Tests pour la fonction generer_phases."""
    
    def test_etat_audit_non_effectue(self):
        """Test la génération des phases pour l'état 'audit non effectué'."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        
        # Vérifier que les phases d'audit sont présentes
        noms_phases = [p["nom"] for p in phases]
        assert any("Rédaction du programme" in nom for nom in noms_phases)
        assert any("Analyse du site" in nom for nom in noms_phases)
        assert any("Restitution de l'audit" in nom for nom in noms_phases)
        
        # Vérifier les groupes
        groupes = {p["groupe"] for p in phases}
        assert "Études préalables" in groupes
        assert "Sélection MOE" in groupes
        assert "MOE" in groupes
        
    def test_etat_audit_effectue(self):
        """Test la génération des phases pour l'état 'audit effectué'."""
        etat = "Nous venons de recevoir les comptes rendus des études préalables (dont l'audit énergétique)"
        phases = generer_phases(etat)
        
        # Vérifier que l'analyse des comptes-rendus est présente
        noms_phases = [p["nom"] for p in phases]
        assert any("Analyse des comptes-rendus" in nom for nom in noms_phases)
        
        # Vérifier les groupes
        groupes = {p["groupe"] for p in phases}
        assert "Études préalables" in groupes
        assert "AMO" in groupes
        assert "Sélection MOE" in groupes
        assert "MOE" in groupes
        
    def test_etat_amo_programmiste(self):
        """Test la génération des phases pour l'état 'AMO Programmiste'."""
        etat = "Nous souhaitons faire intervenir un AMO Programmiste"
        phases = generer_phases(etat)
        
        # Vérifier que les phases AMO sont présentes
        noms_phases = [p["nom"] for p in phases]
        assert any("Choix de l'AMO" in nom for nom in noms_phases)
        assert any("Déroulement AMO" in nom for nom in noms_phases)
        
        # Vérifier les groupes
        groupes = {p["groupe"] for p in phases}
        assert "AMO" in groupes
        
    def test_etat_selection_moe(self):
        """Test la génération des phases pour l'état 'Sélection MOE'."""
        etat = "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre"
        phases = generer_phases(etat)
        
        # Vérifier que les phases de sélection MOE sont présentes
        noms_phases = [p["nom"] for p in phases]
        assert any("Rédaction des cahiers" in nom for nom in noms_phases)
        assert any("Publication" in nom for nom in noms_phases)
        assert any("Commission d'appel" in nom for nom in noms_phases)
        assert any("Signature des marchés" in nom for nom in noms_phases)
        
    def test_etat_equipe_selectionnee(self):
        """Test la génération des phases pour l'état 'équipe sélectionnée'."""
        etat = "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"
        phases = generer_phases(etat)
        
        # Vérifier que les phases MOE sont présentes
        noms_phases = [p["nom"] for p in phases]
        assert any("DIAG" in nom for nom in noms_phases)
        assert any("APS" in nom for nom in noms_phases)
        assert any("APD" in nom for nom in noms_phases)
        assert any("PRO" in nom for nom in noms_phases)
        assert any("DCE" in nom for nom in noms_phases)
        assert any("ACT" in nom for nom in noms_phases)
        assert any("DET" in nom for nom in noms_phases)
        assert any("AOR" in nom for nom in noms_phases)
        
    def test_phases_modifiables(self):
        """Test que les phases ont bien l'attribut modifiable."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        
        # Vérifier que certaines phases sont modifiables
        phases_modifiables = [p for p in phases if p["modifiable"]]
        assert len(phases_modifiables) > 0
        
        # Vérifier que certaines phases ne sont pas modifiables
        phases_non_modifiables = [p for p in phases if not p["modifiable"]]
        assert len(phases_non_modifiables) > 0
        
    def test_delais_mo(self):
        """Test que les délais MO sont correctement définis."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        
        # Vérifier que certaines phases ont des délais MO
        phases_avec_delai = [p for p in phases if p.get("delai_mo", 0) > 0]
        assert len(phases_avec_delai) > 0


class TestGenererTaches:
    """Tests pour la fonction generer_taches."""
    
    def test_generation_taches_valide(self):
        """Test la génération des tâches avec des phases valides."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que le DataFrame n'est pas vide
        assert df is not None
        assert not df.empty
        
        # Vérifier les colonnes
        colonnes_attendues = ["Task", "Start", "Finish", "Type", "Groupe", "Definition", "Duration_weeks", "hover_def"]
        for col in colonnes_attendues:
            assert col in df.columns
        
    def test_generation_taches_avec_financement(self):
        """Test la génération des tâches avec financement."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date, include_financement=True, recherche_financement_weeks=8)
        
        # Vérifier que la tâche de financement est présente
        taches = df["Task"].tolist()
        assert any("Recherche de financement" in tache for tache in taches)
        
    def test_generation_taches_sans_financement(self):
        """Test la génération des tâches sans financement."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date, include_financement=False)
        
        # Vérifier que la tâche de financement n'est pas présente
        taches = df["Task"].tolist()
        assert not any("Recherche de financement" in tache for tache in taches)
        
    def test_duree_taches(self):
        """Test que les durées des tâches sont correctement calculées."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que les durées sont positives (sauf pour les tâches avec durée 0)
        assert (df["Duration_weeks"] >= 0).all()
        # Vérifier qu'il y a au moins une tâche avec durée > 0
        assert (df["Duration_weeks"] > 0).any()
        
    def test_ordre_taches(self):
        """Test que les tâches sont dans le bon ordre chronologique."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que les dates de début sont dans l'ordre
        starts = pd.to_datetime(df["Start"])
        assert (starts.diff().dropna() >= timedelta(0)).all()
        
    def test_taches_esq_exclues(self):
        """Test que les tâches ESQ sont exclues du Gantt."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que les tâches ESQ ne sont pas présentes
        taches = df["Task"].tolist()
        # Filtrer les tâches qui commencent par ESQ (pas juste qui contiennent ESQ)
        taches_esq = [tache for tache in taches if tache.startswith("ESQ")]
        assert len(taches_esq) == 0
        
    def test_delais_mo_dans_taches(self):
        """Test que les délais MO sont correctement intégrés."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que des tâches de type 'Délai MO' sont présentes
        types = df["Type"].tolist()
        assert "Délai MO" in types


class TestDecoupageActions:
    """Tests pour le découpage des actions en catégories."""
    
    def test_categorie_etudes_prealables(self):
        """Test le découpage des actions en catégorie 'Études préalables'."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        
        phases_etudes = [p for p in phases if p["groupe"] == "Études préalables"]
        
        # Vérifier que la catégorie contient les bonnes phases
        assert len(phases_etudes) > 0
        noms = [p["nom"] for p in phases_etudes]
        assert any("Rédaction du programme" in nom for nom in noms)
        assert any("Analyse du site" in nom for nom in noms)
        
    def test_categorie_moe(self):
        """Test le découpage des actions en catégorie 'MOE'."""
        etat = "Nous venons de sélectionner notre équipe de maitrise d'oeuvre"
        phases = generer_phases(etat)
        
        phases_moe = [p for p in phases if p["groupe"] == "MOE"]
        
        # Vérifier que la catégorie contient les bonnes phases
        assert len(phases_moe) > 0
        noms = [p["nom"] for p in phases_moe]
        assert any("DIAG" in nom for nom in noms)
        assert any("APS" in nom for nom in noms)
        assert any("APD" in nom for nom in noms)
        
    def test_categorie_selection_moe(self):
        """Test le découpage des actions en catégorie 'Sélection MOE'."""
        etat = "Nous voulons lancer notre marché de recrutement de maîtrise d'oeuvre"
        phases = generer_phases(etat)
        
        phases_selection = [p for p in phases if p["groupe"] == "Sélection MOE"]
        
        # Vérifier que la catégorie contient les bonnes phases
        assert len(phases_selection) > 0
        noms = [p["nom"] for p in phases_selection]
        assert any("Rédaction des cahiers" in nom for nom in noms)
        assert any("Publication" in nom for nom in noms)


class TestFormatGantt:
    """Tests pour le format du Gantt."""
    
    def test_types_taches(self):
        """Test que les types de tâches sont corrects."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date, include_financement=True)
        
        # Vérifier les types de tâches
        types = df["Type"].unique().tolist()
        assert "Phase" in types
        assert "Délai MO" in types
        assert "Financement" in types
        
    def test_groupes_taches(self):
        """Test que les groupes de tâches sont corrects."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date, include_financement=True)
        
        # Vérifier les groupes de tâches
        groupes = df["Groupe"].unique().tolist()
        assert "Études préalables" in groupes
        assert "Sélection MOE" in groupes
        assert "MOE" in groupes
        assert "Financement" in groupes
        
    def test_definitions_taches(self):
        """Test que les définitions des tâches sont présentes."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que les définitions ne sont pas vides
        assert not df["Definition"].isna().all()
        
    def test_hover_def(self):
        """Test que les définitions pour le hover sont correctes."""
        etat = "Nous n'avons pas encore effectué d'audit énergétique"
        phases = generer_phases(etat)
        start_date = datetime(2023, 1, 1)
        
        df = generer_taches(phases, start_date)
        
        # Vérifier que les hover_def contiennent les durées
        assert all("semaines" in str(definition) for definition in df["hover_def"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
