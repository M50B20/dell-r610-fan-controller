import subprocess
import time

# --- Configuration des paliers ---
# < 50°C : 15% (0x0f) -> Silence
# < 60°C : 20% (0x14) -> Léger souffle
# < 70°C : 30% (0x1e) -> Audible mais préventif
# >= 70°C : AUTO -> Urgence, reprise iDRAC

def get_max_core_temp():
    """Récupère la température maximale parmi tous les cœurs CPU."""
    try:
        cmd = "sensors | grep 'Core' | awk '{print $3}' | tr -d '+°C'"
        output = subprocess.check_output(cmd, shell=True, text=True)
        temps = [float(t) for t in output.strip().split('\n') if t]
        return max(temps) if temps else 40.0
    except Exception:
        return 75.0 # Failsafe : force le mode AUTO en cas d'erreur de lecture

def set_fan_speed(auto=False, speed_hex="0x14"):
    """Envoie les instructions IPMI au contrôleur matériel."""
    if auto:
        subprocess.run(["ipmitool", "raw", "0x30", "0x30", "0x01", "0x01"], capture_output=True)
    else:
        subprocess.run(["ipmitool", "raw", "0x30", "0x30", "0x01", "0x00"], capture_output=True)
        subprocess.run(["ipmitool", "raw", "0x30", "0x30", "0x02", "0xff", speed_hex], capture_output=True)

def main():
    current_state = ""

    while True:
        temp = get_max_core_temp()

        if temp >= 70.0:
            if current_state != "AUTO":
                set_fan_speed(auto=True)
                current_state = "AUTO"
        else:
            if temp < 50.0:
                target_hex = "0x0f" # 15%
            elif temp < 60.0:
                target_hex = "0x14" # 20%
            else:
                target_hex = "0x1e" # 30%

            if current_state != target_hex:
                set_fan_speed(auto=False, speed_hex=target_hex)
                current_state = target_hex

        time.sleep(10)

if __name__ == "__main__":
    main()
