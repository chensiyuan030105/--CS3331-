import json

class Storage:
    def __init__(self, file_name='data.json'):
        self.file_name = file_name

    def save_data(self, data):
        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open(self.file_name, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
