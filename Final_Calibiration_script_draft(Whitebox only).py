import os
import yaml
import wntr
import pandas as pd



CM = 0.01
MM = 0.001

INITIAL_MAIN_TANK_LEVEL = 100 * CM
MAX_MAIN_TANK_LEVEL = 1000 * CM
MAIN_TANK_DIAMETER = 100 * CM

DEFAULT_PIPE_LENGTH = 154 * CM
SMALL_PIPE_DIAMETER = 20 * MM
BIG_PIPE_DIAMETER = 50 * MM

DEFAULT_PIPE_ELEVATION = 75 * CM
TANK_TO_PUMP_PIPE_ELEVATION = 10 * CM
TANK_TO_PUMP_PIPE_LENGTH = 100 * CM

HW_EXPONENT = 0.54
ALPHA = 0.5   # damping factor for roughness updates



with open("parameter_values.yml") as f:
    params = yaml.safe_load(f)



wn = wntr.network.WaterNetworkModel()
wn.options.hydraulic.headloss = "HW"

# ---- Tank ----
wn.add_tank(
    "Main_Tank",
    init_level=INITIAL_MAIN_TANK_LEVEL,
    max_level=MAX_MAIN_TANK_LEVEL,
    diameter=MAIN_TANK_DIAMETER,
    overflow=False,
    coordinates=(20, 20)
)

# ---- Junctions ----
wn.add_junction("J1", elevation=TANK_TO_PUMP_PIPE_ELEVATION)
wn.add_junction("J2", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J3", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J4", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J5", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J6", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J7", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J8", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J9", elevation=DEFAULT_PIPE_ELEVATION)
wn.add_junction("J10", elevation=DEFAULT_PIPE_ELEVATION)

# ---- Pipes ----
wn.add_pipe("M1", "Main_Tank", "J1", TANK_TO_PUMP_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("M2", "J2", "J3", TANK_TO_PUMP_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("M3", "J3", "J4", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)

wn.add_pipe("P1", "J4", "J5", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("P2", "J5", "J6", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("P3", "J6", "J7", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("P4", "J7", "J8", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("P5", "J8", "J5", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER, initial_status="CLOSED")
wn.add_pipe("P6", "J8", "J9", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("P7", "J9", "J10", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
wn.add_pipe("P8", "J10", "Main_Tank", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)

# ---- Pump ----
wn.add_pump("Main_Pump", "J1", "J2", pump_type="HEAD", pump_curve_name="MainPumpCurve")



for pid, pdata in params.get("pipes", {}).items():
    if pid in wn.link_name_list:
        link = wn.get_link(pid)
        if link.link_type == "Pipe":
            link.roughness = pdata.get("roughness", link.roughness)
            link.minor_loss = pdata.get("minor_loss", link.minor_loss)



pump_curve = params["pumps"]["Main_Pump"]["head_curve"]
a = pump_curve["a"]
b = pump_curve["b"]

Q = [0.0, 0.01, 0.02]  # m3/s
H = [a - b*q*q for q in Q]

wn.add_curve("MainPumpCurve", "HEAD", list(zip(Q, H)))


sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()


sim_flows = results.link["flowrate"].iloc[0]
sim_df = sim_flows.reset_index()
sim_df.columns = ["pipe_id", "sim_flow"]
sim_df.to_csv("sim_flows.csv", index=False)



actual_df = pd.read_csv("actual_flows.csv")
merged = actual_df.merge(sim_df, on="pipe_id", how="inner")

merged["error"] = merged["sim_flow"] - merged["flow"]
merged["rel_error"] = merged["error"] / merged["flow"]

print("\nFLOW COMPARISON:")
print(merged[["pipe_id", "flow", "sim_flow", "rel_error"]])




for _, row in merged.iterrows():
    pid = row["pipe_id"]

    if pid in params["pipes"]:
        Qm = row["flow"]
        Qs = row["sim_flow"]

        if Qm > 0 and Qs > 0:
            C_old = params["pipes"][pid]["roughness"]
            C_new = C_old * (Qm / Qs) ** (1 / HW_EXPONENT)
            C_new = ALPHA * C_new + (1 - ALPHA) * C_old
            params["pipes"][pid]["roughness"] = float(C_new)



with open("parameter_values.yml", "w") as f:
    yaml.safe_dump(params, f)

print("\nCalibration iteration complete.")
