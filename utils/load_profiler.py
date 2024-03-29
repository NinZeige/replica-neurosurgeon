import json
from .model_info import ModelInfo
from .nprofile import *

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

def merge_profile(edge:dict, cloud: dict) -> dict:
    merged = edge.copy()
    for entry in edge.keys():
        if entry not in cloud:
            print(f'Warning: cloud dictionary doesn\'t contain key "{entry}"')
            continue
        merged[entry][REMOTE_LAT] = cloud[entry][LOCAL_LAT]
    return merged

def load_profile(data: dict[str,dict]) -> ModelInfo:
    tmp = {}
    for key in data.keys():
        num = key[:key.find('--')]
        local_lat = data[key][LOCAL_LAT]
        remote_lat = data[key][REMOTE_LAT]
        size = data[key][NPRO_SIZE]
        tmp[int(num)] = (local_lat, remote_lat, size)
    result = []
    for i in range(len(data)):
        result.append(tmp[i])
    return ModelInfo(result)