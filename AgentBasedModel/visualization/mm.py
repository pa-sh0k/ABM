from AgentBasedModel.simulator import SimulatorInfo
import matplotlib.pyplot as plt
from collections import defaultdict
import json

"""
Visualisation for the Cash size of MMs
"""


def plot_cash(info: SimulatorInfo, figsize=(25, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'HTF cash')
    plt.xlabel('Iterations')
    plt.ylabel('Cash')
    plt.xticks([i for i in range(1, 1000, 20)])

    cash_through_sim = defaultdict(list)
    for asset in info.cash:
        for k, v in asset.items():
            if k in [0, 1, 2, 3, 4]: cash_through_sim[k].append(v)

    for k, v in cash_through_sim.items():
        plt.plot(range(len(v)), v, label=f'HFT{k}i')

    plt.legend(loc="upper right")
    plt.savefig(save_path) if save_path else plt.show()


def plot_and_save_cash_avg(info: SimulatorInfo, figsize=(25, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'HTF cash')
    plt.xlabel('Iterations')
    plt.ylabel('Cash')
    plt.xticks([i for i in range(1, 1000, 20)])

    cash_through_sim = defaultdict(list)
    for asset in info.cash:
        for k, v in asset.items():
            if k in range(0, 10): cash_through_sim[k].append(v)

    average = [sum([cash_through_sim[j][i] / 5 for j in range(5)]) for i in range(len(cash_through_sim[0]))]
    with open('base_mm.json', 'w') as f:
        f.write(json.dumps(average))
    plt.plot(range(len(average)), average, label=f'HFT_base_avg')
    plt.legend(loc="upper right")
    plt.savefig(save_path) if save_path else plt.show()


def plot_cash_avg_from_files(file_nn: str, file_base: str, figsize=(25, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'HTF cash')
    plt.xlabel('Iterations')
    plt.ylabel('Cash')
    plt.xticks([i for i in range(1, 1000, 20)])

    with open(file_nn, 'r') as f:
        nn_avg = json.loads(f.read())
    with open(file_base, 'r') as f:
        base_avg = json.loads(f.read())

    plt.plot(range(len(nn_avg)), nn_avg, label=f'HFT_nn_avg')
    plt.plot(range(len(base_avg)), base_avg, label=f'HFT_base_avg')
    plt.legend(loc="upper right")
    plt.savefig(save_path) if save_path else plt.show()
