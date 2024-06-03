import pandas as pd
import constants_and_calculations as const

"""
This class stores the Waterfall Output as a pandas dataframe. Contains helper functions for calculating the row for sum totals as well as converting
the floats to a dollar string format
"""

class WaterfallDF:
    def __init__(self):
        # Initialize an empty DataFrame with the specified waterfall columns
        self.df = pd.DataFrame(columns=const.waterfall_columns)
    
    def add_row(self, row: dict):
        self.df.loc[len(self.df)] = row

    def calculate_totals(self):
        total_row = {}
        total_row[const.TIER_NAME_COLUMN] = 'Total'
        total_row[const.LP_ALLOCATION_COLUMN] = self.df[const.LP_ALLOCATION_COLUMN].sum()
        total_row[const.GP_ALLOCATION_COLUMN] = self.df[const.GP_ALLOCATION_COLUMN].sum()
        total_row[const.TOTAL_TIER_DISTRIBUTION_COLUMN] = self.df[const.TOTAL_TIER_DISTRIBUTION_COLUMN].sum()
        self.add_row(total_row)
    
    def format_floats_to_dollars(self):
        for column in self.df.columns:
            if self.df[column].dtype == 'float64':
                # Convert float values to dollar format rounded to two decimal places
                self.df[column] = self.df[column].map(lambda x: '${:,.2f}'.format(x) if pd.notnull(x) else x)
    
    def output_to_csv(self, file_path):
        self.format_floats_to_dollars()
        self.df.to_csv(file_path, index=False)
    