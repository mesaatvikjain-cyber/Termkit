import psutil
from Modules.colors import cyan, green, red, yellow, bold
def process_list(arguments):
    print(f"\n{bold('Top 10 Processes by Memory Usage:')}")
    print(f"  {bold('PID'):<8} {bold('Name'):<25} {bold('Memory %'):<10} {bold('Status')}")
    print("  " + "-" * 55)

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort processes by memory_percent in descending order
    top_processes = sorted(processes, key=lambda p: p['memory_percent'] or 0, reverse=True)[:10]

    for p in top_processes:
        pid = str(p['pid'])
        name = p['name'][:24] if p['name'] else 'Unknown'
        mem = f"{p['memory_percent']:.1f}%" if p['memory_percent'] else '0.0%'
        status = p['status'] or 'unknown'
        print(f"  {pid:<8} {name:<25} {mem:<10} {status}")
    print()

def process_find(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} process find <process_name> (e.g. process find python)")
        return

    query = arguments[0].lower()
    matches = []

    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            name = proc.info['name']
            if name and query in name.lower():
                matches.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not matches:
        print(f"No running processes found matching '{query}'.")
        return

    print(f"\nFound {len(matches)} matching process(es):")
    print(f"  {bold('PID'):<8} {bold('Name'):<30} {bold('Memory %')}")
    print("  " + "-" * 50)
    for p in matches:
        pid = str(p['pid'])
        name = p['name'][:29]
        mem = f"{p['memory_percent']:.1f}%" if p['memory_percent'] else '0.0%'
        print(f"  {cyan(pid):<17} {name:<30} {mem}")
    print()

def process_kill(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} process kill <pid> (e.g. process kill 1234)")
        return

    try:
        pid = int(arguments[0])
    except ValueError:
        print(f"{red('Error:')} PID must be an integer number.")
        return

    try:
        p = psutil.Process(pid)
        process_name = p.name()
        p.terminate()  # Sends graceful SIGTERM signal
        print(f"{green('Success:')} Terminated process {bold(process_name)} (PID {pid}).")
    except psutil.NoSuchProcess:
        print(f"{red('Error:')} No running process found with PID {pid}.")
    except psutil.AccessDenied:
        print(f"{red('Error:')} Permission denied. You may need to run TermKit as Administrator to kill this process.")
    except Exception as e:
        print(f"{red('Error:')} Failed to kill process: {e}")

def help_command(arguments=None):
    print(f"\n{bold('Process Commands:')}")
    print(f"  {cyan('list'):<12} - Show top 10 processes by memory usage")
    print(f"  {cyan('find <name>'):<12} - Search for processes by name")
    print(f"  {cyan('kill <pid>'):<12} - Terminate a process by its PID")
    print(f"  {cyan('help'):<12} - Show this help menu\n")


def process_command(arguments):
    if len(arguments) == 0:
        help_command()
        return

    command = arguments[0].lower()

    process_commands = {
        "list": process_list,
        "find": process_find,
        "kill": process_kill,
        "help": help_command
    }

    if command in process_commands:
        process_commands[command](arguments[1:])
    else:
        print(f"{red('Unknown process command:')} '{command}'. Type '{cyan('process help')}' for commands.")

        