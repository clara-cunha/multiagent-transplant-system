# Multi-Agent System for Organ Transplant Management

Academic group project developed for the **Intelligent Systems** course (academic year 2024/2025).

**Team**: [Clara Cunha](https://github.com/clara-cunha), [Manuel Carvalho](https://github.com/Brisingrzzz)
, [Nuno Matos](https://github.com/Nuno-lxm) and Leonor Amorim

**Grade**: 19/20

## Overview

This project implements a **multi-agent system** to simulate and manage organ transplant logistics. The system includes four specialized agents:

- **AT (Transplant Agent)**: Manages organ allocation and fallback strategies.

- **AR (Receiver Agent)**: Handles patient lists and communicates updates.

- **ATR (Transport Agent)**: Simulates organ/patient transport with delays/failures.

- **AH (Hospital Agent)**: Creates patients/organs and manages hospital resources.


Together, these agents cooperate to ensure that transplant decisions are based on:
- Blood type compatibility
- Patient urgency
- Hospital resource availability
- Organ ischemia time
- Transportation time and failure risk


## Technologies

- ![Windows](https://img.shields.io/badge/OS-Windows_11-lightgrey?logo=windows&logoColor=white)
- ![Language](https://img.shields.io/badge/Language-Python_3.9-blue)
- ![Library](https://img.shields.io/badge/Library-SPADE-yellowgreen)
- ![PyCharm](https://img.shields.io/badge/IDE-PyCharm-green)
- ![Protocol](https://img.shields.io/badge/Protocol-XMPP-orange)

## Installation & Usage

1. **Clone the repository**

    ```
    git clone https://github.com/clara-cunha/multiagent-transplant-system

    cd multiagent-transplant-system
    ```

2. **Configure your XMPP credentials**

    Edit the *parameters.py* file with your server credentials:

    ```
    XMPP_SERVER = "your_server"
    PASSWORD = "your_password"
    ```

3. **Start your XMPP server**

    Make sure all agents can connect and communicate.

4. **Run the main script**

    ``` python main.py ```


## Academic Report
The complete academic report (Portuguese only) is available at [relatorio.pdf](relatorio.pdf).

## Acknowledgments
This project was developed as part of the Biomedical Engineering Master’s Program (Medical Informatics branch) at University of Minho.
