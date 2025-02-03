import unittest
from calculariva import calculariva

class PruebaCalcularIva(unittest.TestCase):
    def test_iva_de_100(self):
        # El IVA debería ser 21.
        self.assertEqual(calculariva(100), 21)

if __name__ == '__main__':
    unittest.main()
