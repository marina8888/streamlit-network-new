import streamlit as st
from .run_simulation import run_simulation
from .ui import get_user_inputs, display_results
import io
import contextlib

def run():

    st.title("🔥Combustion & Emissions Simulator")

    # Store results in session state to persist them across rerenders
    if "results" not in st.session_state:
        st.session_state.results = None

    user_inputs = get_user_inputs()

    run_sim = st.button("▶ Run Simulation", key="run-sim")
    reset = st.button("🔄 Reset", key="reset")

    if run_sim:
        # Create a buffer to capture stdout
        stdout_buffer = io.StringIO()

        with st.spinner("Running simulation..."):
            with contextlib.redirect_stdout(stdout_buffer):
                # Run your actual simulation function
                st.session_state.results = run_simulation(user_inputs)
                st.session_state.results["phi"] = user_inputs["phi"]

        # Get the captured output from buffer
        cantera_output = stdout_buffer.getvalue()

        # Show the output in Streamlit
        st.subheader("📋 Cantera Output")
        st.text(cantera_output)

    if st.session_state.results:
        display_results(st.session_state.results)

    if reset:
        st.session_state.results = None
        st.experimental_rerun()

