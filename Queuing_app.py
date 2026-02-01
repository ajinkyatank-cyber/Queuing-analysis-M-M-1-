import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="M/M/1 Queue Calculator", layout="centered")

st.title("M/M/1 Queue Calculator")
st.caption("Compute standard M/M/1 performance measures and state probabilities (Pn) using textbook formulas.")

st.markdown("### Inputs")

col1, col2 = st.columns(2)

with col1:
    lam = st.number_input("Average arrival rate, λ (per hour)", min_value=0.0, value=12.0, step=0.5, format="%.4f")
with col2:
    service_time_min = st.number_input("Average service time (minutes per customer)", min_value=0.0, value=4.0, step=0.5, format="%.4f")

st.markdown("### Probability settings")
col3, col4 = st.columns(2)
with col3:
    n_exact = st.number_input("n for P(n customers in system)", min_value=0, value=3, step=1)
with col4:
    n_max = st.number_input("Show probability table up to n =", min_value=0, value=15, step=1)

# Convert service time to mu per hour
mu = (60.0 / service_time_min) if service_time_min > 0 else float("inf")

st.divider()
st.markdown("### Results")

if service_time_min <= 0:
    st.error("Average service time must be greater than 0.")
elif lam <= 0 and lam != 0:
    st.error("Arrival rate must be non-negative.")
else:
    # Stability check
    if mu == float("inf"):
        st.warning("Service time is extremely small; μ is very large. Results may be trivial.")
    if lam >= mu and mu != float("inf"):
        st.error(
            f"Unstable system: λ ≥ μ (λ = {lam:.4f}, μ = {mu:.4f} per hour). "
            "M/M/1 steady-state formulas require λ < μ."
        )
    else:
        rho = 0.0 if mu == float("inf") else (lam / mu if mu > 0 else float("nan"))

        # Textbook formulas (Model 1 style)
        # P0, Pn
        P0 = 1 - rho
        def Pn(n: int) -> float:
            return (1 - rho) * (rho ** n)

        # Ls, Lq, Ws, Wq
        if lam == 0:
            Ls = 0.0
            Lq = 0.0
            Ws = 0.0
            Wq = 0.0
        else:
            Ls = lam / (mu - lam)  # Ls
            Lq = (lam ** 2) / (mu * (mu - lam))  # Lq
            Ws = Ls / lam  # Ws (hours)
            Wq = Lq / lam  # Wq (hours)

        # Display headline metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Service rate, μ (per hour)", f"{mu:.4f}")
        m2.metric("Utilization, ρ", f"{rho:.4f}")
        m3.metric("P0 (system empty)", f"{P0:.4f}")

        st.markdown("#### Performance measures (averages)")
        df = pd.DataFrame(
            {
                "Measure": ["Ls (avg. in system)", "Lq (avg. waiting)", "Ws (avg. time in system)", "Wq (avg. waiting time)"],
                "Value": [Ls, Lq, Ws, Wq],
                "Units": ["customers", "customers", "hours", "hours"],
                "Value (minutes)": [
                    "—",
                    "—",
                    Ws * 60 if isinstance(Ws, (int, float)) else "—",
                    Wq * 60 if isinstance(Wq, (int, float)) else "—",
                ],
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("#### State probabilities")
        pn_exact = Pn(int(n_exact))
        st.write(f"**P(N = {int(n_exact)}) = (1 − ρ) ρ^{int(n_exact)} = {pn_exact:.6f}**")

        # Probability table
        rows = []
        for n in range(int(n_max) + 1):
            rows.append({"n": n, "P(N = n)": Pn(n)})
        dfp = pd.DataFrame(rows)
        dfp["P(N = n)"] = dfp["P(N = n)"].map(lambda x: f"{x:.6f}")
        st.dataframe(dfp, use_container_width=True, hide_index=True)

        st.markdown("#### Notes")
        st.markdown(
            "- These formulas assume an **M/M/1** queue in steady state: Poisson arrivals, exponential service, single server.\n"
            "- Ensure **λ < μ** for the steady-state measures to be valid.\n"
            "- Units: if λ is per hour and service time is in minutes, the app converts μ to per hour and reports times in hours (and minutes for convenience)."
        )
