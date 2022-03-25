import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_syo_edullisesti_kateisella(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kateisella(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_edullisesti_kateisella_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_maukkaasti_kateisella_ei_riita(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(390), 390)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_lataa_rahaa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, (100000+1000))
        self.assertEqual(str(self.kortti), "saldo: 20.0")
    
    def test_lataa_rahaa_kortille_neg(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, (100000))
        self.assertEqual(str(self.kortti), "saldo: 10.0")

    def test_syo_maukkaasti_kortilla(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)
        self.assertEqual(self.kassapaate.maukkaat, 1)    
        self.assertEqual(str(self.kortti), "saldo: 6.0")

    def test_syo_edullisesti_kortilla(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(str(self.kortti), "saldo: 7.6")

    def test_syo_maukkaasti_kortilla_ei_riita(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), False)
        self.assertEqual(self.kassapaate.maukkaat, 2)    
        self.assertEqual(str(self.kortti), "saldo: 2.0")    

    def test_syo_edullisesti_kortilla_ei_riita(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), False)
        self.assertEqual(self.kassapaate.edulliset, 4)    
        self.assertEqual(str(self.kortti), "saldo: 0.4")    