# /src/application/use_cases/use_cases.py

from src.domain.entities.entities import (
    FacilityProfile,
    IotSystemConfiguration,
    EfficiencyAssumptions
)

from src.application.dto.roi_use_case_dtos import (
    OperatorBenefitsDTO,
    OperatorIotCostDTO, CalculateRoiResultDTO
)

from src.application.services.calculate_operator_benefits import (
    OperatorBenefitsCalculator)

from src.application.services.calculate_operator_efficiencies import (
    calculate_annual_gain_overnight_rounds,
    calculate_annual_gain_wellness_checks,
    calculate_annual_gain_documentation,
    calculate_annual_gain_response_prioritization,
    calculate_annual_gain_room_entries,
    calculate_annual_gain_delayed_hiring,

)

from src.application.services.calculate_iot_cost_npv import calculate_npv


class CalculateRoiUseCase:

    def __init__(
            self,
            calculate_benefits: OperatorBenefitsCalculator,
    ):
        self._calculate_benefits = calculate_benefits

    def execute(
            self,
            facility: FacilityProfile,
            iot_system_config: IotSystemConfiguration,
            assumptions: EfficiencyAssumptions,
    ) -> CalculateRoiResultDTO:
        # --- OPERATOR BENEFITS

        operator_benefits: OperatorBenefitsDTO = self._calculate_operator_benefits(
            facility=facility,
            assumptions=assumptions,
        )

        # --- IOT SYSTEM COST

        kit_count: int = iot_system_config.kit_installations
        hardware_cost: float = kit_count * iot_system_config.selected_kit_price
        monthly_subscription_cost: float = kit_count * iot_system_config.monthly_subscription_price

        iot_cost_annual: OperatorIotCostDTO = calculate_npv(
            annual_discount_rate=iot_system_config.annual_discount_rate,
            hardware_cost=hardware_cost,
            monthly_subscription_cost=monthly_subscription_cost,
            contract_term_months=iot_system_config.contract_months,
        )

        _print_to_shell_iot_costs(iot_system_config, iot_cost_annual)

        # --- NET BENEFIT & ROI

        net_benefit_annualized = operator_benefits.new_resident_value_annual - iot_cost_annual.annualized_iot_cost
        monthly_benefit: float = net_benefit_annualized / 12

        roi_percent = (
            net_benefit_annualized / iot_cost_annual.annualized_iot_cost
            if iot_cost_annual.annualized_iot_cost > 0
            else 0
        )

        payback_months = (
            iot_cost_annual.npv_cost / monthly_benefit
            if monthly_benefit > 0
            else None
        )

        return CalculateRoiResultDTO(
            staff_payroll_annual=operator_benefits.staff_payroll_annual,
            iot_percent_efficiency=operator_benefits.percent_efficiency,

            efficiency_overnight_rounds=operator_benefits.efficiency_annual_overnight_rounds,
            efficiency_wellness_checks=operator_benefits.efficiency_annual_wellness_checks,
            efficiency_documents=operator_benefits.efficiency_annual_documents,
            efficiency_prioritization=operator_benefits.efficiency_annual_prioritization,
            efficiency_room_entries=operator_benefits.efficiency_annual_room_entries,
            efficiency_total=operator_benefits.efficiency_annual_total,
            delayed_hiring_value=operator_benefits.delayed_hiring_value_annual,
            contribution_margin=operator_benefits.contribution_margin_annualized,
            added_residents_theoretical=operator_benefits.added_residents_theoretical,
            new_resident_value=operator_benefits.new_resident_value_annual,

            annualized_iot_cost=iot_cost_annual.annualized_iot_cost,
            net_annual_benefit=net_benefit_annualized,
            roi_percent=roi_percent,
            payback_months=payback_months,
        )

    def _calculate_operator_benefits(
            self,
            facility: FacilityProfile,
            assumptions: EfficiencyAssumptions,
    ):
        # --- CALCULATE ANNUAL EFFICIENCIES

        loaded_wage: float = facility.loaded_hourly_wage

        overnight_rounds = calculate_annual_gain_overnight_rounds(
            loaded_wage=loaded_wage,
            gain_overnight_rounds_minutes=assumptions.gain_overnight_rounds,
        )

        wellness_checks = calculate_annual_gain_wellness_checks(
            loaded_wage=loaded_wage,
            gain_wellness_checks_minutes=assumptions.gain_wellness_checks,
        )

        documents = calculate_annual_gain_documentation(
            loaded_wage=loaded_wage,
            gain_documentation_minutes=assumptions.gain_documentation,
        )

        prioritization = calculate_annual_gain_response_prioritization(
            loaded_wage=loaded_wage,
            gain_prioritization_minutes=assumptions.gain_response_prioritization,
        )

        room_entries = calculate_annual_gain_room_entries(
            loaded_wage=loaded_wage,
            gain_room_entries_minutes=assumptions.gain_room_entries,
        )

        hiring_delay = calculate_annual_gain_delayed_hiring(
            loaded_wage=loaded_wage,
            months_delay=assumptions.hiring_delay_months,
            count_positions_delayed=assumptions.count_positions_delayed,
        )

        total_efficiencies_annual = (
                overnight_rounds
                + wellness_checks
                + documents
                + prioritization
                + room_entries
                + hiring_delay
        )

        # --- CALCULATE BENEFITS

        (
            staff_payroll_annual,
            percent_efficiency,
            unused_capacity,
        ) = self._calculate_benefits.calculate_unused_capacity(
            resident_count=facility.resident_count,
            caregiver_count=facility.caregiver_count,
            loaded_wage=facility.loaded_hourly_wage,
            total_efficiencies_annual=total_efficiencies_annual,
        )

        (
            annualized_margin,
            added_resident_value,
        ) = self._calculate_benefits.calculate_added_resident_value(
            added_capacity=unused_capacity,
            monthly_revenue=facility.monthly_revenue_per_resident,
            monthly_cost=facility.monthly_variable_cost_per_resident,
        )

        return OperatorBenefitsDTO(
            efficiency_annual_overnight_rounds=overnight_rounds,
            efficiency_annual_wellness_checks=wellness_checks,
            efficiency_annual_documents=documents,
            efficiency_annual_prioritization=prioritization,
            efficiency_annual_room_entries=room_entries,
            efficiency_annual_total=total_efficiencies_annual,
            delayed_hiring_value_annual=hiring_delay,

            staff_payroll_annual=staff_payroll_annual,
            percent_efficiency=percent_efficiency,
            contribution_margin_annualized=annualized_margin,
            added_residents_theoretical=unused_capacity,
            new_resident_value_annual=added_resident_value,
        )


def _print_to_shell_iot_costs(
        assumptions: IotSystemConfiguration,
        cost_object: OperatorIotCostDTO,
):
    print("Alerta Home Operator DCF Costs:")
    print(f"Annual Discount Rate  : {100 * assumptions.annual_discount_rate:.1f}%")
    print(f"Period (months)       : {assumptions.contract_months}")
    print(f"NPV ($)               : {cost_object.npv_cost:,.2f}")
    print(f"Annualized ($)        : {cost_object.annualized_iot_cost:,.2f}")
    print(f"Monthly ($)           : {cost_object.monthly_iot_cost:,.2f}")
    print()
    print()
