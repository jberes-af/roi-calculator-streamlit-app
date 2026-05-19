# /src/application/dto/roi_use_case_dtos.py

from dataclasses import dataclass

from src.domain.entities.entities import (
    FacilityProfile,
    IotSystemConfiguration,
    EfficiencyAssumptions
)


@dataclass(frozen=True)
class CalculationInputsDTO:
    facility: FacilityProfile
    iot_system_config: IotSystemConfiguration
    assumptions: EfficiencyAssumptions


@dataclass(frozen=True)
class OperatorBenefitsDTO:
    contribution_margin: float
    added_residents_theoretical: float
    delayed_hiring_value_annual: float
    new_resident_value_annual: float
    total_benefit_annual: float

    efficiency_annual_overnight_rounds: float
    efficiency_annual_wellness_checks: float
    efficiency_annual_documents: float
    efficiency_annual_prioritization: float
    efficiency_annual_room_entries: float
    efficiency_annual_total: float


@dataclass(frozen=True)
class OperatorIotCostDTO:
    npv_cost: float
    monthly_iot_cost: float
    annualized_iot_cost: float


