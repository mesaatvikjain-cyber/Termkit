import os

# This enables ANSI color rendering in Windows Command Prompt & PowerShell
os.system('')

class Colors:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    
    # Bright Colors
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

# Quick helper functions so you can just write green("text") or red("text")
def cyan(text):   return f"{Colors.CYAN}{text}{Colors.RESET}"
def green(text):  return f"{Colors.GREEN}{text}{Colors.RESET}"
def red(text):    return f"{Colors.RED}{text}{Colors.RESET}"
def yellow(text): return f"{Colors.YELLOW}{text}{Colors.RESET}"
def bold(text):   return f"{Colors.BOLD}{text}{Colors.RESET}"