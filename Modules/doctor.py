import psutil
import socket
import time
import urllib.request
from Modules.colors import cyan, green, red, yellow, bold

PASS = green("[PASS]")
WARN = yellow("[WARN]")
FAIL = red("[FAIL]")


def check_internet():
    start = time.time()
    try:
        # Quick ping-like check to Google's public DNS
        with urllib.request.urlopen("https://1.1.1.1", timeout=3):
            latency = int((time.time() - start) * 1000)
            return True, f"Internet connected (latency: {latency} ms)", None
    except Exception:
        return False, "No internet connection detected.", "Check your Wi-Fi or run 'network ping 8.8.8.8'"


def check_cpu():
    usage = psutil.cpu_percent(interval=0.5)
    if usage > 85:
        return False, f"CPU usage is critically high ({usage}%)", "Run 'process list' to see which app is overloading the CPU."
    elif usage > 70:
        return "WARN", f"CPU usage is moderately elevated ({usage}%)", None
    return True, f"CPU usage is normal ({usage}%)", None


def check_memory():
    mem = psutil.virtual_memory()
    free_gb = mem.available / (1024 ** 3)
    if mem.percent > 90:
        return False, f"RAM is almost full ({mem.percent}% used, only {free_gb:.1f} GB free)", "Run 'process list' to find memory-heavy apps."
    elif mem.percent > 75:
        return "WARN", f"RAM usage is high ({mem.percent}% used)", None
    return True, f"Memory is healthy ({mem.percent}% used, {free_gb:.1f} GB available)", None


def check_disks():
    issues = []
    for p in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(p.mountpoint)
            free_percent = 100 - usage.percent
            if free_percent < 10:
                issues.append(f"Drive {p.device} has only {free_percent:.1f}% space remaining!")
        except PermissionError:
            continue

    if issues:
        return False, "Low disk space detected: " + ", ".join(issues), "Free up space or check 'system storage'"
    return True, "All storage drives have plenty of free space", None


def check_battery():
    bat = psutil.sensors_battery()
    if bat is None:
        return True, "No battery (Desktop / AC powered)", None

    if not bat.power_plugged and bat.percent < 20:
        return "WARN", f"Battery low ({bat.percent}%) and not plugged in!", "Plug in your charger soon."
    
    status = "Charging" if bat.power_plugged else "On Battery"
    return True, f"Battery healthy ({bat.percent}%, {status})", None

def doctor_command(arguments=None):
    print(cyan(bold("\n--- TermKit System Doctor ---")))
    print("Running automated health diagnostics...\n")

    checks = [
        ("Network & Internet", check_internet),
        ("Processor (CPU)", check_cpu),
        ("Memory (RAM)", check_memory),
        ("Storage (Disks)", check_disks),
        ("Battery / Power", check_battery)
    ]

    passed_count = 0
    warnings_count = 0
    failed_count = 0
    recommendations = []

    for name, func in checks:
        status, message, advice = func()
        
        if status is True:
            badge = PASS
            passed_count += 1
        elif status == "WARN":
            badge = WARN
            warnings_count += 1
        else:
            badge = FAIL
            failed_count += 1

        print(f"  {badge} {bold(name)}: {message}")
        if advice:
            recommendations.append(advice)

    print("\n" + "-" * 50)
    print(f"Summary: {green(str(passed_count))} Passed | {yellow(str(warnings_count))} Warnings | {red(str(failed_count))} Critical")

    if recommendations:
        print(f"\n{yellow(bold('Doctor Recommendations:'))}")
        for r in recommendations:
            print(f"  * {r}")
    else:
        print(f"\n{green(bold('All systems operational! Your PC is in great shape.'))}")
    print()