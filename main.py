print("Helloooooooo WORLD I am a genius!")
import psutil
import time

def get_cpu_temperature():
    """
    Read CPU temperature directly from Linux sysfs.
    This is the most reliable method for Raspberry Pi.
    """
    try:
        # Linux maps hardware sensors to virtual files in the /sys/ directory.
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            # The raw value is in millidegrees Celsius, so we divide by 1000
            temp_c = int(f.read().strip()) / 1000.0
        return temp_c
    except FileNotFoundError:
        return 0.0

def monitor_system():
    print("======================================")
    print("   Raspberry Pi 5 System Monitor")
    print("======================================")
    
    # 1. CPU Usage
    # interval=1 means it monitors for 1 second to calculate the average usage accurately
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # 2. Memory Usage
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024**3)
    used_gb = memory.used / (1024**3)
    
    # 3. CPU Temperature
    temp = get_cpu_temperature()

    # Print the formatted results
    print(f"CPU Usage:    {cpu_usage}%")
    print(f"Memory Usage: {memory.percent}% ({used_gb:.2f} GB / {total_gb:.2f} GB)")
    print(f"CPU Temp:     {temp:.1f}°C")
    print("======================================")

if __name__ == "__main__":
    monitor_system()
