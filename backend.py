"""Simulación de una cola M/M/c mediante eventos discretos."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class QueueResult:
    arrivals: np.ndarray
    starts: np.ndarray
    departures: np.ndarray
    waiting_times: np.ndarray
    service_times: np.ndarray
    utilization: float


def simulate_queue(arrival_rate: float, service_rate: float, servers: int,
                   customers: int, seed: int = 42) -> QueueResult:
    if arrival_rate <= 0 or service_rate <= 0 or servers < 1:
        raise ValueError("Tasas positivas y al menos un servidor son necesarias.")
    if customers < 10 or customers > 100_000:
        raise ValueError("El número de clientes debe estar entre 10 y 100 000.")
    if arrival_rate >= servers * service_rate:
        raise ValueError("La cola no es estable: λ debe ser menor que c·μ.")
    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.exponential(1 / arrival_rate, customers))
    service = rng.exponential(1 / service_rate, customers)
    available = np.zeros(servers, dtype=float)
    starts = np.empty(customers, dtype=float)
    departures = np.empty(customers, dtype=float)
    for index, arrival in enumerate(arrivals):
        server = int(np.argmin(available))
        starts[index] = max(arrival, available[server])
        departures[index] = starts[index] + service[index]
        available[server] = departures[index]
    waiting = starts - arrivals
    utilization = float(service.sum() / (departures[-1] * servers))
    return QueueResult(arrivals, starts, departures, waiting, service, min(utilization, 1.0))
