def load_api_key(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()
