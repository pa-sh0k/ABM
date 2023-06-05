import matplotlib.pyplot as plt
import pandas as pd

import AgentBasedModel
import random

import json
from AgentBasedModel import plot_price_fundamental, plot_arbitrage, plot_price, plot_dividend, plot_orders, utils
from AgentBasedModel import plot_inventories, plot_hpe_price, plot_hfts_in_panic, plot_cash
from AgentBasedModel.utils import logging

with open("config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())
logging.Logger.info(f"Config: {json.dumps(config)}")

configs = AgentBasedModel.utils.generate_configs(iterations=1000)
with open(f"output/scenarios.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(configs))
for scenario, scenario_configs in configs.items():
    AgentBasedModel.utils.logging.Logger.error(f"Scenario: {scenario}. Configs: [{len(scenario_configs)}]")
    events_dfs = []
    for config_i, config in enumerate(scenario_configs):
        AgentBasedModel.ExchangeAgent.id = 0
        AgentBasedModel.Trader.id = 0
        AgentBasedModel.utils.logging.Logger.error(f"Config: #{config_i}")
        exchanges = []
        traders = []
        events = []

        for exchange in config["exchanges"]:
            exchanges.append(AgentBasedModel.ExchangeAgent(**exchange))
        for trader in config["traders"]:
            params = dict(**trader)
            params.pop("type")
            params.pop("count")
            params["markets"] = [exchanges[_] for _ in trader["markets"]]
            traders.extend(
                [
                    getattr(AgentBasedModel.agents, trader["type"])(**params) for _ in range(trader["count"])
                ]
            )
        for event in config["events"]:
            params = dict(**event)
            params.pop("type")
            events.append(
                getattr(AgentBasedModel.events, event["type"])(**params)
            )
        simulator = AgentBasedModel.Simulator(**{
            'exchanges': exchanges,
            'traders': traders,
            'events': events,
        })
        simulator.simulate(config["iterations"])
        infos = simulator.info

        for _ in range(len(infos)):
            events_dfs.append(AgentBasedModel.utils.make_event_df(info=infos[_], config=config))

            plot_inventories(infos[_], save_path=f"output/plots/{config_i}_inventories_{_}.png")
            plot_hpe_price(infos[_], save_path=f"output/plots/{config_i}_hpe_price_{_}.png")
            plot_hfts_in_panic(infos[_], save_path=f"output/plots/{config_i}_hfts_panic_{_}.png")
            plot_cash(infos[_], save_path=f"output/plots/{config_i}_hfts_cash_nonn_{_}.png")

    events_dfs = pd.concat(events_dfs)
    events_dfs.to_csv(f"output/scenarios/{scenario}.csv", index=False)

