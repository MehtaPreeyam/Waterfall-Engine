# Waterfall Distribution Script

This script processes transactions and handles waterfall distributions, calculating preferred returns, adding tiers, and outputting results to a CSV file.

## Requirements

- Python 3.x
- pandas
- argparse

## Installation

1. Ensure you have Python 3.9 installed on your system.
2. Install the required libraries using pip:
   pip install pandas

## Usage
python main.py <commitment_id> [--output_file_path <output_file_path>] [--carried_interest <carried_interest_amount>] [--preferred_return <preferred_return_amount>]

## Args
<commitment_id>: The commitment ID for the waterfall (required).
--output_file_path: Optional argument to specify the output file path for the CSV file. If not provided, the output file will be named waterfall_<commitment_id>.csv.
--carried_interest: Optional argument to specify the carried interest
--preferred_return: Optional argument to specify the preferred return
