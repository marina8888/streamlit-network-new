import streamlit as st
import cantera as ct
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("🔥 Cantera Combustion & Emissions Simulator")

    # Sidebar: Inputs
    st.sidebar.header("Input Conditions")

    fuel = st.sidebar.selectbox("Fuel", ['CH4', 'C2H6', 'H2', 'CO', 'C3H8'])
    oxidizer = st.sidebar.selectbox("Oxidizer", ['Air', 'O2'])
    equiv_ratio = st.sidebar.slider("Equivalence Ratio (ϕ)", 0.5, 2.0, 1.0, 0.05)
    T_in = st.sidebar.slider("Initial Temperature (K)", 300, 1500, 300, 50)
    P_atm = st.sidebar.slider("Pressure (atm)", 1, 20, 1)
    dust_ppm = st.sidebar.number_input("Dust concentration (ppm)", min_value=0.0, value=10.0, step=1.0)
    show_composition = st.sidebar.checkbox("Show top 10 composition chart", value=True)

    # Action buttons
    run_sim = st.button("▶ Run Simulation")
    reset = st.button("🔄 Reset")

    # Perform simulation only when "Run" is clicked
    if run_sim:
        # Cantera setup
        gas = ct.Solution("gri30.yaml")
        oxid = "O2:1.0, N2:3.76" if oxidizer == "Air" else "O2:1.0"
        gas.set_equivalence_ratio(equiv_ratio, f"{fuel}:1", oxid)
        gas.TP = T_in, P_atm * ct.one_atm
        gas.equilibrate("HP")  # Adiabatic equilibrium

        st.subheader("🧪 Simulation Results")
        st.write(f"**Adiabatic flame temperature:** {gas.T:.1f} K")
        st.write(f"**Pressure:** {gas.P / ct.one_atm:.2f} atm")

        # Convert to ppm (mole fraction × 1e6)
        ppm = lambda x: gas[x].X[0] * 1e6

        emissions = {
            "CO": ppm("CO"),
            "NO": ppm("NO"),
            "NO₂": ppm("NO2"),
            "SO₂": ppm("SO2") if "SO2" in gas.species_names else 0,
            "Dust (user input)": dust_ppm,
            "Total NOx": ppm("NO") + ppm("NO2"),
        }

        df_emissions = pd.DataFrame(emissions.items(), columns=["Species", "Concentration (ppm)"])
        st.subheader("💨 Emissions")
        st.dataframe(df_emissions.set_index("Species").style.format("{:.2f}"))

        # Show top 10 species composition
        if show_composition:
            st.subheader("Composition: Top 10 Species")
            mole_fracs = pd.Series(gas.X, index=gas.species_names)
            top_species = mole_fracs[mole_fracs > 1e-5].sort_values(ascending=False).head(10)

            fig, ax = plt.subplots()
            top_species.plot(kind="bar", ax=ax)
            ax.set_ylabel("Mole Fraction")
            st.pyplot(fig)

    # Reset = clear state (in Streamlit, this is handled by re-running with default values)
    if reset:
        st.experimental_rerun()
