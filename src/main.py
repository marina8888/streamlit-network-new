from pages import cover_page, fuel_converter, elv_factors, inputs
from pages.cantera_calculator import cantera_emissions
import streamlit as st

def main():
    st.set_page_config(page_title="Combustion Dashboard", layout="wide", page_icon="resources/images/img.png")

    # Create tabs
    tab_cover, tab_inputs, tab1, tab2, tab3 = st.tabs(["📘 Introduction", "Site Configuration", "Fuel Converter", "Cantera Emissions", "ELV Factors"])

    with tab_cover:
        cover_page.run()


    with tab_inputs:
        inputs.run()

    with tab1:
        fuel_converter.run()

    with tab2:
        cantera_emissions.run()

    with tab3:
        elv_factors.run()


if __name__ == "__main__":
    main()
