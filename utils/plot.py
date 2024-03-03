import json

def plot_latency(data_file:str, bandwidth: float, title: str="Unknown") -> None:
    #TODO later
    # load dataset
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    # calc layer-wise latency
    
    # plot it
    pass