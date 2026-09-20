import os
from Modules.colors import cyan, green, red, yellow, bold

# Extensions to recognize and their display names
LANGUAGE_EXTENSIONS = {
    ".py":   ("Python", "#"),
    ".js":   ("JavaScript", "//"),
    ".ts":   ("TypeScript", "//"),
    ".html": ("HTML", None),
    ".css":  ("CSS", None),
    ".c":    ("C", "//"),
    ".cpp":  ("C++", "//"),
    ".h":    ("C Header", "//"),
    ".java": ("Java", "//"),
    ".sh":   ("Shell Script", "#"),
    ".bat":  ("Batch Script", "REM"),
    ".ps1":  ("PowerShell", "#"),
    ".md":   ("Markdown", None),
    ".json": ("JSON", None),
    ".yaml": ("YAML", "#"),
    ".yml":  ("YAML", "#"),
    ".sql":  ("SQL", "--"),
}

IGNORED_DIRS = {
    ".git", "__pycache__", "node_modules", "venv", ".venv", "env", ".idea", ".vscode", "dist", "build"
}
def analyze_file(filepath, comment_prefix):
    """Counts code, comments, and blank lines in a file."""
    code_lines = 0
    comment_lines = 0
    blank_lines = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif comment_prefix and stripped.startswith(comment_prefix):
                    comment_lines += 1
                else:
                    code_lines += 1
    except Exception:
        return 0, 0, 0

    return code_lines, comment_lines, blank_lines
def stats_command(arguments):
    target_dir = arguments[0] if len(arguments) > 0 else "."

    if not os.path.exists(target_dir):
        print(f"{red('Error:')} Directory '{target_dir}' does not exist.")
        return

    abs_target = os.path.abspath(target_dir)
    print(f"\n{bold('Analyzing Codebase:')} {cyan(abs_target)}...\n")

    # language_name -> {'files': int, 'code': int, 'comments': int, 'blank': int}
    lang_stats = {}

    for root, dirs, files in os.walk(target_dir):
        # In-place modify dirs to avoid entering ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            if ext in LANGUAGE_EXTENSIONS:
                lang_name, comment_prefix = LANGUAGE_EXTENSIONS[ext]
                file_path = os.path.join(root, file)

                code_cnt, comm_cnt, blank_cnt = analyze_file(file_path, comment_prefix)

                if lang_name not in lang_stats:
                    lang_stats[lang_name] = {'files': 0, 'code': 0, 'comments': 0, 'blank': 0}

                lang_stats[lang_name]['files'] += 1
                lang_stats[lang_name]['code'] += code_cnt
                lang_stats[lang_name]['comments'] += comm_cnt
                lang_stats[lang_name]['blank'] += blank_cnt

    if not lang_stats:
        print(yellow("No recognizable source code files found in this directory.\n"))
        return

    # Print Table Header
    print(f"  {bold('Language'):<16} {bold('Files'):<8} {bold('Code'):<10} {bold('Comments'):<10} {bold('Blank'):<8} {bold('Total')}")
    print("  " + "=" * 65)

    total_files = 0
    total_code = 0
    total_comments = 0
    total_blank = 0

    # Sort languages by lines of code descending
    sorted_langs = sorted(lang_stats.items(), key=lambda item: item[1]['code'], reverse=True)

    for lang, data in sorted_langs:
        tot = data['code'] + data['comments'] + data['blank']
        total_files += data['files']
        total_code += data['code']
        total_comments += data['comments']
        total_blank += data['blank']

        print(f"  {cyan(lang):<25} {data['files']:<8} {data['code']:<10} {data['comments']:<10} {data['blank']:<8} {tot}")

    grand_total = total_code + total_comments + total_blank
    print("  " + "-" * 65)
    print(f"  {bold('Total'):<16} {total_files:<8} {green(str(total_code)):<19} {yellow(str(total_comments)):<19} {total_blank:<8} {bold(str(grand_total))}")
    print("  " + "=" * 65)

    # Visual Language Distribution Bar
    if total_code > 0:
        print(f"\n{bold('Code Distribution:')}")
        for lang, data in sorted_langs:
            percent = (data['code'] / total_code) * 100
            if percent >= 1.0:
                bar_len = int(percent / 5)  # 20 blocks = 100%
                bar = "=" * bar_len + "-" * (20 - bar_len)
                print(f"  {lang:<14} [{cyan(bar)}] {percent:>5.1f}%")
    print()