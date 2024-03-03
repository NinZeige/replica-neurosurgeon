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
    time_upload = [entry / bandwidth for entry in minfo.data_size]
    for index in range(len(minfo)):
        upload_lat = time_upload[index]
        if target == 'latency':
            local_lat = sum(minfo.edge_lat[:index + 1])
            cloud_lat = sum(minfo.cloud_lat[index + 1:])
            total_lat = local_lat + cloud_lat + upload_lat
            if best is None or total_lat < best:
                best = total_lat
                split_index = index
        elif target == 'energy':
            energy = minfo.edge_energy
            if not energy:
                raise ValueError("Edge energy data is required for energy optimization.")
            compute_watts = sum(minfo.edge_lat[i] * energy[i] for i in range(index + 1))
            upload_watts = upload_power * upload_lat
            total_watts = compute_watts + upload_watts
            if best is None or total_watts < best:
                best = total_watts
                split_index = index
        else:
            raise ValueError(f"Unsupported target: {target}")

    return split_index
