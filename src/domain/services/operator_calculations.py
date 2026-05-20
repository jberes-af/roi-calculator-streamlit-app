# /src/domain/assumptions/operator_calculations.py

"""
for the system cost annuity:
1. calculate present value of the 24-month annuity
   `PV_Annuity = PMT × (1 − (1 + r)^−n) / r`
2. then discount it back one additional month:
   `PV_Deferred = PV_Annuity / (1 + r)`
3. then add the hardware cost
"""


# HOURS_PER_YEAR_1_FTE: float = 2080  # 40 hours p week * 52 weeks per year
# HOURS_PER_YEAR_CALENDAR: float = 8760  # 24 * 365



def monthly_discount_rate(annual_rate: float) -> float:
    return (1 + annual_rate) ** (1 / 12) - 1


"""
def annuity_present_value(
        monthly_payment: float,
        monthly_rate: float,
        months: int,
) -> float:
    if monthly_rate == 0:
        return monthly_payment * months

    return monthly_payment * (1 - (1 + monthly_rate) ** -months) / monthly_rate
"""

def contribution_margin(
        monthly_revenue: float,
        monthly_variable_cost: float,
) -> float:
    return monthly_revenue - monthly_variable_cost


def added_capacity(
        current_residents: int,
        efficiency_gain: float,
) -> float:
    return current_residents * efficiency_gain


def present_value_iot_system_cost(
        hardware_cost: float,
        monthly_payment: float,
        monthly_rate: float,
        months: int,
) -> float:
    # No discounting case
    if monthly_rate == 0:
        return hardware_cost + (monthly_payment * months)

    # Standard annuity PV
    npv_subscription = (
            monthly_payment
            * (1 - (1 + monthly_rate) ** (-months))
            / monthly_rate
    )

    # First payment begins one month later
    # discount the subscription annuity back one additional month
    npv_subscription /= (1 + monthly_rate)

    total_npv = hardware_cost + npv_subscription

    return total_npv

