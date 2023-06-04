import pandas as pd

import AgentBasedModel
import random
import time
import json
from AgentBasedModel.agents import DQNAgent, MarketMaker
from AgentBasedModel import plot_price_fundamental, plot_arbitrage, plot_price, plot_dividend, plot_orders, utils
from AgentBasedModel.utils import logging

input_size = 6
output_size = 100
hidden_size = 128
batch_size = 32
target_network_update_freq = 3
learning_rate, discount_factor, exploration_rate = 0.01, 0.85, 0.99
agent = DQNAgent(input_size, output_size, hidden_size, learning_rate, discount_factor, exploration_rate)

configs = AgentBasedModel.utils.generate_configs(iterations=1000)

agent.load_model("model_checkpoint.pth")

new_learning_rate, new_discount_factor, new_exploration_rate = 0.005, 0.8, 0.91

for param_group in agent.optimizer.param_groups:
    param_group['lr'] = new_learning_rate

agent.discount_factor = new_discount_factor

agent.exploration_rate = new_exploration_rate

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
        # try:
        simulator.train_nn(batch_size, agent, config["iterations"])
        # except:
        #     continue
        infos = simulator.info

        if counter % target_network_update_freq == 0:
            agent.update_target_network()

        for trader in simulator.traders:
            if isinstance(trader, MarketMaker):
                logging.Logger.info(f"CASH: {trader.cash}")
        logging.Logger.info(f"EPISODE {counter} FINISHED")
        agent.save_model('model_checkpoint.pth')
        logging.Logger.info(f"MODEL SAVED")
        time.sleep(5)

        new_exploration_rate *= 0.999
        agent.exploration_rate = new_exploration_rate

        logging.Logger.info(f"NEW EXPLORATION RATE: {agent.exploration_rate}")


