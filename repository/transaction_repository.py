import csv
from typing import List
from datetime import datetime
from models.transaction import Transaction

class TransactionsRepository:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def load_from_csv(self, file_path: str):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                transaction = Transaction(
                    transaction_date=datetime.strptime(row['transaction_date'], '%m/%d/%Y'),
                    transaction_amount=self.clean_and_convert_amount(row['transaction_amount']),
                    contribution_or_distribution=row['contribution_or_distribution'],
                    commitment_id=int(row['commitment_id'])
                )
                self.transactions.append(transaction)

    def clean_and_convert_amount(self, amount: str) -> float:
        amount = amount.strip()
        # Remove dollar sign, commas, spaces, and parentheses
        amount = amount.replace('$', '').replace(',', '').replace(' ', '')
        amount = amount.replace('(', '-').replace(')', '')  # Convert parentheses to negative sign
        return float(amount)

    def get_distributions_for_commitment(self, commitment_id: int) -> List[Transaction]:
        return [t for t in self.transactions if t.commitment_id == commitment_id and t.contribution_or_distribution == 'distribution']

    def get_contributions_for_commitment(self, commitment_id: int, before_date: datetime = None) -> List[Transaction]:
        contributions = [t for t in self.transactions if t.commitment_id == commitment_id and t.contribution_or_distribution == 'contribution']
        if before_date:
            contributions = [t for t in contributions if t.transaction_date <= before_date]
        return contributions
