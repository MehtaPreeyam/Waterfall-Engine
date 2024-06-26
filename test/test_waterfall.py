import unittest
from datetime import datetime
from constants import constants_and_calculations as calcs
from models.transaction import Transaction

class TestWaterfallCalculations(unittest.TestCase):
    def test_calculate_return_of_capital(self):
        contribution_sum = 100000
        distribution_total = 150000
        expected_output = {
            'Tier Name': calcs.RETURN_OF_CAPITAL,
            'Starting Tier Capital': 150000,
            'LP Allocation': 99000,
            'GP Allocation': 0,
            'Total Tier Distribution': 99000,
            'Remaining Capital for Next Tier': 51000
        }
        result = calcs.calculate_return_of_capital(contribution_sum, distribution_total, 1000)
        self.assertEqual(result, expected_output)

    def test_calculate_return_of_capital_with_higher_contribution(self):
        contribution_sum = 200000
        distribution_total = 150000
        expected_output = {
            'Tier Name': calcs.RETURN_OF_CAPITAL,
            'Starting Tier Capital': 150000,
            'LP Allocation': 150000,
            'GP Allocation': 0,
            'Total Tier Distribution': 150000,
            'Remaining Capital for Next Tier': 0
        }
        result = calcs.calculate_return_of_capital(contribution_sum, distribution_total, 0)
        self.assertEqual(result, expected_output)

    def test_calculate_return_of_capital_with_high_previous_capital_returned(self):
        contribution_sum = 200000
        distribution_total = 150000
        previous_capital_returned = 1000000
        expected_output = {
            'Tier Name': calcs.RETURN_OF_CAPITAL,
            'Starting Tier Capital': 150000,
            'LP Allocation': 0,
            'GP Allocation': 0,
            'Total Tier Distribution': 0,
            'Remaining Capital for Next Tier': 150000
        }
        result = calcs.calculate_return_of_capital(contribution_sum, distribution_total, previous_capital_returned)
        self.assertEqual(result, expected_output)

    def test_calculate_preferred_return_for_one_contribution(self):
        starting_capital = 100000
        waterfall_date = datetime.strptime("01/01/2020", "%m/%d/%Y")
        contribution_date = datetime.strptime("01/01/2019", "%m/%d/%Y")
        expected_preferred_return = 8000.0
        result = calcs._calculate_preffered_return_for_one_contribution(starting_capital, waterfall_date, contribution_date)
        self.assertEqual(result, expected_preferred_return)

    def test_calculate_total_preferred_return(self):
        starting_capital = 100000
        transaction1 = Transaction(
            transaction_date=datetime.strptime("01/01/2019", "%m/%d/%Y"),
            transaction_amount=50000,
            contribution_or_distribution='contribution',
            commitment_id=1
        )
        transaction2 = Transaction(
            transaction_date=datetime.strptime("06/01/2019", "%m/%d/%Y"),
            transaction_amount=50000,
            contribution_or_distribution='contribution',
            commitment_id=1
        )
        contributions = [transaction1, transaction2]

        waterfall_date = datetime.strptime("01/01/2020", "%m/%d/%Y")
        expected_output = {
            'Tier Name': calcs.PREFERRED_RETURN,
            'Starting Tier Capital': 100000,
            'LP Allocation': 6307.79,
            'GP Allocation': 0,
            'Total Tier Distribution': 6307.79,
            'Remaining Capital for Next Tier': 93692.21
        }
        result = calcs.calculate_total_preferred_return(starting_capital, contributions, waterfall_date)
        self.assertEqual(result, expected_output)

    def test_calculate_total_preferred_return_where_lp_allocation_exceeds(self):
        starting_capital = 100
        transaction1 = Transaction(
            transaction_date=datetime.strptime("01/01/2019", "%m/%d/%Y"),
            transaction_amount=50000,
            contribution_or_distribution='contribution',
            commitment_id=1
        )
        transaction2 = Transaction(
            transaction_date=datetime.strptime("06/01/2019", "%m/%d/%Y"),
            transaction_amount=50000,
            contribution_or_distribution='contribution',
            commitment_id=1
        )
        contributions = [transaction1, transaction2]
        waterfall_date = datetime.strptime("01/01/2020", "%m/%d/%Y")
        expected_output = {
            'Tier Name': calcs.PREFERRED_RETURN,
            'Starting Tier Capital': 100,
            'LP Allocation': 100,
            'GP Allocation': 0,
            'Total Tier Distribution': 100,
            'Remaining Capital for Next Tier': 0
        }
        result = calcs.calculate_total_preferred_return(starting_capital, contributions, waterfall_date)
        self.assertEqual(result, expected_output)

    def test_calculate_catchup(self):
        starting_capital = 100000
        expected_output = {
            'Tier Name': calcs.CATCH_UP,
            'Starting Tier Capital': 100000,
            'LP Allocation': 0,
            'GP Allocation': 25000.0,
            'Total Tier Distribution': 25000.0,
            'Remaining Capital for Next Tier': 75000.0
        }
        result = calcs.calculate_catchup(starting_capital)
        self.assertEqual(result, expected_output)

    def test_calculate_final_split(self):
        starting_capital = 100000
        expected_output = {
            'Tier Name': calcs.FINAL_SPLIT,
            'Starting Tier Capital': 100000,
            'LP Allocation': 80000.0,
            'GP Allocation': 20000.0,
            'Total Tier Distribution': 100000.0,
            'Remaining Capital for Next Tier': 0
        }
        result = calcs.calculate_final_split(starting_capital)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
