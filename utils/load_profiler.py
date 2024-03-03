import json
from model_info import ModelInfo

def load_dummy_profile(file: str) -> ModelInfo:
    with open(file, 'r') as f:
        dummy_data = json.load(f)

    data = []
    for entry in dummy_data:
        if not isinstance(entry, (list, tuple)):
            raise ValueError("Each entry in the JSON file must be a list or tuple.")
        if len(entry) not in (3, 4):
            raise ValueError("Each entry must have a length of 3 or 4.")

        data.append(tuple(entry))

    return ModelInfo(data)

def load_chrome_tracing(file: str) -> ModelInfo:
    # pass