import os
import sys
import atexit
import subprocess

from Modules.colors import cyan, green, red, yellow, bold
from Modules.system import system_command
from Modules.network import network_command
from Modules.process import process_command
from Modules.files import files_command
from Modules.py_tool import py_command
from Modules.doctor import doctor_command
from Modules.stats import stats_command
from Modules.init_tool import init_command
from Modules.ai import ai_command
from Modules.tools import tools_command
from Modules.git_tool import git_command

# History configuration
HISTORY_FILE = os.path.expanduser("~/.termkit_history")
command_history_list = []
readline = None

def init_history():
    global readline
    try:
        import pyreadline3 as readline
    except ImportError:
        try:
            import readline
        except ImportError:
            readline = None

    if readline and os.path.exists(HISTORY_FILE):
        try:
            readline.read_history_file(HISTORY_FILE)
        except Exception:
            pass

def save_history():
    if readline:
        try:
            readline.write_history_file(HISTORY_FILE)
        except Exception:
            pass

atexit.register(save_history)

def history_command(arguments):
    limit = 20
    if len(arguments) > 0 and arguments[0].isdigit():
        limit = int(arguments[0])

    entries = []
    if readline:
        total = readline.get_current_history_length()
        start = max(1, total - limit + 1)
        for i in range(start, total + 1):
            item = readline.get_history_item(i)
            if item:
                entries.append((i, item))
    else:
        start = max(0, len(command_history_list) - limit)
        entries = list(enumerate(command_history_list[start:], start=start + 1))

    if not entries:
        print(yellow("No command history yet.\n"))
        return

    print(f"\n{bold('Recent Command History:')}")
    for idx, cmd in entries:
        print(f"  {cyan(str(idx).rjust(4))}  {cmd}")
    print()

COMMAND_DESCRIPTIONS = {
    "system":  "Inspect hardware and OS specs (CPU, RAM, storage, OS)",
    "network": "Network diagnostics and connectivity tools (IP, ping)",
    "files":   "File explorer, search, and disk utilities",
    "process": "Monitor, inspect, and terminate running processes",
    "python":  "Interactive Python scratchpad and evaluator",
    "doctor":  "Run automated system diagnostics & health checks",
    "stats":   "Analyze codebase lines of code and language statistics",
    "init":    "Scaffold and generate new project blueprints (python, web, api)",
    "ai":      "Terminal AI assistant connected to custom model / Colab",
    "tools":   "Developer utilities (JSON, Hashes, Base64, UUID, Passwords)",
    "git":     "Git integration (status, branch, log, diff, commit)",
    "history": "Show recent command execution history",
    "clear":   "Clear the terminal screen",
    "exit":    "Exit the TermKit shell",
    "help":    "Show help menu or help on a command (e.g. 'help system')",
}

def help_command(arguments):
    if len(arguments) > 0:
        target = arguments[0].lower()

        if target == "system":
            system_command(["help"])
        elif target == "network":
            network_command(["help"])
        elif target == "process":
            process_command(["help"])
        elif target == "files":
            files_command(["help"])
        elif target == "python":
            py_command(["help"])
        elif target == "doctor":
            doctor_command(["help"])
        elif target == "init":
            init_command(["help"])
        elif target == "ai":
            ai_command(["help"])
        elif target == "tools":
            tools_command(["help"])
        elif target == "git":
            git_command(["help"])
        elif target == "stats":
            print(f"\n{bold('STATS:')}")
            print("  Description: Analyze lines of code, comments, and language distribution.")
            print("  Usage: stats [directory_path]\n")
        elif target == "history":
            print(f"\n{bold('HISTORY:')}")
            print("  Description: View command history. Use Up/Down arrows to cycle commands.")
            print("  Usage: history [limit]\n")
        elif target in COMMAND_DESCRIPTIONS:
            print(f"\n{target.upper()}:")
            print(f"  Description: {COMMAND_DESCRIPTIONS[target]}")
            print(f"  Usage: {target}\n")
        else:
            print(f"Unknown command: '{target}'. Type 'help' to see all available commands.")
        return

    print("\n--- TermKit Available Commands ---")
    for cmd, desc in COMMAND_DESCRIPTIONS.items():
        print(f"  {cmd:<10} - {desc}")
    print("\nTip: Type 'help <command>' for specific subcommand help (e.g., 'help system')\n")

def clear_terminal(arguments):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

def exit_command(arguments):
    save_history()
    print("TermKit exited")
    return True

commands = {
    "help": help_command,
    "exit": exit_command,
    "system": system_command,
    "network": network_command,
    "clear": clear_terminal,
    "process": process_command,
    "files": files_command,
    "python": py_command,
    "doctor": doctor_command,
    "stats": stats_command,
    "init": init_command,
    "ai": ai_command,
    "tools": tools_command,
    "git": git_command,
    "history": history_command
}

def main():
    init_history()
    print(cyan(bold(r"""
  ===========================================
     _____                   _  ___ _   
    |_   _|__ _ __ _ __ ___ | |/ (_) |_ 
      | |/ _ \ '__| '_ ` _ \| ' /| | __|
      | |  __/ |  | | | | | | . \| | |_ 
      |_|\___|_|  |_| |_| |_|_|\_\_|\__|
               The All-in-One CLI Toolkit
  ===========================================
""")))
    print(f"Type '{cyan('help')}' for commands or '{yellow('exit')}' to quit.\n")

    while True:
        prompt = f"{cyan(bold('TermKit'))} {green('/>')} "
        try:
            user_command = input(prompt)
        except KeyboardInterrupt:
            print(yellow("\n^C (Type 'exit' to quit)"))
            continue
        except EOFError:
            break

        user_command_list = user_command.split()

        if len(user_command_list) == 0:
            continue

        command_history_list.append(user_command)

        command = user_command_list[0]
        arguments = user_command_list[1:]

        if command in commands:
            should_exit = commands[command](arguments)
            if should_exit:
                break
        else:
            print(f"{red('Error:')} Unknown command '{user_command}'. Type '{cyan('help')}' for commands.")

if __name__ == "__main__":
    main()
