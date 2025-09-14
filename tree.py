import os

def save_repo_tree(output_file: str = "repo_tree.txt") -> None:
    exclude = {".git", ".venv", "venv", "__pycache__", "node_modules",
               "dist", "build", "archive/attachments"}

    with open(output_file, "w", encoding="utf-8") as f:
        for root, dirs, files in os.walk(".", topdown=True):
            # odfiltruj katalogi do pominięcia
            dirs[:] = [d for d in dirs if d not in exclude]

            # wypisz katalog
            level = root.count(os.sep)
            indent = " " * 2 * level
            f.write(f"{indent}{os.path.basename(root) or '.'}/\n")

            # wypisz pliki w katalogu
            for file in files:
                f.write(f"{indent}  {file}\n")

if __name__ == "__main__":
    save_repo_tree()
    print("✅ Zapisano strukturę repo do repo_tree.txt")
