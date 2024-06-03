import pandas as pd
from typing import Optional

"""
Implemented this class before I realized we're not using commitments for this excercise
"""

class Commitments:
    def __init__(self, df: Optional[pd.DataFrame] = None):
        if df:
            self.df = df
            self.turn_commitment_into_float()

    def get_commitment_amount_per_fund_id(self, fund_id):
        total_commitment = self.df[self.df['fund_id'] == fund_id]['commitment_amount'].sum()
        return total_commitment
    
    def turn_commitment_into_float(self):
        self.df['commitment_amount'] = self.df['commitment_amount'].replace('[\$,]', '', regex=True).astype(float)
    
    def load_from_csv(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.turn_commitment_into_float()