from pathlib import Path
import json


def get_files(path, suffix):
    processed_dir = Path(path)
    json_files = list(processed_dir.glob(f"*/*{suffix}")) 


def save_json(json_text, path):
    with Path.open(path, "w") as f:
        json.dump(json_text, f)


def read_json_file(path):
    with Path.open(path, "r") as f:
        return json.load(f)
    return None

