import pandas as pd
import cantera as ct
import numpy as np
def select_mechanism(fuels):
    fuels = set(fuels) - {'None'}
    if any(f in fuels for f in ['CH4', 'C2H6', 'C3H8', 'H2', 'CO']):
        return "gri.yaml"  # Natural gas, hydrogen, syngas
    elif 'NH3' in fuels:
        return "kovaleva9.yaml"
    elif 'DME' in fuels:
        return "dme_mech.yaml"
    elif any(f in fuels for f in ['C2H5OH', 'biodiesel', 'butanol']):
        return "creck.yaml"
    else:
        raise KeyError("No mechanism selected")
    return "gri.yaml"  # Default fallback



def run_simulation(inputs):
    fuel_mix = inputs.get("fuel_mix", {})
    oxid = inputs.get("oxid", "O2:1.0, N2:3.76")
    phi_target = inputs.get("phi", 1.0)
    T_in = inputs.get("T_in", 300)
    P_atm = inputs.get("P_atm", 1)
    dust_ppm = inputs.get("dust_ppm", 0.0)
    sulfur_ppm = inputs.get("sulfur_ppm", 0.0)

    fuels = list(fuel_mix.keys())
    mech_file = select_mechanism(fuels)
    gas = ct.Solution(f"resources/mech/{mech_file}")

    phi_range = np.arange(0.5, 2.05, 0.05)
    data = {
        "ϕ": [],
        "CO": [],
        "NO": [],
        "NO2": [],
        "SO2": [],
        "N2O": [],
        "NH3": [],
        "Total NOx": [],
    }

    selected_gas = None
    selected_index = None

    for i, phi in enumerate(phi_range):
        # Compose fuel string
        fuel_str = ",".join([f"{f}:{frac}" for f, frac in fuel_mix.items()])
        gas.set_equivalence_ratio(phi, fuel_str, oxid)
        gas.TP = T_in, P_atm * ct.one_atm

        # Equilibrate at constant HP to simulate adiabatic flame conditions
        gas.equilibrate("HP")

        def ppm(species):
            return gas[species].X[0] * 1e6 if species in gas.species_names else 0.0

        data["ϕ"].append(phi)
        data["CO"].append(ppm("CO"))
        data["NO"].append(ppm("NO"))
        data["NO2"].append(ppm("NO2"))
        data["SO2"].append(ppm("SO2"))
        data["N2O"].append(ppm("N2O"))
        data["NH3"].append(ppm("NH3"))
        data["Total NOx"].append(ppm("NO") + ppm("NO2"))

        if abs(phi - phi_target) < 1e-3:
            selected_gas = gas
            selected_index = i

    df = pd.DataFrame(data)

    results = {
        "df": df,
        "selected": {
            "index": selected_index,
            "T": selected_gas.T if selected_gas else None,
            "P": selected_gas.P if selected_gas else None,
        },
        "gas": selected_gas,
        "phi": phi_target
    }

    return results

