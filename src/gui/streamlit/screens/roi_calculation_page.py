# /src/gui/streamlit/screens/roi_calculation_page.py


from src.application.dto.roi_use_case_dtos import CalculateRoiResultDTO

import streamlit as st


def render_roi_calculation_screen(result: CalculateRoiResultDTO):

    st.title("Care Facility Alerta Home ROI Calculator")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Annual Benefit", f"${result.net_annual_benefit:,.0f}")
    col2.metric("Annual IoT Cost", f"${result.annualized_iot_cost:,.0f}")
    col3.metric("Payback (months)", f"{result.payback_months:.1f}")
    col4.metric("ROI", f"{result.roi_percent:.0%}")


    st.write("")
    st.subheader("Operational Outputs")
    st.write(f"Calculated caregiver staff payroll (annual): **${result.staff_payroll_annual:,.0f}**")
    st.write(f"Operational %-Efficiency from Alerta Home: **{100 * result.iot_percent_efficiency:.1f}%**")
    st.write(f"Contribution margin per resident: **${result.contribution_margin:,.0f}**")
    st.write(f"Estimated added resident capacity: **{result.added_residents_theoretical:.1f} residents**")

    # if result.payback_months:
        # st.write(f"Estimated payback period: **{result.payback_months:.1f} months**")

    st.write("")
    st.subheader("Efficiency Components (annualized $)")

    st.table(
        {
            "Component": [
                "Reduced Overnight Rounds Time",
                "Reduced Wellness Check Time",
                "Reduced Documentation Time",
                "Reduced Prioritization Response Time",
                "Reduced Room Entry Time",
                "Benefit Delayed New Caregiver Hiring",
                "Total",
            ],
            "Annual Value": [
                f"${result.efficiency_overnight_rounds:,.0f}",
                f"${result.efficiency_wellness_checks:,.0f}",
                f"${result.efficiency_documents:,.0f}",
                f"${result.efficiency_prioritization:,.0f}",
                f"${result.efficiency_room_entries:,.0f}",
                f"${result.delayed_hiring_value:,.0f}",
                f"${result.efficiency_total:,.0f}",
            ],
        }
    )
