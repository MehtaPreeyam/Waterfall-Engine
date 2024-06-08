from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    transaction_date: datetime
    transaction_amount: float
    contribution_or_distribution: str
    commitment_id: int

    def __str__(self):
        return (f"Transaction(Date: {self.transaction_date.strftime('%Y-%m-%d')}, "
                f"Amount: {self.transaction_amount}, "
                f"Type: {self.contribution_or_distribution}, "
                f"Commitment ID: {self.commitment_id})")
