"""
Tests pour la configuration et les constantes.
"""

import pytest
from config import GLOSSAIRE, GLOSSAIRE_COMPLET, LOGO_BASE64


class TestGlossaire:
    """Tests pour les glossaires."""
    
    def test_glossaire_non_vide(self):
        """Test que le glossaire n'est pas vide."""
        assert len(GLOSSAIRE) > 0
        
    def test_glossaire_complet_non_vide(self):
        """Test que le glossaire complet n'est pas vide."""
        assert len(GLOSSAIRE_COMPLET) > 0
        
    def test_glossaire_cles_presentes(self):
        """Test que les clés attendues sont présentes dans le glossaire."""
        cles_attendues = ["DIAG", "ESQ", "APS", "APD", "PRO", "ACT / AMT", "DCE", "EXE", "AOR"]
        
        for cle in cles_attendues:
            assert cle in GLOSSAIRE
            assert cle in GLOSSAIRE_COMPLET
            
    def test_glossaire_valeurs_non_vides(self):
        """Test que les valeurs du glossaire ne sont pas vides."""
        for cle, valeur in GLOSSAIRE.items():
            assert valeur != ""
            assert len(valeur) > 0
            
    def test_glossaire_complet_valeurs_non_vides(self):
        """Test que les valeurs du glossaire complet ne sont pas vides."""
        for cle, valeur in GLOSSAIRE_COMPLET.items():
            assert valeur != ""
            assert len(valeur) > 0
            
    def test_glossaire_complet_plus_detaille(self):
        """Test que le glossaire complet est plus détaillé que le glossaire simple."""
        for cle in GLOSSAIRE:
            if cle in GLOSSAIRE_COMPLET:
                assert len(GLOSSAIRE_COMPLET[cle]) >= len(GLOSSAIRE[cle])


class TestLogo:
    """Tests pour le logo."""
    
    def test_logo_base64_non_vide(self):
        """Test que le logo en base64 n'est pas vide."""
        assert LOGO_BASE64 != ""
        assert len(LOGO_BASE64) > 0
        
    def test_logo_base64_format_valide(self):
        """Test que le logo en base64 a un format valide."""
        # Vérifier que la chaîne est en base64
        import base64
        import binascii
        
        # Le logo doit être une chaîne base64 valide
        try:
            # Décoder pour vérifier le format
            base64.b64decode(LOGO_BASE64)
        except binascii.Error:
            pytest.fail("Le logo en base64 n'est pas valide")


class TestAutres:
    """Autres tests de configuration."""
    
    def test_glossaire_cles_uniques(self):
        """Test que les clés du glossaire sont uniques."""
        cles = list(GLOSSAIRE.keys())
        assert len(cles) == len(set(cles))
        
    def test_glossaire_complet_cles_uniques(self):
        """Test que les clés du glossaire complet sont uniques."""
        cles = list(GLOSSAIRE_COMPLET.keys())
        assert len(cles) == len(set(cles))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
