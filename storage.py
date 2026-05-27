import json
from pathlib import Path

def load_data(path: Path):

    if not path.exists():
        return None

    with open(path, "r") as file:
        return json.load(file)

def save_data(data, path: Path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)