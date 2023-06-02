import os
import glob


def remove_logs() -> str:
    files = glob.glob('./output/logs/*.log')
    for f in files:
        os.remove(f)
    return 'Logs'


def remove_plots() -> str:
    files = glob.glob('./output/plots/*.png')
    for f in files:
        os.remove(f)
    return 'Plots'


def main():
    logs = input("Remove logs [y/n]: ")
    plots = input("Remove plots [y/n]: ")

    if logs == 'y': print(f'\033[92m{remove_logs()} successfully removed\033[0m')
    if plots == 'y': print(f'\033[92m{remove_plots()} successfully\033[0m')


if __name__ == '__main__':
    main()
