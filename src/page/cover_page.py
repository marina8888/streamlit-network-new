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
    ### 📁 Site Configuration Tab
    - Capture information of previous sites with achievable ELVs for future records
    - For sites fuel switching to new fuel - record to attach to permit.
    
    ### 📁 Fuel Converter Tab - In Progress
    - Converts TDS information to inputs for Cantera simulation tab, primarily used for blended fuels with challenging compositions. 
    - A biodiesel composition is typically a mix of FAME or HVO and PtL (e-diesel) which are paraffinic, or biocrude which includes multicomponent (alcohols and nitrogen included in blend)
    
    ## 🔥 Major Emission-Causing Impurities in Biodiesel """)
    st.markdown("""
| Impurity          | Source / Cause                          | Emission Impact                                    | Regulatory Concern |
|-------------------|------------------------------------------|----------------------------------------------------|--------------------|
| **Sulfur (S)**    | Feedstock, catalyst residues             | Forms **SO₂**, **sulfates**, corrosive acids; contributes to **PM** | Must be <10–15 ppm (EN 14214 / ASTM D6751) |
| **Phosphorus (P)**| Degummed oils, phospholipids             | **Poisoning of diesel oxidation catalysts (DOCs)**, increased CO/HC | <10 ppm (EN 14214) |
| **Alkali Metals (Na, K)** | Catalyst residues (NaOH, KOH)    | **Ash**, deposits, catalyst deactivation, **PM** formation | <5 ppm combined (EN 14214) |
| **Alkaline Earth Metals (Ca, Mg)** | Soap residues           | Same as above; **contribute to ash** and emissions | <5 ppm combined (EN 14214) |
| **Iodine (Iodine Value)**| Unsaturated FAMEs (e.g., linoleic acid) | **Indirect**—high iodine value → **oxidative instability**, deposit formation → more **PM** | Iodine value must be <120 (EN 14214) |
| **Water**         | Poor drying, hygroscopic FAMEs           | Causes **microbial growth**, fuel degradation → **increased CO, PM** | <500 mg/kg (EN 14214), ideally <200 ppm |
| **Methanol**      | Incomplete transesterification           | Affects combustion, lowers flash point → **higher CO, unburnt HC** | <0.2 wt% (EN 14214) |
| **Free Glycerol** | Incomplete separation after reaction     | Coking, injector fouling → **PM, CO**               | <0.02 wt% (ASTM D6751) |
| **Total Glycerol**| Bound + free glycerol                    | Engine deposits, **incomplete combustion**, emissions | <0.24 wt% (ASTM D6751) |
| **Nitrogen Compounds** | Proteins in feedstock, contamination | NOₓ precursors, **fuel instability**                | Not directly regulated, but impacts NOₓ |
| **Chlorine (Cl)** | Salts from process water                 | Corrosion, **dioxin and HCl emissions**             | Must be minimized |
| **Polyunsaturated FAMEs** | e.g., Methyl linolenate            | Easily oxidized → deposits, PM, aldehydes           | Limited by Iodine Value & EN 14214 |
| **Unreacted Triglycerides** | Incomplete transesterification | Poor atomization, coking → **higher PM, CO**        | <0.2% wt (EN 14214) |
| **Mono-/Diglycerides**| Reaction intermediates              | Injector fouling, coking → **PM, incomplete combustion** | <0.2% wt combined |
| **Particulate Contaminants (solids)** | Poor filtration       | Abrasion, fouling, increased **PM**                 | Filtered to <1 µm typically |
""")
    st.markdown("""
    ### 🧪 Cantera Emissions Tab
    - Runs a Cantera simulation using a FreeFlame object to predict emerging and possible emissions. 
    - Calculates emissions based on fuel and input conditions (fuel blends are possible if requested). 
    - Currently just looks at a basic device, but may have the option to add additional components, such as selective catalytic reduction, recirculation gases etc. 
    - Reaction mechanism sources: [liquid biodiesels and alcohols](https://gitlab.multiscale.utah.edu/common/ChemicalMechanisms/-/tree/master), ammmonia (Kovaleva mech), natural gas (GRI-3.0), hydrogen and syngas (GRI-3.0 - not a great fit). 
        

    ### 🗂️ NOx Factors Calculator - Not Implemented
    - Converts ELVs based on adjustment factors. 

    ---
    Use the tabs above to navigate.
    """)
