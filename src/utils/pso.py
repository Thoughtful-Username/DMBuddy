from pathlib import Path
import json

def generate_pso(project_root: str, output_file: str):
    root = Path(project_root)
    with open(output_file, "w") as f:
        f.write(f"{root.name}/\n")
        for path in root.rglob("*"):
            if path.is_dir() and not path.name.startswith("."):
                f.write(f"{'│   ' * path.relative_to(root).parent.parts.count('/')}{path.name}/\n")
            elif path.is_file() and not path.name.endswith((".pyc", ".pyo")):
                f.write(f"{'│   ' * path.relative_to(root).parent.parts.count('/')}{path.name}\n")

if __name__ == "__main__":
    generate_pso(".", "DMBuddyy.txt")