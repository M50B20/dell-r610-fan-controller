# Dell R610 - Dynamic Thermal Control (IPMI/Python)

Dynamic thermal control daemon for Dell PowerEdge R610 servers using IPMI and Python.

## The Problem
The Dell PowerEdge R610 is an excellent server for homelabs, but its default thermal management (iDRAC) is extremely aggressive. At the slight increase in load, the fans ramp up significantly, generating deafening noise and unnecessary power consumption. 

Conversely, manually locking the fan speed at a low percentage via IPMI is a dangerous practice: under sustained load, the processors risk hardware overheating.

## The Solution
This project provides a lightweight systemd daemon written in Python. It reads the temperature of each CPU core in real-time and dynamically adjusts the fan speeds using raw IPMI commands based on predefined thermal thresholds.

**Built-in Failsafe:** If any single core reaches or exceeds 70°C (or if a sensor reading fails), the script instantly hands control back to the hardware iDRAC controller (Auto Mode) to protect the CPU.

---

## Prerequisites
* A Dell PowerEdge server (tested on R610, Dual Xeon E5645).
* A Debian-based OS or hypervisor (tested on Proxmox VE).
* The `ipmitool` and `lm-sensors` packages.

```bash
apt update && apt install ipmitool lm-sensors -y
sensors-detect --auto
