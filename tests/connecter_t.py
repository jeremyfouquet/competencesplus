import unittest
import pandas as pd
import sys
sys.path.insert(1, 'app')
from connecter import connecter

class TestConnecter(unittest.TestCase):

    def test_connecter_bdd(self):
        ''' Test la fonction connecter_bdd() => le statut du retour est égal à 1 '''
        conn = connecter.connecter_bdd()
        self.assertEqual(conn.status, 1)

    def test_charger_bdd_ou_csv(self):
        ''' Test la fonction charger_bdd_ou_csv() => est une instance de DataFrame, le DataFrame de retour possède 4 colonnes '''
        df = connecter.charger_bdd_ou_csv()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.columns), 4)

if __name__ == '__main__' :
    unittest.main()