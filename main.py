print("Helloooooooo WORLD I am a genius!")
import psutil
import time

def get_cpu_temperature():
    """
    Read CPU temperature directly from Linux sysfs.
    This is the most reliable method for Raspberry Pi.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_c = int(f.read().strip()) / 1000.0
        return temp_c
    except FileNotFoundError:
        return 0.0

def bytes_to_gb(bytes_value):
    """
    Helper function to convert bytes to Gigabytes (GB).
    """
    return bytes_value / (1024 ** 3)

def monitor_system():
    print("=====================================================================")
    print("             Raspberry Pi 5 Real-time System Monitor                 ")
    print("                (Press Ctrl + C to stop gracefully)                  ")
    print("=====================================================================")
    
    try:
        # The main infinite loop for continuous monitoring
        while True:
            # Get current timestamp (Hour:Minute:Second)
            current_time = time.strftime("%H:%M:%S")
            
            # 1. CPU Metrics (interval=1 blocks execution for 1 second)
            cpu_usage = psutil.cpu_percent(interval=1)
            temp = get_cpu_temperature()
            
            # 2. RAM (Memory) Metrics
            ram = psutil.virtual_memory()
            ram_used_gb = bytes_to_gb(ram.used)
            ram_total_gb = bytes_to_gb(ram.total)
            
            # 3. Storage (Disk) Metrics 
            # We check the root partition '/' to see the main SD card/NVMe usage
            disk = psutil.disk_usage('/')
            disk_used_gb = bytes_to_gb(disk.used)
            disk_total_gb = bytes_to_gb(disk.total)

            # Print the formatted log line in a clean, single-row layout
            print(
                f"[{current_time}] "
                f"CPU: {cpu_usage:4.1f}% ({temp:.1f}°C) | "
                f"RAM: {ram.percent:4.1f}% ({ram_used_gb:.1f}/{ram_total_gb:.1f}GB) | "
                f"Disk: {disk.percent:4.1f}% ({disk_used_gb:.1f}/{disk_total_gb:.1f}GB)"
            )
            
            # Pause for 2 seconds before the next reading to reduce overhead
            time.sleep(2)
            
    except KeyboardInterrupt:
        # Catch the Ctrl+C signal for a clean exit without throwing ugly errors
        print("\n=====================================================================")
        print(" [!] Interruption signal received. Monitor exited gracefully. Bye! ")
        print("=====================================================================")

if __name__ == "__main__":
    monitor_system()