import streamlit as st

def run():
    st.header("Input Site and Technology Details")

    # Text inputs
    site_name = st.text_input("Site Name")
    permit_number = st.text_input("Permit Number")

    # Technology modeled (multi-select checkboxes)
    st.markdown("### System")
    tech_options = [
        "Furnace",
        "Boiler",
        "Flare",
        "Gas Turbine",
        "Internal Combustion Engine",
    ]
    selected_technologies = st.radio("Select technology types", tech_options)

    # Uses (SCR or NSCR)
    st.markdown("### Add-Ons")
    use_options = [
        "SCR (NOx Scrubber)",
        "NSCR (Downstream urea/ammonia injection)",
        "EGR (Exhaust Gas Recirculation)",
    ]
    selected_uses = st.multiselect("Select uses", use_options)

    # Show entered data (optional)
    if st.button("Submit"):
        st.write("Site Name:", site_name)
        st.write("Permit Number:", permit_number)
        st.write("Technologies:", selected_technologies)
        st.write("Uses:", selected_uses)
