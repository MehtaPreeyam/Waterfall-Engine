import unittest
from datetime import datetime
from constants_and_calculations import calculate_catchup, calculate_final_split, calculate_return_of_capital, calculate_total_preferred_return, _calculate_preffered_return_for_one_contribution

class TestWaterfallCalculations(unittest.TestCase):
    def test_calculate_return_of_capital(self):
        contribution_sum = 100000
        distribution_total = 150000
        expected_output = {
            'Tier Name': 'Preferred Return',
            'Starting Tier Capital': 150000,
            'LP Allocation': 100000,
            'GP Allocation': 0,
            'Total Tier Distribution': 100000,
            'Remaining Capital for Next Tier': 50000
        }
        result = calculate_return_of_capital(contribution_sum, distribution_total)
        self.assertEqual(result, expected_output)

    def test_calculate_return_of_capital_with_higher_contribution(self):
        contribution_sum = 200000
        distribution_total = 150000
        expected_output = {
            'Tier Name': 'Preferred Return',
            'Starting Tier Capital': 150000,
            'LP Allocation': 150000,
            'GP Allocation': 0,
            'Total Tier Distribution': 150000,
            'Remaining Capital for Next Tier': 0
        }
        result = calculate_return_of_capital(contribution_sum, distribution_total)
        self.assertEqual(result, expected_output)

    def test_calculate_preferred_return_for_one_contribution(self):
        starting_capital = 100000
        waterfall_date = "01/01/2020"
        contribution_date = "01/01/2019"
        expected_preferred_return = 8000.0
        result = _calculate_preffered_return_for_one_contribution(starting_capital, waterfall_date, contribution_date)
        self.assertAlmostEqual(result, expected_preferred_return, places=2)

    def test_calculate_total_preferred_return(self):
        starting_capital = 100000
        contributions = [
            {'transaction_amount': 50000, 'transaction_date': "01/01/2019"},
            {'transaction_amount': 50000, 'transaction_date': "06/01/2019"}
        ]
        waterfall_date = "01/01/2020"
        expected_output = {
            'Tier Name': 'Preferred Return',
            'Starting Tier Capital': 100000,
            'LP Allocation': 6307.79,
            'GP Allocation': 0,
            'Total Tier Distribution': 6307.79,
            'Remaining Capital for Next Tier': 93692.21
        }
        result = calculate_total_preferred_return(starting_capital, contributions, waterfall_date)
        self.assertAlmostEqual(result['LP Allocation'], expected_output['LP Allocation'], places=2)
        self.assertAlmostEqual(result['Total Tier Distribution'], expected_output['Total Tier Distribution'], places=2)
        self.assertAlmostEqual(result['Remaining Capital for Next Tier'], expected_output['Remaining Capital for Next Tier'], places=2)

    def test_calculate_catchup(self):
        starting_capital = 100000
        expected_output = {
            'Tier Name': 'Catch-up',
            'Starting Tier Capital': 100000,
            'LP Allocation': 0,
            'GP Allocation': 25000.0,
            'Total Tier Distribution': 25000.0,
            'Remaining Capital for Next Tier': 75000.0
        }
        result = calculate_catchup(starting_capital)
        self.assertAlmostEqual(result['GP Allocation'], expected_output['GP Allocation'], places=2)
        self.assertAlmostEqual(result['Total Tier Distribution'], expected_output['Total Tier Distribution'], places=2)
        self.assertAlmostEqual(result['Remaining Capital for Next Tier'], expected_output['Remaining Capital for Next Tier'], places=2)

    def test_calculate_final_split(self):
        starting_capital = 100000
        expected_output = {
            'Tier Name': 'Final Split 80/20',
            'Starting Tier Capital': 100000,
            'LP Allocation': 80000.0,
            'GP Allocation': 20000.0,
            'Total Tier Distribution': 100000.0,
            'Remaining Capital for Next Tier': 0
        }
        result = calculate_final_split(starting_capital)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
