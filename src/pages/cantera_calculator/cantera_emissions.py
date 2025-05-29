import streamlit as st
from .run_simulation import run_simulation
from .ui import get_user_inputs, display_results

def run():
    st.title("🔥 Cantera Combustion & Emissions Simulator")

    # Store results in session state to persist them across rerenders
    if "results" not in st.session_state:
        st.session_state.results = None

    user_inputs = get_user_inputs()

    run_sim = st.button("▶ Run Simulation", key="run-sim")
    reset = st.button("🔄 Reset", key="reset")

    if run_sim:
        st.session_state.results = run_simulation(user_inputs)
        st.session_state.results["phi"] = user_inputs["phi"]  # 🔧 Add phi to results

    if st.session_state.results:
        display_results(st.session_state.results)

    if reset:
        st.session_state.results = None
        st.experimental_rerun()

