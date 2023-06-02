from AgentBasedModel.simulator import SimulatorInfo
import AgentBasedModel.utils.math as math
import matplotlib.pyplot as plt
from collections import defaultdict


"""
Visualisation of Hot Potato Effect (HPE)
1 chart: Shows HFT inventories during timeline with a given delay
2 chart: The number of HFT that are in panic according to timeline with a give delay
3 chart: Shows the last traded price according to timeline with a given delay
"""


def plot_inventories(info: SimulatorInfo, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'HTF inventories, with compliance orders')
    plt.xlabel('Iterations')
    plt.ylabel('Inventories')

    inventories_through_sim = defaultdict(list)
    for asset in info.assets:
        for k, v in asset.items():
            if k in [0, 1, 2, 3, 4]: inventories_through_sim[k].append(v)

    for k, v in inventories_through_sim.items():
        plt.plot(range(len(v)), v, label=f'HFT{k}i')

    plt.legend(loc="upper right")
    plt.savefig(save_path) if save_path else plt.show()


def plot_hpe_price(info: SimulatorInfo, spread=False, rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Last traded price, with compliance orders')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    plt.plot(range(rolling - 1, len(info.prices)), math.rolling(info.prices, rolling), color='black')
    if spread:
        v1 = [el['bid'] for el in info.spreads]
        v2 = [el['ask'] for el in info.spreads]
        plt.plot(range(rolling - 1, len(v1)), math.rolling(v1, rolling), label='bid', color='green')
        plt.plot(range(rolling - 1, len(v2)), math.rolling(v2, rolling), label='ask', color='red')

    plt.savefig(save_path) if save_path else plt.show()


def plot_hfts_in_panic(info: SimulatorInfo, rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'HTFs in panic, with stub quotes')
    plt.xlabel('Iterations')
    plt.ylabel('HFTs in panic')
    plt.plot(range(rolling - 1, len(info.prices)), info.traders_in_panic, color='black')
    plt.savefig(save_path) if save_path else plt.show()


if __name__ == '__main__':
    plot_hfts_in_panic()
