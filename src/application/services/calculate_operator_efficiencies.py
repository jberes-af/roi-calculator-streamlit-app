# /src/application/services/calculate_operator_benefits

from src.application.dto.roi_use_case_dtos import OperatorBenefitsDTO

from src.domain.services.operator_calculations import (
    contribution_margin,
    added_capacity,
)


class CalculateOperatorEfficienciesService:

    @staticmethod
    def calculate_annual_gain_overnight_rounds():
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

    @staticmethod
    def calculate_annual_gain_wellness_checks(
            facility,
            assumptions,
    ) -> float:
        pass

    @staticmethod
    def calculate_annual_gain_documentation(
            facility,
            assumptions,
    ) -> float:
        pass

    @staticmethod
    def calculate_annual_gain_response_prioritization(
            facility,
            assumptions,
    ) -> float:
        pass

    @staticmethod
    def calculate_annual_gain_room_entries(
            facility,
            assumptions,
    ) -> float:
        pass
