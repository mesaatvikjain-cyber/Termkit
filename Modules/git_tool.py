import subprocess
import os
from Modules.colors import cyan, green, red, yellow, bold

def run_git(args):
    """Executes a git command and returns (success, stdout, stderr)."""
    try:
        res = subprocess.run(["git"] + args, capture_output=True, text=True, errors="replace")
        return res.returncode == 0, res.stdout, res.stderr
    except FileNotFoundError:
        return False, "", "Git is not installed or not in PATH."

def check_git_repo():
    ok, stdout, stderr = run_git(["rev-parse", "--is-inside-work-tree"])
    if not ok:
        if "not a git repository" in stderr.lower():
            print(f"{yellow('Notice:')} Current directory is not a Git repository.")
            print(f"Run {cyan('git init')} in your terminal to initialize a repository here.\n")
        else:
            print(f"{red('Git Error:')} {stderr.strip()}\n")
        return False
    return True

def git_status(arguments):
    if not check_git_repo():
        return

    ok, branch, _ = run_git(["branch", "--show-current"])
    current_branch = branch.strip() if ok else "unknown"

    print(f"\n{bold('Git Repository Status')} (Branch: {green(current_branch)}):")

    ok, out, err = run_git(["status", "--short"])
    if not ok:
        print(f"{red('Error:')} {err}")
        return

    lines = out.strip().splitlines()
    if not lines or (len(lines) == 1 and not lines[0]):
        print(f"  {green('Clean working tree')} - nothing to commit!\n")
        return

    for line in lines:
        if len(line) < 3:
            continue
        staged = line[0]
        unstaged = line[1]
        filename = line[3:]

        if staged == "?" and unstaged == "?":
            print(f"  {red('[Untracked]')}  {filename}")
        elif staged in ["M", "A", "D", "R"]:
            print(f"  {green('[Staged]   ')}  {filename} ({staged})")
        elif unstaged in ["M", "D"]:
            print(f"  {yellow('[Modified] ')}  {filename}")
        else:
            print(f"  {cyan('[' + line[:2] + ']')}     {filename}")
    print()


def git_branch(arguments):
    if not check_git_repo():
        return

    ok, out, err = run_git(["branch", "-a"])
    if not ok:
        print(f"{red('Error:')} {err}")
        return

    print(f"\n{bold('Branches:')}")
    for line in out.strip().splitlines():
        if line.startswith("*"):
            print(f"  {green(line)}")
        else:
            print(f"  {line}")
    print()


def git_log(arguments):
    if not check_git_repo():
        return

    limit = "5"
    if len(arguments) > 0 and arguments[0].isdigit():
        limit = arguments[0]

    fmt = "%C(yellow)%h%Creset | %C(green)%ad%Creset | %s %C(cyan)[%an]%Creset"
    ok, out, err = run_git(["log", f"-n{limit}", f"--pretty=format:{fmt}", "--date=short"])

    if not ok:
        print(f"{yellow('No commits found in this repository yet.')}\n")
        return

    print(f"\n{bold(f'Recent {limit} Commits:')}")
    print("  " + out.replace("\n", "\n  "))
    print()


def git_diff(arguments):
    if not check_git_repo():
        return

    ok, out, err = run_git(["diff", "--stat"])
    if not ok:
        print(f"{red('Error:')} {err}")
        return

    if not out.strip():
        print(green("\nNo unstaged changes detected.\n"))
        return

    print(f"\n{bold('Modified Files Summary:')}")
    print(out)


def git_add(arguments):
    if not check_git_repo():
        return

    targets = arguments if len(arguments) > 0 else ["."]
    ok, out, err = run_git(["add"] + targets)
    if ok:
        print(green(f"Staged {', '.join(targets)} for commit.\n"))
    else:
        print(f"{red('Error:')} {err}\n")


def git_commit(arguments):
    if not check_git_repo():
        return

    if len(arguments) == 0:
        print(f"{yellow('Usage:')} git commit <commit message>")
        return

    msg = " ".join(arguments)
    ok, out, err = run_git(["commit", "-m", msg])
    if ok:
        print(green(f"Committed successfully:\n{out}"))
    else:
        print(f"{red('Commit failed:')} {err or out}\n")


def help_command():
    print(f"\n{bold('Git Integration Commands:')}")
    print(f"  {cyan('git status'):<25} - Show staged, unstaged, and untracked files with badges")
    print(f"  {cyan('git branch'):<25} - List local and remote branches")
    print(f"  {cyan('git log [limit]'):<25} - Show pretty commit history (default 5)")
    print(f"  {cyan('git diff'):<25} - Show stats of modified files")
    print(f"  {cyan('git add [files]'):<25} - Stage files (defaults to '.' for all)")
    print(f"  {cyan('git commit <msg>'):<25} - Commit staged changes with message")
    print(f"  {cyan('git help'):<25} - Show this help menu\n")


def git_command(arguments):
    if len(arguments) == 0:
        git_status([])
        return

    sub = arguments[0].lower()

    git_dispatch = {
        "status": git_status,
        "st":     git_status,
        "branch": git_branch,
        "log":    git_log,
        "diff":   git_diff,
        "add":    git_add,
        "commit": git_commit,
        "help":   lambda _: help_command()
    }

    if sub in git_dispatch:
        git_dispatch[sub](arguments[1:])
    else:
        # Fallback: pass through standard git commands directly!
        ok, out, err = run_git(arguments)
        if out:
            print(out)
        if err:
            print(f"{red(err)}")
