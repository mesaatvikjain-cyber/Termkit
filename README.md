# TermKit ⚡
> The Modern, All-in-One Developer & System Shell Toolkit.

TermKit is a unified terminal companion designed to replace dozens of one-off scripts, bookmarks, and system monitors. It brings hardware diagnostics, network auditing, process management, safe file organization, live code statistics, project scaffolding, cloud-connected AI, and developer utilities right into one sleek, interactive CLI.

---

## ✨ Features

- 🖥️ **System Diagnostics (`system`)**: Real-time inspection of CPU, multi-drive storage, GPU (via CIM), RAM, battery status, system uptime, and OS kernel specs.
- 🌐 **Network Toolkit (`network`)**: Public & local IP fetcher, ping tester, DNS domain resolver, TCP port scanner, and HTTP latency checker.
- ⚙️ **Process Manager (`process`)**: Inspect top memory-hogging processes, find PIDs by keyword, and terminate stuck tasks safely.
- 📁 **File & Disk Suite (`files`)**: Formatted directory explorer, recursive pattern finder, line-numbered file viewer, metadata inspector, and **Safe Folder Organizer (`files arrange`)** with dry-run preview.
- 🩺 **System Doctor (`doctor`)**: Automated 1-click health diagnostics checking connectivity, CPU load, RAM thresholds, and disk exhaustion with smart recommendations.
- 📊 **Codebase Analytics (`stats`)**: Deep project line counter separating real code, comments, and blanks with visual ASCII distribution bars.
- 🚀 **Project Scaffolder (`init`)**: Instant boilerplate generator for full Python packages, modern frontend Web projects, and Flask REST APIs.
- 🤖 **AI Assistant (`ai`)**: Connected client querying custom neural network models (e.g. Qwen2.5) hosted on Google Colab or external endpoints.
- 🛠️ **Developer Utilities (`tools`)**: Instant JSON pretty-printer/validator, SHA256/MD5 hash calculator, Base64 encoder/decoder, UUIDv4 generator, and secure password creator.
- 🌿 **Git Integration (`git`)**: Color-coded branch status, badges for staged/unstaged/untracked files, and compact formatted commit logs.
- ⬆️⬇️ **Smart Shell**: Interactive up/down arrow command history powered by `pyreadline3` and persistent history across sessions (`~/.termkit_history`).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- `psutil`
- `pyreadline3` (for Windows shell history)

```bash
# Clone the repository
git clone https://github.com/mesaatvikjain-cyber/Termkit.git
cd Termkit

# Install dependencies
pip install psutil pyreadline3

# Launch TermKit
python TermKit.py
```

---

## 📖 Command Reference

| Command | Subcommands / Usage | Description |
|---|---|---|
| `system` | `cpu`, `gpu`, `ram`, `storage`, `battery`, `uptime`, `os` | Hardware & operating system metrics |
| `network` | `ip`, `ping <host>`, `dns <domain>`, `port <host> <port>`, `web <url>` | Network connectivity and diagnostics |
| `process` | `list`, `find <name>`, `kill <pid>` | Monitor and manage system processes |
| `files` | `list [path]`, `find <pattern>`, `read <file> [lines]`, `info <path>`, `arrange [preview]` | File management & safe organizer |
| `doctor` | `doctor` | 1-click automated system health checkup |
| `stats` | `stats [path]` | Scan lines of code, comments, and language stats |
| `init` | `init <python/web/api> <name>`, `init list` | Generate project boilerplate architectures |
| `ai` | `ai ask <question>`, `ai explain <file>`, `ai config url <endpoint>` | Query custom AI models / Colab server |
| `tools` | `json <input>`, `hash <file/text>`, `b64 <encode/decode>`, `uuid`, `pass [len]` | Formatters, crypto hashes, Base64, UUIDs |
| `git` | `status`, `branch`, `log [n]`, `diff`, `add`, `commit <msg>` | Git repository management with colored badges |
| `python` | `eval <expr>`, `repl`, `run <file>`, `info` | Quick math evaluator, interactive REPL scratchpad |
| `history` | `history [limit]` | Display recent command history |
| `clear` | `clear` | Clear terminal screen cross-platform |
| `exit` | `exit` | Exit TermKit |

---

## 🧠 Training & Connecting TermKit AI

TermKit AI can be connected to any LLM. You can host an open-source model like `Qwen/Qwen2.5-0.5B-Instruct` on a free Google Colab GPU via FastAPI & ngrok:

1. Run the Colab notebook script to expose port 8000 via ngrok.
2. In TermKit, link the public endpoint:
   ```bash
   ai config url https://your-tunnel.ngrok-free.dev/generate
   ```
3. Ask questions directly from your terminal:
   ```bash
   ai "how do I reverse a string in python?"
   ```

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
