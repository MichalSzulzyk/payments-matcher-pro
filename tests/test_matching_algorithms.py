import unittest
from matching_algorithms import match_payments_invoices, get_similarity

class TestMatchingAlgorithms(unittest.TestCase):

    def test_get_similarity(self):
        string1 = "123 Main St"
        string2 = "123 Main Street"
        result = get_similarity(string1, string2)
        self.assertAlmostEqual(result, 0.8235, delta=0.01)

if __name__ == '__main__':
    unittest.main()
