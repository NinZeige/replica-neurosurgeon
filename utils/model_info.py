from typing import List

class ModelInfo:
    def __init__(self, data):
        if not all(len(entry) == len(data[0]) for entry in data):
            raise ValueError("All tuples in data must have the same length")
        self.__data = data

    @property
    def edge_lat(self) -> List[float]:
        """Returns a list of edge latencies."""
        return [entry[0] for entry in self.__data]

    @property
    def cloud_lat(self) -> List[float]:
        """Returns a list of cloud latencies."""
        return [entry[1] for entry in self.__data]

    @property
    def data_size(self) -> List[float]:
        """Returns a list of data sizes."""
        return [entry[2] for entry in self.__data]

    @property
    def edge_energy(self) -> List[float]:
        """Returns a list of edge energies if available, otherwise an empty list."""
        return [entry[3] for entry in self.__data] if len(self.__data[0]) == 4 else []

    def __len__(self) -> int:
        """Returns the number of entries in the data."""
        return len(self.__data)
