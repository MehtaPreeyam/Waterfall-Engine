import pandas as pd
from typing import Optional
import datetime

"""
After reading transactions from the csv file we store them into a pandas dataframe in this class
This class also contains all the helper functions to give us all the contributions and distributions for a commitment_id 
"""
class Transactions:
    def __init__(self, df: Optional[pd.DataFrame] = None):
        if df:
            self.df = df
            self.turn_commitment_into_float()
        
    def get_contributions_for_commitment(self, commitment_id: int, date: datetime):
        contributions = self.df[
            (self.df['commitment_id'] == commitment_id) & 
            (self.df['contribution_or_distribution'] == 'contribution') & 
            (self.df['transaction_date'] <= date)
        ]
        return contributions.to_dict(orient='records')
    
    def get_distributions_for_commitment(self, commitment_id: int):
        distributions = self.df[(self.df['commitment_id'] == commitment_id) & (self.df['contribution_or_distribution'] == 'distribution')]
        return distributions
    
    def clean_and_convert_amount(self, amount: str):
        amount = amount.strip()
        # Remove dollar sign, commas, and spaces
        amount = amount.replace('$', '').replace(',', '').replace(' ', '')
        amount = amount.replace('(', '').replace(')', '')
        return float(amount)
    
    def load_from_csv(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.df['transaction_amount'] = self.df['transaction_amount'].apply(self.clean_and_convert_amount)