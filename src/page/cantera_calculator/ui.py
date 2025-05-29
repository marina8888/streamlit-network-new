import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

FUEL_OPTIONS = ['CH4', 'C2H6', 'C3H8', 'H2', 'CO', 'NH3', 'DME', 'C2H5OH', 'biodiesel', 'butanol']

def get_user_inputs():
    st.sidebar.header("Input Conditions")

    fuel1 = st.sidebar.selectbox("Primary Fuel", FUEL_OPTIONS, key="fuel1")
    fuel2 = st.sidebar.selectbox("Secondary Fuel", ['None'] + FUEL_OPTIONS, key="fuel2")
    mix_ratio = st.sidebar.slider("Primary Fuel Fraction", 0.0, 1.0, 1.0, 0.05, key="mix")
    oxidizer = st.sidebar.selectbox("Oxidizer", ['Air', 'O2'], key="oxidizer")
    phi = st.sidebar.slider("Equivalence Ratio (ϕ)", 0.5, 2.0, 1.0, 0.05, key="phi")
    T_in = st.sidebar.slider("Initial Temperature (K)", 300, 1500, 300, 50, key="Tin")
    P_atm = st.sidebar.slider("Pressure (atm)", 1, 20, 1, key="Patm")
    dust_ppm = st.sidebar.number_input("Ash level (%)", min_value=0.0, value=10.0, step=1.0, key="dust")
    sulfur_ppm = st.sidebar.number_input("Sulphur in fuel (%)", min_value=0.0, value=0.0, step=0.01, key="sulfur")

    # Fuel mixing
    fuel_mix = {}
    if fuel2 != 'None' and mix_ratio < 1.0:
        fuel_mix[fuel1] = mix_ratio
        fuel_mix[fuel2] = 1.0 - mix_ratio
    else:
        fuel_mix[fuel1] = 1.0

    oxid = "O2:1.0, N2:3.76" if oxidizer == "Air" else "O2:1.0"

    return {
        "fuel_mix": fuel_mix,
        "oxid": oxid,
        "phi": phi,
        "T_in": T_in,
        "P_atm": P_atm,
        "dust_ppm": dust_ppm,
        "sulfur_ppm": sulfur_ppm
    }


def get_emissions_summary(gas):
    emissions_groups = {
        "Cyanides (total)": ["HCN", "CN", "CNO", "CNH"],
        "HCN": ["HCN"],
        "NO": ["NO"],
        "NOx (NO + NO2)": ["NO", "NO2"],
        "N2O": ["N2O"],
        "NH3": ["NH3"],
        "Amines (total)": ["NH2", "NH", "N2H4", "NH3"],
        "CO": ["CO"],
        "PPMV/Dust (particulates)": ["C", "C2", "C3", "C4", "SOOT", "CARB", "Soot"],
        "Other HAPs (total)": ["CH2O", "HCHO", "C6H14", "C6H6", "Benzene", "Hexane"]
    }

    summary = {}
    for label, species_list in emissions_groups.items():
        total_x = 0.0
        species_found = False
        for sp in species_list:
            if sp in gas.species_names:
                total_x += gas[sp].X[0]
                species_found = True
        if species_found:
            summary[label] = total_x * 1000000  # convert mole fraction to ppm
        else:
            summary[label] = None  # Or "Not available"
    return summary


def display_results(results):

    gas = results.get("gas")  # Make sure your results dict includes gas object after simulation

    if gas is None:
        st.warning("Gas object not found in results — cannot show detailed emissions.")
        return

    # Show basic results as before
    phi = results.get("phi", None)
    if phi is not None:
        st.write(f"**Adiabatic flame temperature at ϕ = {phi:.2f}:** {gas.T:.1f} K")
    st.write(f"**Pressure:** {gas.P / 101325:.2f} atm")

    # Get emissions summary dict
    emissions_summary = get_emissions_summary(gas)

    # Filter out None and build DataFrame
    data = {k: v for k, v in emissions_summary.items() if v is not None}
    df_emissions = pd.DataFrame.from_dict(data, orient='index', columns=['Concentration (ppm)'])

    st.subheader("Key Emissions Summary")
    st.table(df_emissions.style.format("{:.2f}"))

    st.subheader("🧪 Simulation Results")

    # Show summary info
    st.write(f"**Exhaust gas flame temperature at ϕ = {results['phi']:.2f}:** {results['selected']['T']:.1f} K")
    st.write(f"**Pressure:** {results['selected']['P'] / 101325:.2f} atm")

    df = results['df']

    # Choose species to plot
    species_to_plot = ["CO", "NO", "NO2", "SO2", "N2O", "NH3", "Total NOx"]

    # Compute scaling factors to bring all species to similar max height
    max_vals = df[species_to_plot].max()
    target_max = 100
    scaling_factors = {sp: target_max / max_vals[sp] if max_vals[sp] > 0 else 1.0 for sp in species_to_plot}

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each species scaled
    for sp in species_to_plot:
        scaled = df[sp] * scaling_factors[sp]
        ax.plot(df["ϕ"], scaled, label=f"{sp} (×{scaling_factors[sp]:.2g})")

    # Highlight selected phi point
    i = results['selected']['index']
    for sp in species_to_plot:
        ax.plot(df["ϕ"].iloc[i], df[sp].iloc[i] * scaling_factors[sp], 'ro')

    ax.set_xlabel("Equivalence Ratio (ϕ)")
    ax.set_ylabel("Scaled Concentration (ppm × factor)")
    ax.grid(True)
    ax.legend(loc='upper right')

    st.pyplot(fig)



