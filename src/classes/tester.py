
import folium
from folium import plugins
from streamlit_folium import folium_static
import streamlit as st
import pypsa
import pandas as pd
import plotly.graph_objects as go

def tester():
       # --- CONFIG ---
    NETWORK_PATH = "src/networks/base_s_5___2030.nc"  # Update this with your greenfield network path
    COUNTRIES = ["GB", "IE", "FR", "DE", "NL", "DK", "NO"]  # Add more as needed

    st.set_page_config(layout="wide")
    st.title("Hydrogen Network – PyPSA-Eur-Sec Greenfield Scenario")

    # --- LOAD NETWORK ---
    @st.cache_resource
    def load_network(path):
        return pypsa.Network(path)

    network = load_network(NETWORK_PATH)

    # --- FILTER HYDROGEN COMPONENTS ---
    # Assume hydrogen pipelines are in links, with carrier = 'H2 pipeline'
    hydrogen_links = network.links[network.links.carrier.str.contains("H2 pipeline", case=False)].copy()
    buses = network.buses.copy()

    # Merge coordinates from buses
    hydrogen_links = hydrogen_links.merge(buses[["x", "y"]], left_on="bus0", right_index=True, suffixes=("", "_from"))
    hydrogen_links = hydrogen_links.merge(buses[["x", "y"]], left_on="bus1", right_index=True, suffixes=("", "_to"))

    # --- PLOT HYDROGEN NETWORK MAP ---
    fig = go.Figure()

    # Plot pipelines
    for _, row in hydrogen_links.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[row["x"], row["x_to"]],
            lat=[row["y"], row["y_to"]],
            mode="lines",
            line=dict(width=2, color="green"),
            hoverinfo="text",
            name=row["carrier"],
            text=f'{row.name} ({row["p_nom"]:.2f} MW)'
        ))

    # Plot hydrogen-related buses (with H2 carriers)
    h2_buses = buses[buses.carrier.str.contains("H2", case=False, na=False)].copy()
    fig.add_trace(go.Scattergeo(
        lon=h2_buses["x"],
        lat=h2_buses["y"],
        mode="markers",
        marker=dict(size=6, color="blue"),
        text=h2_buses.index,
        name="H2 Nodes",
        hoverinfo="text"
    ))

    # Layout setup
    fig.update_layout(
        geo=dict(
            resolution=50,
            showland=True,
            landcolor="rgb(240, 240, 240)",
            showcountries=True,
            countrycolor="gray",
            projection_type="mercator",
            lonaxis_range=[-12, 30],
            lataxis_range=[45, 65]
        ),
        height=700,
        title="Hydrogen Pipelines and Nodes in Europe",
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # --- DISPLAY IN STREAMLIT ---
    st.plotly_chart(fig, use_container_width=True)

    # Optional: show data
    if st.checkbox("Show hydrogen pipeline table"):
        st.dataframe(hydrogen_links[["carrier", "bus0", "bus1", "p_nom"]])
