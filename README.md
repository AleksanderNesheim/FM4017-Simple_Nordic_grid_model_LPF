# FM4017-Project

This GitHub repository is part of a submission in the **FM4017 – Project** course at the **University of South-Eastern Norway (USN)**.

The repository provides the necessary files to use a **simplified network model of the Nordic Synchronous Grid**, developed for educational and methodological purposes.

---

## Model description

The base network is created using the **PyPSA-eur workflow** and reflects the specifications defined in the provided configuration file.  
The resulting model is a **65-bus representation** of the Nordic synchronous area.

The model is intended for:
- Linear power flow (LPF) studies
- Zonal power flow analysis
- Comparison against reported ENTSO-E data
- Methodological validation of simplified transmission modelling

The model is **not** intended for operational or security studies.

---

## Repository contents

This repository contains:
- A pre-built PyPSA network model of the Nordic synchronous grid
- Helper functions for computing zonal and cross-border flows
- A Jupyter notebook (`workflow.ipynb`) for running LPF simulations and visualising results
- Supporting data files used in the modelling and validation process

---

## Installation and requirements

To use the model, you need a Python environment with the required PyPSA dependencies.

If you do not already have a working PyPSA environment, follow the official installation guide:
https://pypsa-eur.readthedocs.io/en/latest/installation.html#installation

---

## How to run the model

1. Clone this repository
2. Activate your PyPSA-compatible environment
3. Open and run `workflow.ipynb`

This notebook performs:
- Linear power flow (LPF) calculations
- Zonal and cross-border flow extraction
- Network visualisation

This is a **first iteration** of the model. Bugs may occur.  
If you encounter issues, you are encouraged to:
- Modify the workflow or helper functions to fix them, and report the fix
- Or report the issue directly via GitHub without providing a fix

---

## Example output

Running an LPF for a selected date can produce a network plot such as:

<img width="1638" height="1336" alt="Resulting loading and power flow direction after lpf summer heat plot" src="https://github.com/user-attachments/assets/cc871cb5-9a31-4b93-b9da-79da006c1984" />

In this visualisation:
- **Arrows** indicate power flow direction
- **Colour** indicates relative loading of AC lines and HVDC links
- **Line thickness** is correlated with transfer capacity

---

## Modelling assumptions

The following assumptions apply throughout the project:

- Power flows are computed using a **linear (DC) power flow approximation**
- Voltage magnitudes and reactive power are not modelled
- Network topology is fixed (no outages or switching actions)
- Power flow directions are normalised using alphabetical ordering of bidding zones

As a consequence, deviations from reported ENTSO-E AC flows are expected.

---

## Limitations and missing data

Known limitations of the model include:

- The model can only perform LPF due to missing data for some components
- Installed generation capacity per bidding zone is not represented realistically
- Some production technologies are aggregated into the PyPSA carrier **`other`**

The `other` category contains generators that were not placed in the network by the PyPSA-eur workflow.  
These technologies were redistributed evenly among buses in the affected bidding zones.

---

## Validation and interpretation

Model outputs are evaluated using:
- Cross-border flow comparison against ENTSO-E data
- Directional consistency of flows
- Zonal net import/export balances

Percentage deviation metrics are interpreted with care, as small absolute flows can lead to artificially large relative errors.  
Zonal net positions are therefore considered a more robust validation metric.

---

## Citation

If this repository or parts of the model are reused, please cite as:

**FM4017 Project – Simplified Nordic Synchronous Grid Model**  
University of South-Eastern Norway (USN), 2025
