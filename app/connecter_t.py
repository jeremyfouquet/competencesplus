import unittest
from connecter import connecter

class TestExtraire(unittest.TestCase):

    def setUp(self):
        print("Avant le test")

    def tearDown(self):
        print("Après le test")

    def test_nettoyer_data(self):
        conn = connecter.connecter_bdd()
        print(type(conn).__name__)
        #self.assertIsInstance(data, pd.DataFrame)
        #self.assertEqual(len(data), 2)
        #self.assertEqual(len(data.columns), 3)
        #self.assertEqual(data.iloc[0]['competences'], 'analyser le besoin de client . travail en équipe')

if __name__ == '__main__' :
    unittest.main()