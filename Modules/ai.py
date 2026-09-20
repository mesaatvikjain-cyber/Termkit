import os
import json
import urllib.request
import urllib.error
from Modules.colors import cyan, green, red, yellow, bold

CONFIG_FILE = ".termkit_ai.json"

DEFAULT_CONFIG = {
    "endpoint": "http://localhost:8000/generate",
    "model_name": "TermKit-Custom-AI"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
OFFLINE_KB = {
    "git": "Git tip: Use 'git status' to check changes, 'git add .' to stage, and 'git commit -m \"message\"' to save.",
    "python": "Python tip: Run 'python repl' right here in TermKit to test snippets interactively!",
    "memory": "System tip: Run 'doctor' or 'process list' to inspect memory hogs on your PC.",
    "network": "Network tip: Use 'network ping 8.8.8.8' to test connectivity or 'network ip' to see your IPs."
}

def offline_fallback(prompt):
    prompt_lower = prompt.lower()
    for keyword, tip in OFFLINE_KB.items():
        if keyword in prompt_lower:
            return f"[Offline AI Assistant]: {tip}"
    return (
        "[Offline Assistant]: Colab model is currently unreachable.\n"
        "To connect your trained Colab model:\n"
        "  1. Start your Colab notebook with ngrok\n"
        "  2. Run: ai config url <your_colab_ngrok_url>/generate"
    )

def query_model(prompt):
    cfg = load_config()
    endpoint = cfg.get("endpoint")

    payload = json.dumps({"prompt": prompt}).encode("utf-8")
    req = urllib.request.Request(
    endpoint,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
        "User-Agent": "TermKit-CLI"
    }
)

    try:
        # Wait up to 15 seconds for Colab GPU to generate output
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # Expecting Colab to return {"response": "..."} or {"text": "..."}
            return data.get("response") or data.get("text") or str(data)
    except urllib.error.HTTPError as e:
        print(f"{red('Server Error:')} {e.code} {e.reason}")
        return None
    except Exception as e:
        print(f"{red('Connection Error:')} {e}")
        return None

def ai_ask(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} ai ask <your question or prompt>")
        return

    prompt = " ".join(arguments)
    print(cyan(f"\nThinking... Sending to AI model...\n"))

    response = query_model(prompt)
    if response:
        print(f"{green(bold('AI Response:'))}\n{response}\n")
    else:
        print(yellow(offline_fallback(prompt)) + "\n")


def ai_explain(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} ai explain <file_path> (e.g. ai explain Modules/colors.py)")
        return

    filepath = arguments[0]
    if not os.path.isfile(filepath):
        print(f"{red('Error:')} File '{filepath}' does not exist.")
        return

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            code_snippet = f.read(2000)  # Read up to first 2000 chars

        prompt = f"Explain what the following code does briefly and clearly:\n\n{code_snippet}"
        ai_ask([prompt])
    except Exception as e:
        print(f"{red('Error reading file:')} {e}")


def ai_config(arguments):
    cfg = load_config()
    if len(arguments) < 2 or arguments[0].lower() != "url":
        print(f"\n{bold('AI Configuration:')}")
        print(f"  Current Model Endpoint: {cyan(cfg.get('endpoint'))}")
        print(f"\nTo update endpoint from Colab:")
        print(f"  {cyan('ai config url <your_ngrok_url>/generate')}\n")
        return

    new_url = arguments[1]


    cfg["endpoint"] = new_url
    save_config(cfg)
    print(green(f"Successfully updated AI model endpoint to: {new_url}\n"))
def help_command():
    print(f"\n{bold('TermKit AI Commands:')}")
    print(f"  {cyan('ai ask <question>'):<28} - Ask your AI model any programming or system question")
    print(f"  {cyan('ai explain <file>'):<28} - Have AI analyze and explain a source code file")
    print(f"  {cyan('ai config [url <link>]'):<28} - View or set your Colab model API endpoint")
    print(f"  {cyan('ai help'):<28} - Show this help menu\n")


def ai_command(arguments):
    if len(arguments) == 0 or arguments[0].lower() == "help":
        help_command()
        return

    sub = arguments[0].lower()

    if sub == "ask":
        ai_ask(arguments[1:])
    elif sub == "explain":
        ai_explain(arguments[1:])
    elif sub == "config":
        ai_config(arguments[1:])
    else:
        # Shortcut: typing 'ai how do I sort in python' automatically calls ask!
        ai_ask(arguments)