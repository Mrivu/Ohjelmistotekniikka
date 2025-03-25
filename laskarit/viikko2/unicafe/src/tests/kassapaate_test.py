import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kassapaate_saa_oikeat_arvot(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_osta_edullinen_kateisella(self):
        maksu = self.kassapaate.syo_edullisesti_kateisella(700)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(maksu, 460)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

        maksu = self.kassapaate.syo_edullisesti_kateisella(100)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(maksu, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
    
    def test_osta_maukas_kateisella(self):
        maksu = self.kassapaate.syo_maukkaasti_kateisella(700)

        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(maksu, 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

        maksu = self.kassapaate.syo_maukkaasti_kateisella(300)

        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(maksu, 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
    
    def test_osta_edullinen_kortilla(self):
        self.maksukortti = Maksukortti(300)
        maksu = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(maksu, True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        maksu = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(maksu, False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_osta_maukas_kortilla(self):
        self.maksukortti = Maksukortti(500)
        maksu = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(maksu, True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        maksu = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(maksu, False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_lataa_rahaa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)
        self.assertEqual(self.maksukortti.saldo, 2000)

        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)
        self.assertEqual(self.maksukortti.saldo, 2000)