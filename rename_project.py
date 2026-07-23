import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD_NAME = "game_template"


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <new-project-name>")
        sys.exit(1)

    new_name = sys.argv[1].strip()
    if not new_name:
        print("error: project name cannot be empty")
        sys.exit(1)

    package_json = ROOT / "package.json"
    index_html = ROOT / "index.html"

    with open(package_json, "r") as f:
        pkg = json.load(f)

    old_name = pkg.get("name", "")
    if old_name == OLD_NAME:
        print(f"  package.json: name  {old_name} -> {new_name}")
    else:
        print(
            f"  package.json: name  {old_name} -> {new_name}  (was '{old_name}', not '{OLD_NAME}')"
        )

    pkg["name"] = new_name
    with open(package_json, "w") as f:
        json.dump(pkg, f, indent=4)
        f.write("\n")

    with open(index_html, "r") as f:
        html = f.read()

    for tag_name in (OLD_NAME, old_name):
        old_title = f"<title>{tag_name}</title>"
        if old_title in html:
            html = html.replace(old_title, f"<title>{new_name}</title>")
            with open(index_html, "w") as f:
                f.write(html)
            print(f"  index.html:  title {tag_name} -> {new_name}")
            break
    else:
        print(f"  index.html:  title -> {new_name}  (no <title> found)")

    print(f"\nDone. Project renamed to '{new_name}'.")


if __name__ == "__main__":
    main()
