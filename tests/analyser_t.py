import unittest
import pandas as pd
import sys
sys.path.insert(1, 'app')
from analyser import analyser

class TestAnnalyser(unittest.TestCase):
    mocks = pd.read_csv("tests/mocks.csv", dtype={'metier': "string", 'identifiant': "string", 'competences': "string", 'date': "datetime64[ns]"})
    '''
    def setUp(self):
        global data
        data = connecter.charger_bdd_ou_csv()

    def tearDown(self):
        global data
        del data
    '''
    def test_grp_metier(self):
        df = analyser.grp_metier(self.mocks)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.columns), 1)
        self.assertEqual(len(df), 29)

    def test_mediane(self):
        result = analyser.grp_metier(self.mocks)
        median = analyser.mediane(result, 'nb_ligne')
        self.assertEqual(median, 43)

    def test_equilibre_data(self):
        data = analyser.equilibre_data(self.mocks)
        self.assertEqual(len(data.columns), 3)
        self.assertEqual(len(data), 1553)

    def test_competences_occurences(self):
        data = analyser.competences_occurences(analyser.equilibre_data(self.mocks), metier='développeur informatique')
        self.assertEqual(len(data), 15)

    def test_metier_competences(self):
        data = analyser.metier_competences(analyser.equilibre_data(self.mocks))
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data.columns), 2)

    def test_tf_idf(self):
        data = analyser.tf_idf(analyser.equilibre_data(self.mocks), 'développeur informatique')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data.columns), 2)
        self.assertEqual(data.iloc[0]['tfidf'], 0)

if __name__ == '__main__' :
    unittest.main()