import platform
import psutil
def os_info():
    print(f"Operating system: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")

def storage():
    partitions = psutil.disk_partitions()
    print("Storage Drives:")
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            total_gb = usage.total / (1024 ** 3)
            used_gb = usage.used / (1024 ** 3)
            free_gb = usage.free / (1024 ** 3)
            print(f"\n  Drive {p.device} ({p.fstype}):")
            print(f"    Used:  {used_gb:.2f} GB / {total_gb:.2f} GB ({usage.percent}%)")
            print(f"    Free:  {free_gb:.2f} GB")
        except PermissionError:
            # Some drives (like optical drives) may not be ready
            continue

def cpu():
    print(f"CPU: {platform.processor()}")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Logical cores: {psutil.cpu_count(logical=True)}")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")


import subprocess

def gpu():
    try:
        # Run a quick PowerShell command to fetch GPU name(s)
        cmd = 'powershell -Command "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        gpu_names = result.stdout.strip().splitlines()
        
        if gpu_names:
            print("Graphics Hardware (GPU):")
            for name in gpu_names:
                print(f"  - {name.strip()}")
        else:
            print("No dedicated GPU information found.")
    except Exception as e:
        print(f"Failed to retrieve GPU info: {e}")


def ram():
    memory = psutil.virtual_memory()

    print(f"Total RAM: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Used RAM: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Available RAM: {memory.available / (1024 ** 3):.2f} GB")
    print(f"RAM usage: {memory.percent}%")

def battery():
    bat = psutil.sensors_battery()
    if bat is None:
        print("No battery detected (Desktop PC or virtual machine).")
        return
        
    status = "Charging / Plugged in" if bat.power_plugged else "Discharging (On Battery)"
    print(f"Battery: {bat.percent}%")
    print(f"Status:  {status}")
def help_command():
    print("System commands:")
    print("cpu")
    print("gpu")
    print("ram")
    print("storage")
    print("os")
    print("help")
    print("battery")
    print("uptime")
import time
import datetime

def uptime():
    boot_timestamp = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_timestamp)
    formatted_uptime = str(datetime.timedelta(seconds=uptime_seconds))
    print(f"System Uptime: {formatted_uptime}")

def system_command(arguments):
    if len(arguments) == 0:
        help_command()
        return

    command = arguments[0]

    system_commands = {
        "cpu": cpu,
        "gpu": gpu,
        "ram": ram,
        "help": help_command,
        "os":os_info,
        "storage": storage,
        "battery":battery,
        "uptime":uptime,
    }

    if command in system_commands:
        system_commands[command]()
    else:
        print(f"Unknown system command: {command}")