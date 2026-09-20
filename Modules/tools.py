import os
import json
import hashlib
import base64
import uuid
import secrets
import string
import urllib.parse
from Modules.colors import cyan, green, red, yellow, bold

def tool_json(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} tools json <file_path or json_string>")
        return

    target = " ".join(arguments)

    if os.path.isfile(target):
        try:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"{red('Invalid JSON in file:')} {e}")
            return
    else:
        try:
            data = json.loads(target)
        except Exception as e:
            print(f"{red('Invalid JSON string:')} {e}")
            return

    formatted = json.dumps(data, indent=4)
    print(f"\n{green(bold('Valid JSON:'))}\n{formatted}\n")


def tool_hash(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} tools hash <file_path or text>")
        return

    target = " ".join(arguments)

    if os.path.isfile(target):
        print(f"\n{bold('Calculating hashes for file:')} {cyan(target)}")
        try:
            with open(target, "rb") as f:
                content = f.read()
        except Exception as e:
            print(f"{red('Error reading file:')} {e}")
            return
    else:
        content = target.encode("utf-8")
        print(f"\n{bold('Calculating hashes for text:')} {cyan(repr(target))}")

    md5 = hashlib.md5(content).hexdigest()
    sha1 = hashlib.sha1(content).hexdigest()
    sha256 = hashlib.sha256(content).hexdigest()

    print(f"  {bold('MD5:   ')} {md5}")
    print(f"  {bold('SHA1:  ')} {sha1}")
    print(f"  {bold('SHA256:')} {cyan(sha256)}\n")


def tool_b64(arguments):
    if len(arguments) < 2 or arguments[0].lower() not in ["encode", "decode"]:
        print(f"{yellow('Usage:')} tools b64 <encode/decode> <text>")
        return

    action = arguments[0].lower()
    text = " ".join(arguments[1:])

    try:
        if action == "encode":
            encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            print(f"\n{bold('Base64 Encoded:')} {green(encoded)}\n")
        else:
            decoded = base64.b64decode(text.encode("utf-8")).decode("utf-8")
            print(f"\n{bold('Base64 Decoded:')} {green(decoded)}\n")
    except Exception as e:
        print(f"{red('Base64 Error:')} {e}")


def tool_uuid(arguments=None):
    new_uuid = str(uuid.uuid4())
    print(f"\n{bold('Generated UUIDv4:')} {cyan(new_uuid)}\n")


def tool_password(arguments):
    length = int(arguments[0]) if len(arguments) > 0 and arguments[0].isdigit() else 16
    length = max(8, min(length, 128))

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = "".join(secrets.choice(alphabet) for _ in range(length))

    print(f"\n{bold(f'Secure Password ({length} chars):')} {green(password)}\n")


def help_command():
    print(f"\n{bold('Developer Tools:')}")
    print(f"  {cyan('tools json <file/string>'):<30} - Validate and pretty-print JSON")
    print(f"  {cyan('tools hash <file/string>'):<30} - Generate MD5, SHA1, SHA256 checksums")
    print(f"  {cyan('tools b64 <encode/decode> <text>'):<30} - Base64 encode or decode text")
    print(f"  {cyan('tools uuid'):<30} - Generate a unique UUIDv4")
    print(f"  {cyan('tools pass [length]'):<30} - Generate a cryptographically secure password")
    print(f"  {cyan('tools help'):<30} - Show this help menu\n")


def tools_command(arguments):
    if len(arguments) == 0 or arguments[0].lower() == "help":
        help_command()
        return

    sub = arguments[0].lower()

    tool_dispatch = {
        "json": tool_json,
        "hash": tool_hash,
        "b64":  tool_b64,
        "uuid": tool_uuid,
        "pass": tool_password,
        "password": tool_password,
        "help": help_command
    }

    if sub in tool_dispatch:
        tool_dispatch[sub](arguments[1:])
    else:
        print(f"{red('Unknown tool:')} '{sub}'. Type '{cyan('tools help')}' for available utilities.")
