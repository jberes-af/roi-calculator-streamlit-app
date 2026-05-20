# /src/application/services/calculate_operator_benefits.py

from src.domain.services.operator_calculations import (
    contribution_margin,
    added_capacity,
)


HOURS_PER_YEAR_1_FTE: int = 2080  # 40 hours p week * 52 weeks per year
DAYS_PER_YEAR: int = 365
MONTHS_PER_YEAR: int = 12


class OperatorBenefitsCalculator:

    @staticmethod
    def calculate_unused_capacity(
            resident_count: int,
            caregiver_count: int,
            loaded_wage: float,  # hourly wage
            total_efficiencies_annual: float,
    ) -> tuple[float, float, float, float]:
        payroll_per_fte_per_year: float = loaded_wage * HOURS_PER_YEAR_1_FTE
        staff_payroll_annual: float = payroll_per_fte_per_year * caregiver_count

        percent_efficiency: float = total_efficiencies_annual / staff_payroll_annual
        unused_capacity: float = percent_efficiency * resident_count

        added_residents_theoretical = unused_capacity

        added_residents_use_case = (
            int(unused_capacity)
            if unused_capacity >= 1
            else unused_capacity
        )

        return (
            staff_payroll_annual,
            percent_efficiency,
            added_residents_theoretical,
            added_residents_use_case
        )

    @staticmethod
    def calculate_added_resident_value(
            added_capacity: float,
            monthly_revenue: float,
            monthly_cost: float,
    ) -> tuple[float, float, float]:

        margin = contribution_margin(
            monthly_revenue,
            monthly_cost,
        )

        added_resident_value_monthly = margin * added_capacity

        annualized_margin = MONTHS_PER_YEAR * margin
        added_resident_value_annual = annualized_margin * added_capacity

        return (
            annualized_margin,
            added_resident_value_monthly,
            added_resident_value_annual,
        )
