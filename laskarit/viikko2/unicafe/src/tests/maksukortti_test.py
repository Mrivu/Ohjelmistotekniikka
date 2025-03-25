import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
    
    def test_rahan_lataus(self):
        self.maksukortti.lataa_rahaa(100)

        self.assertEqual(self.maksukortti.saldo_euroina(), 11.0)
    
    def test_rahan_vähennys(self):
        boolean_result = self.maksukortti.ota_rahaa(100)

        self.assertEqual(self.maksukortti.saldo_euroina(), 9.0)
        self.assertEqual(boolean_result, True)

        boolean_result = self.maksukortti.ota_rahaa(1500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 9.0)
        self.assertEqual(boolean_result, False)
    
    def test_kortin_str_kutsu(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")