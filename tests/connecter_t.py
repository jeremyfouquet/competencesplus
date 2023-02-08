import unittest
import pandas as pd
import sys
sys.path.insert(1, 'app')
from connecter import connecter

class TestConnecter(unittest.TestCase):

    def test_connecter_bdd(self):
        conn = connecter.connecter_bdd()
        self.assertEqual(conn.status, 1)

    def test_charger_bdd_ou_csv(self):
        df = connecter.charger_bdd_ou_csv()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.columns), 4)

if __name__ == '__main__' :
    unittest.main()