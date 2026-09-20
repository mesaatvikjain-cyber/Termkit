import os
from Modules.colors import cyan, green, red, yellow, bold

PYTHON_GITIGNORE = """__pycache__/
*.py[cod]
*$py.class
venv/
.venv/
env/
.env
.idea/
.vscode/
dist/
build/
"""

PYTHON_MAIN = '''def main():
    print("Hello from your new project!")

if __name__ == "__main__":
    main()
'''

WEB_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Project</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Welcome to My Project</h1>
        <p>Built with TermKit Project Scaffolder.</p>
        <button id="btn">Click Me</button>
    </div>
    <script src="app.js"></script>
</body>
</html>
'''

WEB_CSS = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #0f172a;
    color: #f8fafc;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    text-align: center;
    padding: 2rem;
    background: #1e293b;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}

h1 {
    margin-bottom: 1rem;
    color: #38bdf8;
}

button {
    margin-top: 1.5rem;
    padding: 0.75rem 1.5rem;
    background: #38bdf8;
    color: #0f172a;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

button:hover {
    background: #0284c7;
}
'''

WEB_JS = '''document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("btn");
    btn.addEventListener("click", () => {
        alert("Hello from TermKit Web Starter!");
    });
});
'''

API_MAIN = '''from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Welcome to your API",
        "version": "1.0.0"
    })

@app.route("/health")
def health():
    return jsonify({"health": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
def create_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
def scaffold_python(project_dir, project_name):
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "tests"), exist_ok=True)

    create_file(os.path.join(project_dir, "src", "__init__.py"), "")
    create_file(os.path.join(project_dir, "src", "main.py"), PYTHON_MAIN)
    create_file(os.path.join(project_dir, "tests", "__init__.py"), "")
    create_file(os.path.join(project_dir, "tests", "test_main.py"), "# Write your unit tests here\n")
    create_file(os.path.join(project_dir, "requirements.txt"), "# Add your pip dependencies here\n")
    create_file(os.path.join(project_dir, ".gitignore"), PYTHON_GITIGNORE)
    create_file(os.path.join(project_dir, "README.md"), f"# {project_name}\n\nProject initialized with TermKit.\n\n## Running\n```bash\npython src/main.py\n```\n")


def scaffold_web(project_dir, project_name):
    create_file(os.path.join(project_dir, "index.html"), WEB_HTML)
    create_file(os.path.join(project_dir, "style.css"), WEB_CSS)
    create_file(os.path.join(project_dir, "app.js"), WEB_JS)
    create_file(os.path.join(project_dir, "README.md"), f"# {project_name}\n\nFrontend starter initialized with TermKit.\nOpen `index.html` in your browser to view.\n")


def scaffold_api(project_dir, project_name):
    create_file(os.path.join(project_dir, "main.py"), API_MAIN)
    create_file(os.path.join(project_dir, "requirements.txt"), "flask>=3.0.0\n")
    create_file(os.path.join(project_dir, ".gitignore"), PYTHON_GITIGNORE)
    create_file(os.path.join(project_dir, "README.md"), f"# {project_name} API\n\nRun:\n```bash\npip install -r requirements.txt\npython main.py\n```\n")

TEMPLATES = {
    "python": ("Full Python project with src, tests, .gitignore, requirements.txt", scaffold_python),
    "web":    ("Modern HTML5, CSS3 & JavaScript starter project", scaffold_web),
    "api":    ("Flask REST API starter with / and /health routes", scaffold_api)
}

def help_command():
    print(f"\n{bold('Project Scaffolder (init):')}")
    print(f"  {cyan('init <template> <project_name>'):<32} - Create a new starter project")
    print(f"  {cyan('init list'):<32} - List all available templates")
    print(f"  {cyan('init help'):<32} - Show this help menu\n")


def init_command(arguments):
    if len(arguments) == 0 or arguments[0].lower() == "help":
        help_command()
        return

    if arguments[0].lower() == "list":
        print(f"\n{bold('Available Templates:')}")
        for t_name, (t_desc, _) in TEMPLATES.items():
            print(f"  {cyan(t_name):<10} - {t_desc}")
        print(f"\nUsage: {cyan('init <template> <project_name>')}\n")
        return

    if len(arguments) < 2:
        print(f"{yellow('Usage:')} init <template> <project_name> (e.g. init python my_app)")
        print(f"Type '{cyan('init list')}' to see templates.")
        return

    template = arguments[0].lower()
    project_name = arguments[1]

    if template not in TEMPLATES:
        print(f"{red('Error:')} Unknown template '{template}'. Type '{cyan('init list')}' for available templates.")
        return

    if os.path.exists(project_name):
        print(f"{red('Error:')} A folder named '{project_name}' already exists in this directory.")
        return

    print(f"\nInitializing new {cyan(template)} project in {bold(project_name)}...")
    os.makedirs(project_name, exist_ok=True)

    _, scaffold_func = TEMPLATES[template]
    try:
        scaffold_func(project_name, project_name)
        print(green(f"Successfully generated {bold(project_name)}!"))
        print(f"  --> Run '{cyan(f'files list {project_name}')}' to explore your new blueprint.\n")
    except Exception as e:
        print(f"{red('Failed to scaffold project:')} {e}")