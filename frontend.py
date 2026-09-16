"""Interfaz Streamlit para simular una cola de espera M/M/c."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from backend import simulate_queue


st.set_page_config(page_title="Simulador de colas", page_icon="⏱️", layout="wide")
st.title("Simulador de colas de espera")
st.write("Simula clientes que llegan al azar y reciben servicio en una cola M/M/c.")

with st.sidebar:
    arrival_rate = st.number_input("Tasa de llegada λ (clientes/unidad de tiempo)", min_value=0.01, value=4.0, step=0.5)
    service_rate = st.number_input("Tasa de servicio μ por servidor", min_value=0.01, value=5.0, step=0.5)
    servers = st.slider("Número de servidores c", 1, 10, 1)
    customers = st.slider("Clientes simulados", 100, 20000, 3000, 100)
    seed = st.number_input("Semilla aleatoria", min_value=0, value=42, step=1)

try:
    result = simulate_queue(arrival_rate, service_rate, servers, customers, int(seed))
except ValueError as error:
    st.error(str(error))
    st.stop()

waiting = result.waiting_times
system_time = result.departures - result.arrivals
metrics = st.columns(4)
metrics[0].metric("Espera media", f"{np.mean(waiting):.3f}")
metrics[1].metric("Espera mediana", f"{np.median(waiting):.3f}")
metrics[2].metric("Tiempo medio en sistema", f"{np.mean(system_time):.3f}")
metrics[3].metric("Utilización simulada", f"{result.utilization:.1%}")

left, right = st.columns(2)
with left:
    fig, axis = plt.subplots(figsize=(7, 4.5))
    axis.hist(waiting, bins=35, color="tab:blue", alpha=0.8)
    axis.set(title="Distribución del tiempo de espera", xlabel="Tiempo", ylabel="Clientes")
    axis.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
with right:
    displayed = min(customers, 1000)
    frame = pd.DataFrame({"Cliente": np.arange(displayed), "Llegada": result.arrivals[:displayed], "Salida": result.departures[:displayed]})
    st.subheader("Llegadas y salidas (primeros clientes)")
    st.line_chart(frame.set_index("Cliente"))

st.caption(f"Utilización teórica aproximada: λ/(c·μ) = {arrival_rate / (servers * service_rate):.1%}. Los resultados varían con la semilla y el tamaño de muestra.")
