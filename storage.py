import json
import os

class JsonStore:
    def __init__(self, filename="data.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
