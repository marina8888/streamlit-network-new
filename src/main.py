from combustion import cantera_emissions, tds_input
import streamlit as st
def main():

    st.set_page_config(page_title="Combustion Dashboard", layout="wide")
    st.title("Combustion Analysis Dashboard")

    # Define the tabs
    tab1, tab2 = st.tabs(["Cantera Emissions", "TDS Input"])

    # Tab 1: Cantera Emissions
    with tab1:
        cantera_emissions.run()

    # Tab 2: TDS Input
    with tab2:
        tds_input.run()


if __name__ == "__main__":
    main()
