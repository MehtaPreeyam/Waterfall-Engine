from datetime import datetime

PREFERRED_RETURN_PERCENTAGE = 8
CATCH_UP_PERCENTAGE = 100
CARRIED_INTEREST = 20

RETURN_OF_CAPITAL = 'Return of Capital'
PREFERRED_RETURN = 'Preferred Return'
CATCH_UP = 'Catch-up'
FINAL_SPLIT = f'Final Split {100-CARRIED_INTEREST}/{CARRIED_INTEREST}'

TIER_NAME_COLUMN = 'Tier Name'
STARTING_TIER_CAPITAL_COLUMN = 'Starting Tier Capital'
LP_ALLOCATION_COLUMN = 'LP Allocation'
GP_ALLOCATION_COLUMN = 'GP Allocation'
TOTAL_TIER_DISTRIBUTION_COLUMN = 'Total Tier Distribution'
REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN = 'Remaining Capital for Next Tier'

waterfall_columns = [
            TIER_NAME_COLUMN,
            STARTING_TIER_CAPITAL_COLUMN,
            LP_ALLOCATION_COLUMN,
            GP_ALLOCATION_COLUMN,
            TOTAL_TIER_DISTRIBUTION_COLUMN,
            REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN
        ]

"""
All of the helper functions for doing our tiered calculations are below. Each of them will return the row of data that we will append to our waterfall dataframe
"""

def calculate_return_of_capital(contribution_sum: float, distribution_total: float, previous_capital_returned: float) -> dict:
    if(previous_capital_returned >= contribution_sum):
        contribution_sum = 0
    else:
        # Maximum possible previous capital returned is the sum of all previous distributions and if its not greater than the current contribution sum then subtract it
        contribution_sum -= previous_capital_returned
    
    if(contribution_sum > distribution_total):
        contribution_sum = distribution_total

    return {
        TIER_NAME_COLUMN: RETURN_OF_CAPITAL,
        STARTING_TIER_CAPITAL_COLUMN: distribution_total,
        LP_ALLOCATION_COLUMN: contribution_sum,
        GP_ALLOCATION_COLUMN: 0,
        TOTAL_TIER_DISTRIBUTION_COLUMN: contribution_sum,
        REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN: (distribution_total - contribution_sum)        
    }


def _calculate_preffered_return_for_one_contribution(contribution_amount: float, waterfall_date: datetime, contribution_date: datetime) -> float:
    preffered_rate = PREFERRED_RETURN_PERCENTAGE / 100
    date_format = "%m/%d/%Y"
    waterfall_date = datetime.strptime(waterfall_date, date_format)
    contribution_date = datetime.strptime(contribution_date, date_format)

    difference_in_days = (waterfall_date - contribution_date).days

    preferred_return = (contribution_amount * pow(1 + preffered_rate, (difference_in_days/365))) - contribution_amount

    return preferred_return

def calculate_total_preferred_return(starting_capital, contributions: list, waterfall_date: datetime) -> dict:
    lp_allocation = 0
    for contribution in contributions:
        lp_allocation += _calculate_preffered_return_for_one_contribution(contribution['transaction_amount'], waterfall_date, contribution['transaction_date'])
    
    lp_allocation = round(lp_allocation, 2)

    if(lp_allocation > starting_capital): # Assure we don't allocate more money than we have to give
        lp_allocation = starting_capital

    return {
        TIER_NAME_COLUMN: PREFERRED_RETURN,
        STARTING_TIER_CAPITAL_COLUMN: starting_capital,
        LP_ALLOCATION_COLUMN: lp_allocation,
        GP_ALLOCATION_COLUMN: 0,
        TOTAL_TIER_DISTRIBUTION_COLUMN: lp_allocation,
        REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN: (starting_capital - lp_allocation)
    }


def calculate_catchup(starting_capital: float) -> dict:
    catchup_percentage = CARRIED_INTEREST/(CATCH_UP_PERCENTAGE-CARRIED_INTEREST)
    gp_allocation =  (catchup_percentage) * starting_capital
    gp_allocation = round(gp_allocation, 2)

    return {
        TIER_NAME_COLUMN: CATCH_UP,
        STARTING_TIER_CAPITAL_COLUMN: starting_capital,
        LP_ALLOCATION_COLUMN: 0,
        GP_ALLOCATION_COLUMN: gp_allocation,
        TOTAL_TIER_DISTRIBUTION_COLUMN: gp_allocation,
        REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN: round(starting_capital - gp_allocation, 2)
    }

def calculate_final_split(starting_capital: float) -> dict:
    lp_allocation = round(((100-CARRIED_INTEREST)/100) * starting_capital, 2)
    gp_allocation = round((CARRIED_INTEREST / 100) * starting_capital, 2)

    return {
        TIER_NAME_COLUMN: FINAL_SPLIT,
        STARTING_TIER_CAPITAL_COLUMN: starting_capital,
        LP_ALLOCATION_COLUMN: lp_allocation,
        GP_ALLOCATION_COLUMN: gp_allocation,
        TOTAL_TIER_DISTRIBUTION_COLUMN: (lp_allocation + gp_allocation),
        REMAINING_CAPITAL_FOR_NEXT_TIER_COLUMN: 0
    }
