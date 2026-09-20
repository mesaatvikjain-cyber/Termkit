import os
import datetime
from pathlib import Path
from Modules.colors import cyan, green, red, yellow, bold
import shutil
CATEGORIES = {
    "Images":    [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
    "Code":      [".py", ".js", ".html", ".css", ".ts", ".c", ".cpp", ".java", ".json", ".sql"],
    "Archives":  [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Media":     [".mp3", ".wav", ".mp4", ".mkv", ".mov"]
}

PROTECTED_FILES = {
    "termkit.py", "readme.md", "requirements.txt", "license", ".env", ".gitignore"
}
def files_arrange(arguments):
    # Check if the user specified "preview" mode
    is_preview = False
    target_dir = "."

    if len(arguments) > 0:
        if arguments[0].lower() == "preview":
            is_preview = True
            target_dir = arguments[1] if len(arguments) > 1 else "."
        else:
            target_dir = arguments[0]

    if not os.path.exists(target_dir):
        print(f"{red('Error:')} Directory '{target_dir}' does not exist.")
        return

    abs_target = os.path.abspath(target_dir)
    print(f"\n{bold('Scanning folder to arrange:')} {cyan(abs_target)}")

    # Plan out the moves
    planned_moves = []  # List of tuples: (source_path, dest_folder, file_name)

    try:
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            
            # 1. Skip directories (we only organize loose files)
            if os.path.isdir(item_path):
                continue
            
            # 2. Skip protected files
            if item.lower() in PROTECTED_FILES:
                continue

            # 3. Determine destination category
            _, ext = os.path.splitext(item)
            ext = ext.lower()

            destination_category = "Other"
            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    destination_category = category
                    break

            planned_moves.append((item_path, destination_category, item))

    except PermissionError:
        print(f"{red('Error:')} Permission denied accessing '{target_dir}'.")
        return

    if not planned_moves:
        print(green("Folder is already clean! No loose unorganized files found.\n"))
        return

    # Print the plan
    print(f"\n{bold('Planned Organization:')}")
    for src, cat, name in planned_moves:
        print(f"  {name}  -->  {cyan(cat + '/')}")
    print("-" * 50)
    print(f"Total files to organize: {len(planned_moves)}")

    # If it's preview mode, stop here!
    if is_preview:
        print(yellow("\n[Preview Mode] No files were moved. Run 'files arrange' without 'preview' to apply.\n"))
        return

    # Ask for user confirmation
    confirm = input(f"\n{bold('Move these')} {len(planned_moves)} {bold('files? (y/N): ')}").strip().lower()
    if confirm != 'y':
        print(yellow("Operation cancelled. No files were touched.\n"))
        return

    # Execute moves safely
    moved_count = 0
    for src, cat, name in planned_moves:
        cat_dir = os.path.join(target_dir, cat)
        os.makedirs(cat_dir, exist_ok=True)
        dest_path = os.path.join(cat_dir, name)

        # Prevent overwriting
        if os.path.exists(dest_path):
            print(f"  {yellow('[SKIP]')} '{name}' already exists in {cat}/")
            continue

        try:
            shutil.move(src, dest_path)
            moved_count += 1
        except Exception as e:
            print(f"  {red('[ERROR]')} Failed to move '{name}': {e}")

    print(green(f"\nSuccessfully arranged {moved_count} file(s) into categorized folders!\n"))

def format_size(bytes_size):
    """Converts raw bytes into human-readable B, KB, MB, GB."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} PB"
def files_list(arguments):
    target_path = arguments[0] if len(arguments) > 0 else "."
    
    if not os.path.exists(target_path):
        print(f"{red('Error:')} Path '{target_path}' does not exist.")
        return

    try:
        entries = sorted(os.listdir(target_path))
    except PermissionError:
        print(f"{red('Error:')} Permission denied reading '{target_path}'.")
        return

    abs_path = os.path.abspath(target_path)
    print(f"\n{bold('Directory:')} {cyan(abs_path)}")
    print(f"  {bold('Type'):<8} {bold('Size'):<12} {bold('Name')}")
    print("  " + "-" * 50)

    for entry in entries:
        full_path = os.path.join(target_path, entry)
        if os.path.isdir(full_path):
            print(f"  {cyan('[DIR]'):<17} {'-':<12} {bold(entry)}")
        else:
            size_str = format_size(os.path.getsize(full_path))
            print(f"  {green('[FILE]'):<17} {size_str:<12} {entry}")
    print()
def files_find(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} files find <pattern> [starting_directory] (e.g. files find .py)")
        return

    pattern = arguments[0].lower()
    start_dir = arguments[1] if len(arguments) > 1 else "."

    print(f"\nSearching for '{pattern}' in {os.path.abspath(start_dir)}...")
    matches = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if pattern in file.lower():
                matches.append(os.path.join(root, file))

    if not matches:
        print(f"No files matching '{pattern}' were found.")
        return

    print(f"Found {len(matches)} matching file(s):")
    for m in matches[:25]:  # Cap at 25 so it doesn't flood the terminal
        print(f"  - {m}")
    if len(matches) > 25:
        print(f"  ...and {len(matches) - 25} more.")
    print()
def files_read(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} files read <file_path> [max_lines] (e.g. files read TermKit.py 20)")
        return

    file_path = arguments[0]
    max_lines = int(arguments[1]) if len(arguments) > 1 and arguments[1].isdigit() else 50

    if not os.path.isfile(file_path):
        print(f"{red('Error:')} '{file_path}' is not a valid file.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            print(f"\n{bold('Viewing:')} {cyan(file_path)} (First {max_lines} lines)\n" + "-" * 50)
            for i, line in enumerate(f, start=1):
                if i > max_lines:
                    print(yellow(f"\n[... truncated at line {max_lines}. Use 'files read <file> <number>' to see more]"))
                    break
                print(f"{cyan(str(i).rjust(4))} | {line.rstrip()}")
            print("-" * 50 + "\n")
    except Exception as e:
        print(f"{red('Error reading file:')} {e}")
def files_info(arguments):
    if len(arguments) == 0:
        print(f"{yellow('Usage:')} files info <path> (e.g. files info TermKit.py)")
        return

    path = arguments[0]
    if not os.path.exists(path):
        print(f"{red('Error:')} '{path}' does not exist.")
        return

    stat = os.stat(path)
    mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    is_dir = os.path.isdir(path)

    print(f"\n{bold('Path:')}     {os.path.abspath(path)}")
    print(f"Type:     {'Directory' if is_dir else 'File'}")
    if not is_dir:
        print(f"Size:     {format_size(stat.st_size)} ({stat.st_size} bytes)")
    print(f"Modified: {mod_time}\n")
def help_command(arguments=None):
    print(f"\n{bold('Files Commands:')}")
    print(f"  {cyan('list [path]'):<20} - List directory contents with sizes")
    print(f"  {cyan('find <pattern> [path]'):<20} - Search files recursively")
    print(f"  {cyan('read <file> [lines]'):<20} - Read text file with line numbers")
    print(f"  {cyan('info <path>'):<20} - Show metadata for file or folder")
    print(f"  {cyan('help'):<20} - Show this help menu\n")
    print(f"  {cyan('arrange [preview] [path]'):<26} - Safely organize loose files into category folders")

def files_command(arguments):
    if len(arguments) == 0:
        help_command()
        return

    command = arguments[0].lower()

    file_commands = {
        "list": files_list,
        "ls": files_list,       # Alias for convenience!
        "find": files_find,
        "read": files_read,
        "info": files_info,
        "help": help_command,
        "arrange": files_arrange
        
    }

    if command in file_commands:
        file_commands[command](arguments[1:])
    else:
        print(f"{red('Unknown files command:')} '{command}'. Type '{cyan('files help')}' for commands.")