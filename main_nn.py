import pandas as pd

import AgentBasedModel
import random
from AgentBasedModel.agents import DQNAgent, MarketMaker
import json
from AgentBasedModel import plot_price_fundamental, plot_arbitrage, plot_price, plot_dividend, plot_orders, utils
from AgentBasedModel.utils import logging

with open("config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())
logging.Logger.info(f"Config: {json.dumps(config)}")

num_episodes = 10
input_size = 4
output_size = 128
hidden_size = 128
batch_size = 32
target_network_update_freq = 3
learning_rate, discount_factor, exploration_rate = 0.003, 0.8, 0.69
agent = DQNAgent(input_size, output_size, hidden_size, learning_rate, discount_factor, exploration_rate)
agent.load_model("model_checkpoint.pth")

configs = AgentBasedModel.utils.generate_configs(iterations=2000)

with open(f"output/scenarios.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(configs))

counter = 0
for scenario, scenario_configs in configs.items():
    AgentBasedModel.utils.logging.Logger.error(f"Scenario: {scenario}. Configs: [{len(scenario_configs)}]")
    events_dfs = []
    for config_i, config in enumerate(scenario_configs):
        counter += 1
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
        simulator.simulate_nn(agent, config["iterations"])
        infos = simulator.info

        for trader in simulator.traders:
            if isinstance(trader, MarketMaker):
                logging.Logger.info(f"CASH: {trader.cash} {trader.id}")
        logging.Logger.info(f"EPISODE {counter} FINISHED")

    events_dfs = pd.concat(events_dfs)
    events_dfs.to_csv(f"output/scenarios/{scenario}.csv", index=False)

