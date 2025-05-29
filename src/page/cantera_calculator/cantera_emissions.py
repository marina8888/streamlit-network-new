import cantera as ct
import streamlit as st
from .run_simulation import run_simulation
from .ui import get_user_inputs, display_results
import io

def run():
    st.title("🔥 Combustion & Emissions Simulator")

    if "results" not in st.session_state:
        st.session_state.results = None

    user_inputs = get_user_inputs()

    run_sim = st.button("▶ Run Simulation", key="run-sim")
    reset = st.button("🔄 Reset", key="reset")

    if run_sim:
        # Create a string buffer
        cantera_log = io.StringIO()
        # Redirect Cantera logs to this buffer
        ct.use_logfile(cantera_log)

        with st.spinner("Running simulation..."):
            st.session_state.results = run_simulation(user_inputs)
            st.session_state.results["phi"] = user_inputs["phi"]

        # Get the log output
        cantera_output = cantera_log.getvalue()

        # Show the output in Streamlit
        st.subheader("📋 Cantera Output")
        st.code(cantera_output, language="text")

    if st.session_state.results:
        display_results(st.session_state.results)

    if reset:
        st.session_state.results = None
        st.experimental_rerun()
