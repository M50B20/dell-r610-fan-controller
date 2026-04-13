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
```

# Installation & Deployment

## 1. Fetch the script
Create the target directory and the logic controller file:

```bash
mkdir -p /opt/scripts
nano /opt/scripts/fan_control.py
```

Copy and paste the contents of the `fan_control.py` file from this repository into your editor.

---

## 2. Set permissions
Secure the script so it can only be modified and executed by root:

```bash
chmod 744 /opt/scripts/fan_control.py
```

---

## 3. Create the Systemd Service
To ensure the script runs in the background and starts automatically on boot:

```bash
nano /etc/systemd/system/dell-fans.service
```

Copy and paste the contents of the `dell-fans.service` file from this repository.

---

## 4. Enable and Start the Daemon

```bash
systemctl daemon-reload
systemctl enable dell-fans.service
systemctl start dell-fans.service
systemctl status dell-fans.service
```

---

## Disclaimer

This script interacts directly with your server's hardware controller. Use it at your own risk.  
The author is not responsible for any hardware damage, overheating, or voided warranties.  
Always monitor your core temperatures carefully during the initial deployment.
