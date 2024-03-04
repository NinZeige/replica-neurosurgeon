from utils import model_info

def algo_neurosurgeon(minfo: model_info.ModelInfo, bandwidth: float, target: str = 'latency', upload_power: float = 0) -> int:
    """
    Perform the Neurosurgeon algorithm with the given info. Only the partition point is returned.

        Parameters:
    - minfo: The ModelInfo of the target DNN. Edge latency, cloud latency, and layer-wise data size are sufficient to perform the algorithm.
    - bandwidth: Bandwidth in bytes per second.
    - target: Optimization target, either 'latency' or 'energy'.
    - upload_power: Power consumption during data upload (in watts).
    """
    best = None
    split_index = 0
    for index in range(len(minfo)):
        if target == 'latency':
            cost, _ = calc_latency(minfo, index, bandwidth)
        elif target == 'energy':
            cost, _ = calc_energy(minfo, index, bandwidth, upload_power)
        if best is None or cost < best:
            best = cost
            split_index = index
        else:
            raise ValueError(f"Unsupported target: {target}")

    return split_index

def calc_latency(minfo: model_info.ModelInfo, index: int, bandwidth: float) -> tuple[float,tuple]:
    local_lat = sum(minfo.edge_lat[:index+1]) / 1000**2    # from microsecond
    cloud_lat = sum(minfo.cloud_lat[index+1:]) / 1000**2
    time_upload = minfo.data_size[index] / bandwidth

    tmp = (local_lat, cloud_lat, time_upload)
    return sum(tmp), tmp

def calc_energy(minfo: model_info.ModelInfo, index: int, bandwidth: float, upload_power: float) -> tuple[float,tuple]:
    energy = minfo.edge_energy
    if not energy:
        raise ValueError("Edge energy data is required for energy optimization.")
    
    time_upload = minfo.data_size[index] / bandwidth
    compute_watts = (minfo.edge_lat[i] * energy[i] / 1000**2 for i in range(index + 1))
    upload_watts = upload_power * time_upload
    
    tmp = (compute_watts, upload_watts)
    return tmp, sum(tmp)