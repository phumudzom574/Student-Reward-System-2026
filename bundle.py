import os

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "env", "__pycache__",
             ".idea", ".vscode", "build", "dist", "migrations"}
EXTENSIONS = {".py", ".txt", ".md", ".json", ".html", ".css", ".js",
              ".yml", ".yaml", ".toml", ".ini", ".cfg", ".sql", ".env.example"}
OUTPUT = "project_bundle.txt"

with open(OUTPUT, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in (OUTPUT, "bundle.py"):
                continue
            if os.path.splitext(name)[1].lower() not in EXTENSIONS:
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue
            out.write(f"\n {path}\n{content}\n")

print("Done! Created", OUTPUT)