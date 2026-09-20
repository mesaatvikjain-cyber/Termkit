import sys
import code
import subprocess
from Modules.colors import cyan, green, red, yellow, bold
def py_eval(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} python eval <expression> (e.g. python eval 2**16 or python eval [x for x in range(5)])")
        return

    expr = " ".join(arguments)
    try:
        # Evaluate standard math and Python expressions safely
        result = eval(expr, {"__builtins__": __builtins__})
        print(f"{green('Result:')} {result} ({type(result).__name__})")
    except Exception as e:
        print(f"{red('Eval Error:')} {e}")
def py_repl(arguments=None):
    print(cyan(bold("\n--- TermKit Python Scratchpad ---")))
    print(f"Interactive Python {sys.version.split()[0]}. Type '{yellow('exit()')}' to return to TermKit.\n")
    
    # code.interact spawns an interactive Python prompt
    code.interact(banner="", local={"sys": sys})
    print(cyan("\nReturned to TermKit.\n"))


def py_run(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} python run <file.py> [args...]")
        return

    script = arguments[0]
    script_args = arguments[1:]

    try:
        cmd = [sys.executable, script] + script_args
        subprocess.run(cmd)
    except Exception as e:
        print(f"{red('Failed to run script:')} {e}")

def py_info(arguments=None):
    print(f"\n{bold('Python Environment:')}")
    print(f"  Version:    {sys.version.split()[0]}")
    print(f"  Executable: {sys.executable}")
    print(f"  Platform:   {sys.platform}")
    print()

def help_command(arguments=None):
    print(f"\n{bold('Python Commands:')}")
    print(f"  {cyan('eval <expression>'):<20} - Evaluate a one-line Python expression or math")
    print(f"  {cyan('repl'):<20} - Launch interactive Python scratchpad shell")
    print(f"  {cyan('run <file.py>'):<20} - Execute a Python script")
    print(f"  {cyan('info'):<20} - View active Python version & environment details")
    print(f"  {cyan('help'):<20} - Show this help menu\n")


def py_command(arguments):
    # If the user just types "python" with no arguments, launch the REPL!
    if len(arguments) == 0:
        py_repl()
        return

    command = arguments[0].lower()

    py_commands = {
        "eval": py_eval,
        "repl": py_repl,
        "run": py_run,
        "info": py_info,
        "help": help_command
    }

    if command in py_commands:
        py_commands[command](arguments[1:])
    else:
        # Shortcut: if the user typed "python 5 + 5", treat it directly as eval!
        py_eval(arguments)