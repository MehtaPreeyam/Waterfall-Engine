from commitments import Commitments
from transactions import Transactions
from waterfall_df import WaterfallDF
import os
import argparse
import constants_and_calculations as calcs


def run_waterfall(commitment_id: int, output_file_path: str = None):
    output_file_path = output_file_path or f'waterfall_{commitment_id}.csv'
    waterfall_df = WaterfallDF()
    try:
        contribution_sum = sum(transaction['transaction_amount'] for transaction in contributions)
        return_of_capital_row = calcs.calculate_return_of_capital(contribution_sum, last_distribution['transaction_amount'])
        waterfall_df.add_row(return_of_capital_row)
    except Exception as e:
        print(f'Waterfall calculations failed at return of capital stage {e}')
        
    try:
        preferred_return_row = calcs.calculate_total_preferred_return(return_of_capital_row[calcs.REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN], contributions, last_distribution['transaction_date'])
        waterfall_df.add_row(preferred_return_row)
    except Exception as e:
        print(f'Waterfall calculations failed at preferred return stage {e}')

    try:
        catchup_row = calcs.calculate_catchup(preferred_return_row[calcs.REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN])
        waterfall_df.add_row(catchup_row)
    except Exception as e:
        print(f'Waterfall calculations failed at catchup stage {e}')

    try:
        final_split_row = calcs.calculate_final_split(catchup_row[calcs.REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN])
        waterfall_df.add_row(final_split_row)
    except Exception as e:
        print(f'Waterfall calculations failed at final split stage {e}')

    waterfall_df.calculate_totals()

    waterfall_df.output_to_csv(output_file_path)

parser = argparse.ArgumentParser()
parser.add_argument("commitment_id", type=str, help="Commitment ID")
parser.add_argument("--output_file_path", type=str, default=None)
args = parser.parse_args()
commitment_id = int(args.commitment_id)
output_file_path = args.output_file_path

script_dir = os.path.dirname(os.path.abspath(__file__))

test_files_dir = os.path.join(script_dir, 'test_files')

commitment_file_path = os.path.join(test_files_dir, 'commitments.csv')
transactions_file_path = os.path.join(test_files_dir, 'transactions.csv')

commitments = Commitments()
commitments.load_from_csv(commitment_file_path)

transactions = Transactions()
transactions.load_from_csv(transactions_file_path)

contributions = transactions.get_contributions_for_commitment(commitment_id)
distributions = transactions.get_distributions_for_commitment(commitment_id)
last_distribution = distributions.iloc[-1]
run_waterfall(commitment_id, output_file_path)
