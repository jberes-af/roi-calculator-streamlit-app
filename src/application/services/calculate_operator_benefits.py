# /src/application/services/calculate_operator_benefits

from src.application.dto.roi_use_case_dtos import OperatorBenefitsDTO

from src.domain.services.operator_calculations import (
    contribution_margin,
    added_capacity,
)



class CalculateOperatorBenefitsService:

    @staticmethod
    def calculate_new_resident_contribution(
            facility,
            assumptions,
    ) -> tuple[float, float, float]:
        # --- NEW RESIDENT CONTRIBUTION MARGIN

        margin = contribution_margin(
            facility.monthly_revenue_per_resident,
            facility.monthly_variable_cost_per_resident,
        )

        added_residents = added_capacity(
            facility.resident_count,
            assumptions.caregiver_efficiency_gain,
        )

        occupancy_value_annual = (
                assumptions.occupancy_lift_residents * margin * 12
        )
        return margin, added_residents, occupancy_value_annual

    @staticmethod
    def calculate_delayed_hiring_benefit(
            facility,
            assumptions,
    ) -> float:
        # --- DELAYED HIRING

        delayed_hiring_value_annual = 0   # added_residents * margin * 12
        return delayed_hiring_value_annual



"""
    margin = contribution_margin(
        facility.monthly_revenue_per_resident,
        facility.monthly_variable_cost_per_resident,
    )

    added_residents = added_capacity(
        facility.resident_count,
        assumptions.caregiver_efficiency_gain,
    )

    occupancy_value_annual = (
            assumptions.occupancy_lift_residents * margin * 12
    )

    # --- DELAYED HIRING

    delayed_hiring_value_annual = added_residents * margin * 12

    # --- WORK SHIFT TIME SAVINGS (MINUTES GAINS)

    assumptions.caregiver_efficiency_gain

    overnight_savings_annual = (
            assumptions.overnight_hours_saved_per_night
            * assumptions.loaded_hourly_wage
            * 365
    )

    total_annual_benefit = (
            delayed_hiring_value_annual
            + occupancy_value_annual
            + overnight_savings_annual
    )

    return OperatorBenefitsDTO(
        margin=margin,
        added_residents=added_residents,
        delayed_hiring_value_annual=delayed_hiring_value_annual,
        occupancy_value_annual=occupancy_value_annual,
        overnight_savings_annual=overnight_savings_annual,
        total_annual_benefit=total_annual_benefit,
    )

"""



"""
    margin = contribution_margin(
        facility.monthly_revenue_per_resident,
        facility.monthly_variable_cost_per_resident,
    )

    added_residents = added_capacity(
        facility.resident_count,
        assumptions.caregiver_efficiency_gain,
    )

    occupancy_value_annual = (
            assumptions.occupancy_lift_residents * margin * 12
    )

    # --- DELAYED HIRING

    delayed_hiring_value_annual = added_residents * margin * 12

    # --- WORK SHIFT TIME SAVINGS (MINUTES GAINS)

    assumptions.caregiver_efficiency_gain

    overnight_savings_annual = (
            assumptions.overnight_hours_saved_per_night
            * assumptions.loaded_hourly_wage
            * 365
    )

    total_annual_benefit = (
            delayed_hiring_value_annual
            + occupancy_value_annual
            + overnight_savings_annual
    )

    return OperatorBenefitsDTO(
        margin=margin,
        added_residents=added_residents,
        delayed_hiring_value_annual=delayed_hiring_value_annual,
        occupancy_value_annual=occupancy_value_annual,
        overnight_savings_annual=overnight_savings_annual,
        total_annual_benefit=total_annual_benefit,
    )

"""
