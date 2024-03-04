import json
from . import load_profiler
from .nprofile import *
import matplotlib.pyplot as plt
from deployment import neurosurgeon

def plot_latency(data_file:str, bandwidth: float, title: str="Unknown") -> None:
    # load dataset
    with open(data_file, 'r') as file:
        data = json.load(file)
        minfo = load_profiler.load_profile(data)
    
    # calc layer-wise latency
    data = []
    for index in range(len(minfo)):
        _, result = neurosurgeon.calc_latency(minfo, index, bandwidth)
        data.append(result)
    edge, cloud, upload = zip(*data)
    x = [i for i in range(len(minfo))]
    # plot it
    plt.bar(x, edge, label='Edge Latency')
    plt.bar(x, upload, bottom=edge, label='Upload Latency')
    plt.bar(x, cloud, bottom=[edge[i] + upload[i] for i in range(len(minfo))], label='Cloud Latency')
    plt.ylim(top=max([edge[i] + upload[i] + cloud[i] for i in range(len(minfo))]) * 1.2)
    plt.legend()
    plt.savefig(f'images/{title}.svg')
    plt.cla()
    
