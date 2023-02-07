import unittest
import sys
sys.path.append('./app')
from extraire import extraire
class TestExtraire(unittest.TestCase):
    def test_charger(self):
        extraire.charger_page_urls()

if __name__ == '__main__' :
    unittest.main()