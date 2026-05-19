# /src/gui/streamlit/screens/roi_calculation_page.py


from src.domain.value_objects.value_objects import RoiResult

import streamlit as st


def render_roi_calculation_screen(result: RoiResult):

    st.title("Care Facility Alerta Home ROI Calculator")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Annual Benefit", f"${result.total_annual_benefit:,.0f}")
    col2.metric("Annual IoT Cost", f"${result.annualized_iot_cost:,.0f}")
    col3.metric("Net Annual Benefit", f"${result.net_annual_benefit:,.0f}")
    col4.metric("ROI", f"{result.roi_percent:.0%}")

    st.subheader("ROI Components")

    st.table(
        {
            "Component": [
                "Delayed caregiver hiring",
                "Increased occupancy",
                "Reduced overnight workload",
            ],
            "Annual Value": [
                f"${result.delayed_hiring_value_annual:,.0f}",
                f"${result.occupancy_value_annual:,.0f}",
                f"${result.overnight_savings_annual:,.0f}",
            ],
        }
    )

    st.subheader("Operational Outputs")

    st.write(f"Contribution margin per resident: **${result.contribution_margin_per_resident:,.0f}/month**")
    st.write(f"Estimated added resident capacity: **{result.added_resident_capacity:.1f} residents**")

    if result.payback_months:
        st.write(f"Estimated payback period: **{result.payback_months:.1f} months**")
