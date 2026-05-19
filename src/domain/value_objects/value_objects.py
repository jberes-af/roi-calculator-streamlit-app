# /src/domain/value_objects/value_objects.py

from dataclasses import dataclass

@dataclass(frozen=True)
class RoiResult:
    contribution_margin_per_resident: float
    added_resident_capacity: float
    delayed_hiring_value_annual: float
    occupancy_value_annual: float
    overnight_savings_annual: float
    total_annual_benefit: float
    annualized_iot_cost: float
    net_annual_benefit: float
    roi_percent: float
    payback_months: float | None
