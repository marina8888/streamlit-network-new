import streamlit as st
import pypsa
import pandas as pd
def tester():
    st.title("🔗 Sector Coupling: Electricity ↔ Heat")

    # User inputs
    electric_demand = st.slider("Electricity Demand (MW)", 10, 100, 50)
    heat_demand = st.slider("Heat Demand (MW)", 10, 100, 50)
    cop = st.slider("Heat Pump COP (Coefficient of Performance)", 1.0, 5.0, 3.0)

    # Build network
    n = pypsa.Network()

    # Add buses
    n.add("Bus", "electric")
    n.add("Bus", "heat", carrier="heat")

    # Add generator
    n.add("Generator", "gen", bus="electric", p_nom=200, marginal_cost=50)

    # Add electric load
    n.add("Load", "electric_load", bus="electric", p_set=electric_demand)

    # Add heat load
    n.add("Load", "heat_load", bus="heat", p_set=heat_demand)

    # Add heat pump (link)
    n.add("Link", "heat_pump",
          bus0="electric",  # from electricity
          bus1="heat",      # to heat
          efficiency=cop,
          p_nom=200,
          marginal_cost=10)

    # Run linear optimal power flow (LOPF)
    n.lopf()

    # Results
    st.subheader("💡 Results")
    st.write("Electric Generator Output (MW):", n.generators_t.p["gen"].values[0])
    st.write("Heat Pump Electricity Use (MW):", n.links_t.p0["heat_pump"].values[0])
    st.write("Heat Supplied by Heat Pump (MW):", n.links_t.p1["heat_pump"].values[0])

    # Optional: Show full dataframe
    with st.expander("See Full Results"):
        st.write("Generators:")
        st.dataframe(n.generators_t.p)
        st.write("Links:")
        st.dataframe(n.links_t.p0)
