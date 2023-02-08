import unittest
import pandas as pd
import sys
sys.path.insert(1, 'app')
from analyser import analyser

class TestAnnalyser(unittest.TestCase):
    mocks = pd.read_csv("tests/mocks.csv", dtype={'metier': "string", 'identifiant': "string", 'competences': "string", 'date': "datetime64[ns]"})

    def test_grp_metier(self):
        ''' Test la fonction grp_metier(data) => est une instance de DataFrame, le DataFrame de retour possède 1 seul colonne, le DataFrame de retour possède 29 lignes '''
        df = analyser.grp_metier(self.mocks)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.columns), 1)
        self.assertEqual(len(df), 29)

    def test_mediane(self):
        ''' Test la fonction mediane(data, colname, f=False) => est une instance de int, le int de retour à pour valeur 43 '''
        result = analyser.grp_metier(self.mocks)
        median = analyser.mediane(result, 'nb_ligne')
        self.assertIsInstance(median, int)
        self.assertEqual(median, 43)

    def test_equilibre_data(self):
        ''' Test la fonction equilibre_data(data) => est une instance de DataFrame, le DataFrame de retour possède 3 seul colonne, le DataFrame de retour possède 1553 lignes '''
        data = analyser.equilibre_data(self.mocks)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data.columns), 3)
        self.assertEqual(len(data), 1553)

    def test_competences_occurences(self):
        ''' Test la fonction competences_occurences(data, nb=15, metier=metier) => est une instance de DataFrame, le DataFrame de retour possède 15 lignes '''
        data = analyser.competences_occurences(analyser.equilibre_data(self.mocks), metier='développeur informatique')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 15)

    def test_metier_competences(self):
        ''' Test la fonction metier_competences(data) => est une instance de DataFrame, le DataFrame de retour possède 2 colonnes '''
        data = analyser.metier_competences(analyser.equilibre_data(self.mocks))
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data.columns), 2)

    def test_tf_idf(self):
        ''' Test la fonction tf_idf(data, metier) => est une instance de DataFrame, le DataFrame de retour possède 2 colonnes, la colonne tfidf de la premiere ligne à pour valeur 0 pour le DataFarme de retour '''
        data = analyser.tf_idf(analyser.equilibre_data(self.mocks), 'développeur informatique')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data.columns), 2)
        self.assertEqual(data.iloc[0]['tfidf'], 0)

if __name__ == '__main__' :
    unittest.main()