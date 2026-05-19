# /src/application/use_cases/use_cases.py

from src.domain.entities.entities import (
    FacilityProfile,
    IotSystemConfiguration,
    EfficiencyAssumptions, IotPricingCatalog,
)

from src.domain.value_objects.value_objects import RoiResult

from src.domain.services.operator_calculations import (
    contribution_margin,
    added_capacity,
    monthly_discount_rate,
    annuity_present_value,
)

from src.application.dto.roi_use_case_dtos import (
    OperatorBenefitsDTO,
    OperatorIotCostDTO
)

from src.application.services.calculate_operator_benefits import (
    CalculateOperatorBenefitsService)

from src.application.services.calculate_operator_efficiencies import (
    CalculateOperatorEfficienciesService)

from src.application.services.calculate_iot_cost_npv import calculate_npv


class CalculateRoiUseCase:

    def __init__(
            self,
            calculate_efficiencies: CalculateOperatorEfficienciesService,
            calculate_benefits: CalculateOperatorBenefitsService,
    ):
        self._calculate_efficiencies = calculate_efficiencies
        self._calculate_benefits = calculate_benefits

    def execute(
            self,
            facility: FacilityProfile,
            iot_system_config: IotSystemConfiguration,
            assumptions: EfficiencyAssumptions,
    ) -> RoiResult:
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

        # --- NET BENEFITS

        net_annual_benefit = (
                operator_benefits.total_annual_benefit
                - iot_cost_annual.annualized_iot_cost
        )

        monthly_benefit = operator_benefits.total_annual_benefit / 12

        # --- ROI

        roi_percent = (
            net_annual_benefit / iot_cost_annual.annualized_iot_cost
            if iot_cost_annual.annualized_iot_cost > 0
            else 0
        )

        payback_months = (
            iot_cost_annual.npv_cost / monthly_benefit
            if monthly_benefit > 0
            else None
        )

        return RoiResult(
            contribution_margin_per_resident=operator_benefits.margin,
            added_resident_capacity=operator_benefits.added_residents,
            delayed_hiring_value_annual=operator_benefits.delayed_hiring_value_annual,
            occupancy_value_annual=operator_benefits.occupancy_value_annual,
            overnight_savings_annual=operator_benefits.overnight_savings_annual,
            total_annual_benefit=operator_benefits.total_annual_benefit,
            annualized_iot_cost=iot_cost_annual.annualized_iot_cost,
            net_annual_benefit=net_annual_benefit,
            roi_percent=roi_percent,
            payback_months=payback_months,
        )

    def _calculate_operator_benefits(
            self,
            facility: FacilityProfile,
            assumptions: EfficiencyAssumptions,
    ):
        # --- CALCULATE EFFICIENCIES

        overnight_rounds = self._calculate_efficiencies.calculate_annual_gain_overnight_rounds()
        wellness_checks = self._calculate_efficiencies.calculate_annual_gain_wellness_checks()
        documents = self._calculate_efficiencies.calculate_annual_gain_documentation()
        prioritization = self._calculate_efficiencies.calculate_annual_gain_response_prioritization()
        room_entries = self._calculate_efficiencies.calculate_annual_gain_room_entries()
        total_efficiencies = (
                overnight_rounds + wellness_checks + documents + prioritization + room_entries
        )

        # --- CALCULATE BENEFITS

        (
            margin,
            added_residents,
            new_resident_value,
        ) = self._calculate_benefits.calculate_new_resident_contribution(
            facility.monthly_revenue_per_resident,
            facility.monthly_variable_cost_per_resident,

        )

        delayed_hiring = self._calculate_benefits.calculate_new_resident_contribution()

        total_annual_benefit = (
                total_efficiencies
                + new_resident_value
                + delayed_hiring
        )

        return OperatorBenefitsDTO(
            contribution_margin=margin,
            added_residents_theoretical=added_residents,
            new_resident_value_annual=new_resident_value,
            delayed_hiring_value_annual=delayed_hiring,
            total_benefit_annual=total_annual_benefit,

            efficiency_annual_overnight_rounds=overnight_rounds,
            efficiency_annual_wellness_checks=wellness_checks,
            efficiency_annual_documents=documents,
            efficiency_annual_prioritization=prioritization,
            efficiency_annual_room_entries=room_entries,
            efficiency_annual_total=total_efficiencies,
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
