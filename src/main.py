import pypsa
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static

def tester():
    # Create a new PyPSA network
    n = pypsa.Network()

    # Create buses (representing locations/sites)
    n.add("Bus", "Site_A")  # Power site A
    n.add("Bus", "Site_B")  # Power site B
    n.add("Bus", "Site_C")  # Power site C

    # Define generation capacities (MW) at each site
    n.add("Generator", "gen_A", bus="Site_A", p_nom=100, marginal_cost=50)  # Site A produces 100 MW
    n.add("Generator", "gen_B", bus="Site_B", p_nom=200, marginal_cost=60)  # Site B produces 200 MW
    n.add("Generator", "gen_C", bus="Site_C", p_nom=150, marginal_cost=55)  # Site C produces 150 MW

    # Add loads (demand) for each site (e.g., industrial consumption)
    n.add("Load", "load_A", bus="Site_A", p_set=80)  # Site A demands 80 MW
    n.add("Load", "load_B", bus="Site_B", p_set=180)  # Site B demands 180 MW
    n.add("Load", "load_C", bus="Site_C", p_set=120)  # Site C demands 120 MW

    # Hydrogen Pipeline (Link between Site_A and Site_C)
    n.add("Link", "hydrogen_pipeline", bus0="Site_A", bus1="Site_C", efficiency=0.8, p_nom=150, marginal_cost=10)

    # Gas Pipeline (Link between Site_B and Site_C)
    n.add("Link", "gas_pipeline", bus0="Site_B", bus1="Site_C", efficiency=0.9, p_nom=200, marginal_cost=15)

    # Add an industrial load that will be supplied by these links
    n.add("Load", "industrial_load", bus="Site_C", p_set=200)

    # Streamlit display section
    st.title("PyPSA Network with Hydrogen and Gas Pipelines")

    # Show basic information about generators and links (pipelines)
    st.subheader("💡 Generator Details")
    st.write("Site A Generator Output:", n.generators.loc["gen_A", "p_nom"])
    st.write("Site B Generator Output:", n.generators.loc["gen_B", "p_nom"])
    st.write("Site C Generator Output:", n.generators.loc["gen_C", "p_nom"])

    # Show links (pipelines) between the sites
    st.subheader("💨 Pipeline Details")
    st.write("Hydrogen Pipeline Capacity (MW):", n.links.loc["hydrogen_pipeline", "p_nom"])
    st.write("Gas Pipeline Capacity (MW):", n.links.loc["gas_pipeline", "p_nom"])

    # ----------------------------- Map Visualization -------------------------------

    # Coordinates for the sites (you can adjust these coordinates)
    site_coords = {
        "Site_A": [51.5074, -0.1278],  # Example coordinates (London)
        "Site_B": [52.2053, 0.1218],   # Example coordinates (Cambridge)
        "Site_C": [53.4808, -2.2426]   # Example coordinates (Manchester)
    }

    # Initialize the map centered on the UK
    m = folium.Map(location=[52.0, -0.1], zoom_start=6)

    # Add markers for each site
    for site, coords in site_coords.items():
        folium.Marker(
            location=coords,
            popup=f"{site}",
            icon=folium.Icon(color="blue", icon="cloud")
        ).add_to(m)

    # Display map in Streamlit
    st.subheader("🗺️ Map of Power Sites")
    st.write("Map showing power generation sites.")
    folium_static(m)

if __name__ == "__main__":
    tester()
