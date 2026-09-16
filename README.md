# Simulador de colas de espera

Aplicación Streamlit para simular una cola M/M/c con llegadas y tiempos de servicio exponenciales, varios servidores y atención FCFS.

## Funciones

- Configura tasa de llegada `λ`, tasa de servicio `μ`, servidores y número de clientes.
- Estima tiempos de espera, tiempo en el sistema y utilización.
- Muestra histograma de esperas y una gráfica de llegadas/salidas.
- Rechaza configuraciones inestables (`λ ≥ cμ`).

## Estructura

```text
.
├── backend.py       # Simulación de eventos discretos
├── frontend.py      # Controles y resultados
├── requirements.txt
└── README.md
```

## Instalación y ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```

En macOS o Linux, activa el entorno con `source .venv/bin/activate`.

## Uso

Ajusta los parámetros en la barra lateral. La tasa total de servicio es `cμ`; para una cola estable se requiere `λ < cμ`. La simulación es aleatoria, por lo que los promedios se acercan a sus valores teóricos al aumentar el número de clientes.
