import streamlit as st

def run():
    st.header("📘Introduction Notes - by MK")
    st.markdown("""
    #### 🔥 Background
    This calculator is used for calculating the output parameters to as supporting information for permitting and AQMAU, 
    given a known fuel composition input.
    """)

    st.image("resources/images/process.png", caption="Inputs and Outputs", width=600)

    st.markdown("""
    ### 📁 Fuel Converter Tab
    - Converts TDS information to inputs for Cantera simulation tab. 
    - Obtains scaling factors for emissions conversion. 
    
    ### 🧪 Cantera Emissions Tab
    - Runs a Cantera simulation using a FreeFlame object to predict emerging and possible emissions. 
    - Calculates emissions based on fuel and input conditions (fuel blends are possible if requested). 
    - Currently just looks at a basic device, but may have the option to add additional components, such as selective catalytic reduction, recirculation gases etc. 
    - Reaction mechanism sources: [liquid biodiesels and alcohols](https://gitlab.multiscale.utah.edu/common/ChemicalMechanisms/-/tree/master), ammmonia (Kovaleva mech), natural gas (GRI-3.0), hydrogen and syngas (GRI-3.0 - not a great fit). 
        

    ### 🗂️ NOx Factors Calculator
    - Converts ELVs based on adjustment factors. 

    ---
    Use the tabs above to navigate.
    """)
