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
    selected_technologies = st.radio("Select technology to model", tech_options)

    st.markdown("## 🔥 Previous Fuel Used in this System")

    # Predefined list of fuels
    fuel_options = ["Natural Gas", "Gas Oil/Diesel", "Propane", "Hydrogen", "Biodiesel", "Other", "None (New System)"]

    # Dropdown to select fuel
    selected_fuel = st.selectbox("Select previous fuel type", fuel_options)

    # If "Other" is selected, show a text input to enter custom fuel name
    if selected_fuel == "Other":
        custom_fuel = st.text_input("Enter unlisted fuel type")
        permit_fuel = custom_fuel
    else:
        permit_fuel = selected_fuel


    st.markdown("### Emission Limit Values")
    st.markdown("##### Previously Achieved by Operator (For Retraining New Simulations)")

    # Create 4 columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        co_limit_prev = st.number_input("CO Limit (ppm)", min_value=0.0, step=1.0, key="co_limit_prev")
    with col2:
        no_limit_prev = st.number_input("NO Limit (ppm)", min_value=0.0, step=1.0, key="no_limit_prev")
    with col3:
        so2_limit_prev = st.number_input("SO₂ Limit (ppm)", min_value=0.0, step=1.0, key="so2_limit_prev")
    with col4:
        nvpm_limit_prev = st.number_input("nvPM Limit (ppm)", min_value=0.0, step=1.0, key="nvpm_limit_prev")

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
