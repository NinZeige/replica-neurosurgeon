import sys


def plot_nsg(title: str):
    from utils import plot_lantency

    plot_lantency.plot_latency(f'./{title}_edge.json', 5000 * 1000, title=f'{title}-5M')
    plot_lantency.plot_latency(f'./{title}_edge.json', 2000 * 1000, title=f'{title}-2M')
    plot_lantency.plot_latency(f'./{title}_edge.json', 1000 * 1000, title=f'{title}-1M')
    plot_lantency.plot_latency(f'./{title}_edge.json', 500 * 1000, title=f'{title}-500K')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usages: plot.py <title>', file=sys.stderr)
    plot_nsg(sys.argv[1])
