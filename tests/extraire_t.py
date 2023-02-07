import unittest
import sys
sys.path.append('./app')
from extraire import extraire
class TestExtraire(unittest.TestCase):
    def test_charger(self):
        urls = extraire.charger_page_urls()
        print(urls)

if __name__ == '__main__' :
    unittest.main()