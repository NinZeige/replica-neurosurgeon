import torch
from torch import nn
from torch.profiler import profile, record_function
import json

SIZE_DUMP = 'size.json'
TRACE_DUMP = 'chrome.json'
LOCAL_LAT = 'local_lat'
REMOTE_LAT = 'remote_lat'

def profile_flatten(model: nn.Module, input: torch.Tensor, label:str) -> torch.Tensor:
    '''
    Profile the flatten network
    '''
    size_record = {}
    with torch.no_grad():
        with profile(
            record_shapes=True,
            profile_memory=True,
        ) as prof:
            out = input
            for name, layer in model.named_children():
                with record_function(name):
                    out:torch.Tensor = layer(out)
                    # record output shape
                    info = {
                        'size': out.numel() * 4,    # assume all with float32 dtype
                    }
                    size_record[name] = info
    print(prof.key_averages().table(sort_by="cpu_time", top_level_events_only=False))
    prof.export_chrome_trace(TRACE_DUMP)

    with open(TRACE_DUMP, 'r') as file:
        trace_data:list = json.load(file)['traceEvents']
        assert type(trace_data) == list
    
    # read from chrome profile
    for entry in trace_data:
        key = entry['name']
        if key in size_record:
            size_record[key]['local_lat'] = entry['dur']
        
    save_name = f'{label}_{SIZE_DUMP}'
    with open(save_name, 'w') as file:
        json.dump(size_record, file, indent=4)
    return out
