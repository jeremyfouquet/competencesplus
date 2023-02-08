import unittest
import pandas as pd
import sys
sys.path.insert(1, 'app')
from extraire import extraire

class TestExtraire(unittest.TestCase):

    def test_charger_page_urls(self):
        urls = extraire.charger_page_urls()
        self.assertIsInstance(urls, list)
        self.assertEqual(len(urls), 30)

    def test_charger_liste_metiers(self):
        urls = extraire.charger_page_urls()
        sources = extraire.charger_liste_metiers(urls[0], 2)
        self.assertIsInstance(sources, list)
        self.assertEqual(len(sources), 2)

    def test_decoder_attributs(self):
        urls = extraire.charger_page_urls()
        sources = extraire.charger_liste_metiers(urls[0], 2)
        data = extraire.decoder_attributs(sources[0])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)

    def test_normalisation(self):
        sentences = extraire.normalisation('tests (A) etc B/C D-E, ...')
        self.assertEqual(sentences, 'test a b c d e .')

    def test_nettoyer_data(self):
        df = pd.DataFrame({'metier': ['Test', 'Test', 'Test', 'Test', 'Test'], 'identifiant': ['1', '1', '1', '2', '3'], 'competences': ['Analyser les besoins du clients', 'Analyser les besoins du clients', 'Analyser les besoins du clients', 'Analyser les besoins du clients', None], 'savoir-etre': ['Travail en équipe', 'Travail en équipe', 'Travail en équipe', 'Travail en équipe', None]})
        data = extraire.nettoyer_data(df)
        print(data)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data.columns), 3)
        self.assertEqual(data.iloc[0]['competences'], 'analyser le besoin de client . travail en équipe')

    def test_nettoyer_data(self):
        df = pd.DataFrame({'metier': ['Test', 'Test', 'Test', 'Test', 'Test'], 'identifiant': ['1', '1', '1', '2', '3'], 'competences': ['Analyser les besoins du clients', 'Analyser les besoins du clients', 'Analyser les besoins du clients', 'Analyser les besoins du clients', None], 'savoir-etre': ['Travail en équipe', 'Travail en équipe', 'Travail en équipe', 'Travail en équipe', None]})
        data = extraire.nettoyer_data(df)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data.columns), 3)
        self.assertEqual(data.iloc[0]['competences'], 'analyser le besoin de client . travail en équipe')

if __name__ == '__main__' :
    unittest.main()